from pydantic import BaseModel, PositiveInt
from datetime import datetime, time

from app import constants


class Order(BaseModel):
    """
    Represents a food delivery order, including its cart value, delivery distance, number of items, and time.
    Provides methods to calculate various fees associated with the order.
    """
    cart_value: PositiveInt
    delivery_distance: PositiveInt
    number_of_items: PositiveInt
    time: datetime

    def free_delivery(self) -> bool:
        """
        Determines if the order qualifies for free delivery.
        Delivery is free if the cart value is equal ir higher than the constant FREE_DELIVERY_THRESHOLD value.

        For example with FREE_DELIVERY_THRESHOLD = 200€, orders with value 200€ and above qualify for free delivery,
        order with value 199€ or lower will not qualify for free delivery.
        """
        return self.cart_value >= constants.FREE_DELIVERY_THRESHOLD

    def calculate_distance_fee(self) -> float:
        """
        Calculates the delivery fee based on the distance.
        Includes a base fee and additional fees for distances exceeding a threshold.
        """
        fee = constants.BASE_DELIVERY_FEE

        if self.delivery_distance > constants.BASE_DELIVERY_FEE_DISTANCE:
            additional_distance = self.delivery_distance - constants.BASE_DELIVERY_FEE_DISTANCE
            additional_fees = (additional_distance // constants.ADDITIONAL_FEE_DISTANCE) + 1
            fee += additional_fees * constants.ADDITIONAL_FEE

        return fee

    def calculate_small_order_surcharge_fee(self) -> float:
        """
        Calculates (possible) the surcharge fee for small orders.
        A surcharge is applied if the cart value is below a certain threshold (constant SMALL_ORDER_THRESHOLD).
        The surcharge is the difference between the cart value and SMALL_ORDER_THRESHOLD.

        For example if SMALL_ORDER_THRESHOLD is 10€ and cart value is 8.90€. The surcharge will be
        SMALL_ORDER_THRESHOLD - cart value = 10€ - 8.90€ = 1.10€.
        """
        if self.cart_value < constants.SMALL_ORDER_THRESHOLD:
            return constants.SMALL_ORDER_THRESHOLD - self.cart_value

        return 0.0

    def calculate_bulk_fee(self):
        """
        Larger order have an extra bulk fee included in them. Bulk fee applies if order has more items than the set
        threshold, defined by constant BULK_FEE_THRESHOLD. Bulk fee value is defined in BULK_FEE constant.

        For example if BULK_FEE_THRESHOLD is 10 and order has 10 items, the bulk fee is NOT CHARGED.
        If the amount of items is 11, the bulk fee IS CHARGED.
        """
        if self.number_of_items > constants.BULK_FEE_THRESHOLD:
            return constants.BULK_FEE

        return 0.0

    def calculate_item_count_surcharge_fee(self) -> float:
        """
        Calculates (possible) surcharge based on the number of items in the order. Includes additional fees
        (constant ADDITIONAL_ITEM_SURCHARGE) for orders exceeding a certain item count (constant ADDITIONAL_ITEM_LIMIT).

        For example if ADDITIONAL_ITEM_LIMIT is 5, ADDITIONAL_ITEM_SURCHARGE is 0.5€ and order has 6 items, then
        an additional surcharge of 1.0€ (2 * 0.5€), fee is added for each item above and including the fifth item.
        """
        if self.number_of_items >= constants.ADDITIONAL_ITEM_LIMIT:
            extra_items = self.number_of_items - constants.ADDITIONAL_ITEM_LIMIT - 1
            return extra_items * constants.ADDITIONAL_ITEM_SURCHARGE

        return 0.0

    def calculate_rush_hour_fees(self, fee: float) -> float:
        """
        Calculates additional fees for orders placed during rush hours.
        Applies a multiplier to the fee for orders within specified rush hour time frames.
        """
        fee = fee

        if self.time.weekday() == constants.RUSH_DELIVERY_DAY and time(constants.RUSH_DELIVERY_START, 0) <= self.time.time() <= time(constants.RUSH_DELIVERY_END, 0):
            fee *= constants.RUSH_MULTIPLIER

        return fee

    def calculate_delivery_fee(self) -> float:
        """
        Calculates the total delivery fee for the order.
        Considers distance fees, item count surcharges, bulk fees, rush hour fees, and small order surcharges.
        Maximum limit is set to the delivery fee (constant MAX_FEE), higher fees will not be charged.
        """
        fee = 0.0
        if self.free_delivery():
            return fee

        fee += self.calculate_distance_fee()
        fee += self.calculate_item_count_surcharge_fee()
        fee += self.calculate_small_order_surcharge_fee()
        fee += self.calculate_bulk_fee()
        fee = self.calculate_rush_hour_fees(fee)
        return min(fee, constants.MAX_FEE)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cart_value": 790,
                    "delivery_distance": 2235,
                    "number_of_items": 4,
                    "time": "2024-01-15T13:00:00Z",
                }
            ]
        }
    }
