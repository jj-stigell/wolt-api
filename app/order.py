import math

from pydantic import BaseModel, PositiveInt
from datetime import datetime, time

from app import constants


class Order(BaseModel):
    """
    Represents a food delivery order, including its cart value,
    delivery distance, number of items, and time of the order.
    """
    cart_value: PositiveInt
    delivery_distance: PositiveInt
    number_of_items: PositiveInt
    time: datetime

    def free_delivery(self) -> bool:
        """
        Determines if the order qualifies for free delivery.
        Delivery is free if the cart value is equal or higher than the constant FREE_DELIVERY_THRESHOLD value.

        For example with FREE_DELIVERY_THRESHOLD = 20_000, orders with value 200€ (20 000 in cents) and above
        qualify for free delivery, order with value 199.99€ (19 999 in cents) or lower will not qualify for free delivery.
        """
        return self.cart_value >= constants.FREE_DELIVERY_THRESHOLD

    def calculate_distance_fee(self) -> int:
        """
        Calculates the delivery fee based on the distance. Includes a base fee and additional fees for distances
        exceeding a threshold. If the delivery distance is longer than constant BASE_DELIVERY_FEE_DISTANCE then additional
        fee (constant ADDITIONAL_FEE) is added for each additional distance that is over the ADDITIONAL_FEE_DISTANCE.

        For example if the BASE_DELIVERY_FEE_DISTANCE = 1000, ADDITIONAL_FEE_DISTANCE = 500,
        BASE_DELIVERY_FEE = 200 (2.0€) and ADDITIONAL_FEE = 100 (1.0€), then:
            * If the delivery distance is 1499 meters, the delivery fee is: 200 base fee + 100 for the additional 500 m => 300
            * If the delivery distance is 1500 meters, the delivery fee is: 200 base fee + 100 for the additional 500 m => 300
            * If the delivery distance is 1501 meters, the delivery fee is: 200 base fee + 100 for the first 500 m + 100 for the second 500 m => 400
        """
        fee = constants.BASE_DELIVERY_FEE

        if self.delivery_distance > constants.BASE_DELIVERY_FEE_DISTANCE:
            additional_distance = self.delivery_distance - constants.BASE_DELIVERY_FEE_DISTANCE
            additional_fees = math.ceil(additional_distance / constants.ADDITIONAL_FEE_DISTANCE)
            fee += additional_fees * constants.ADDITIONAL_FEE

        return fee

    def calculate_small_order_surcharge_fee(self) -> int:
        """
        Calculates (possible) the surcharge fee for small orders.
        A surcharge is applied if the cart value is below a certain threshold (constant SMALL_ORDER_THRESHOLD).
        The surcharge is the difference between the cart value and SMALL_ORDER_THRESHOLD.

        For example if SMALL_ORDER_THRESHOLD is 1_000 (in euro cents) and cart value is 890 (in euro cents).
        The surcharge will be SMALL_ORDER_THRESHOLD - cart value = 1_000 - 890 = 110 (1.10€).
        """
        if self.cart_value < constants.SMALL_ORDER_THRESHOLD:
            return constants.SMALL_ORDER_THRESHOLD - self.cart_value

        return 0

    def calculate_bulk_fee(self) -> int:
        """
        Larger order have an extra bulk fee included in them. Bulk fee applies if order has more items than the set
        threshold, defined by constant BULK_FEE_THRESHOLD. Bulk fee value is defined in BULK_FEE constant.

        For example if BULK_FEE_THRESHOLD is 10 and order has 10 items, the bulk fee is NOT CHARGED.
        If the amount of items is 11, the bulk fee IS CHARGED.
        """
        if self.number_of_items > constants.BULK_FEE_THRESHOLD:
            return constants.BULK_FEE

        return 0

    def calculate_item_count_surcharge_fee(self) -> int:
        """
        Calculates surcharge based on the number of items in the order. Includes additional fees
        (constant ADDITIONAL_ITEM_SURCHARGE) for orders exceeding a certain item count (constant ADDITIONAL_ITEM_LIMIT).

        For example if ADDITIONAL_ITEM_LIMIT is 5, ADDITIONAL_ITEM_SURCHARGE is 50 and order has 6 items, then an additional
        surcharge of 100 (2 * 50) is returned. The fee is added for each item above and including the fifth item.
        """
        if self.number_of_items >= constants.ADDITIONAL_ITEM_LIMIT:
            extra_items = self.number_of_items - constants.ADDITIONAL_ITEM_LIMIT + 1
            return extra_items * constants.ADDITIONAL_ITEM_SURCHARGE

        return 0

    def calculate_rush_hour_fees(self, fee: int) -> int:
        """
        Calculates additional fees for orders placed during rush hours.
        Applies a multiplier to the fee for orders within specified rush hour time frames.

        For example, if rush hours time applies, current fee is = 100, and RUSH_MULTIPLIER = 1.2.
        Then the current delivery fee is multiplied 1.2 * 100 = 120.
        """
        fee = fee

        if (self.time.weekday() == constants.RUSH_DELIVERY_DAY and
                time(constants.RUSH_DELIVERY_START, 0) <= self.time.time() <= time(constants.RUSH_DELIVERY_END, 0)):
            fee *= constants.RUSH_MULTIPLIER

        return fee

    def calculate_delivery_fee(self) -> int:
        """
        Calculates the total delivery fee for the order.
        Considers distance fees, item count surcharges, bulk fees, rush hour fees, and small order surcharges.
        Maximum limit is set for the delivery fee (constant MAX_FEE), higher fees will not be charged.
        """
        fee = 0
        if self.free_delivery():
            return fee

        fee += self.calculate_distance_fee()
        fee += self.calculate_item_count_surcharge_fee()
        fee += self.calculate_small_order_surcharge_fee()
        fee += self.calculate_bulk_fee()
        fee = self.calculate_rush_hour_fees(fee)
        return min(fee, constants.MAX_FEE)
