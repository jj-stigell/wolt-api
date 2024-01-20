from datetime import time

from app import constants
from app.order import Order

'''
Specification
Rules for calculating a delivery fee

* If the cart value is less than 10€, a small order surcharge is added to the delivery price.
The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€,
the surcharge will be 1.10€. IMPLEMENTED


* A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added
for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the
distance would be shorter than 500 meters, the minimum fee is always 1€.

    * Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
    * Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
    * Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€



If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. An extra "bulk" fee applies for more than 12 items of 1,20€
Example 1: If the number of items is 4, no extra surcharge
Example 2: If the number of items is 5, 50 cents surcharge is added
Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
Example 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
Example 5: If the number of items is 14, 6,20€ surcharge is added ((10 * 50 cents) + 1,20€)

* The delivery fee can never be more than 15€, including possible surcharges. IMPLEMENTED

* The delivery is free (0€) when the cart value is equal or more than 200€. IMPLEMENTED

During the Friday rush, 3 - 7 PM, the delivery fee (the total fee including possible surcharges) will be multiplied
by 1.2x. However, the fee still cannot be more than the max (15€). Considering timezone, for simplicity, use UTC
as a timezone in backend solutions (so Friday rush is 3 - 7 PM UTC).

'''



def calculate_delivery_fee(order: Order):
    # Free delivery for high cart value
    if order.cart_value >= constants.FREE_DELIVERY_THRESHOLD:
        return 0.0

    # Initial fee
    fee = 0.0

    # Small order surcharge
    if order.cart_value < constants.SMALL_ORDER_THRESHOLD:
        fee += constants.SMALL_ORDER_THRESHOLD - order.cart_value

    # Base delivery fee
    if order.delivery_distance > constants.BASE_DELIVERY_FEE_DISTANCE:
        # Calculate additional distance fees
        additional_distance = order.delivery_distance - constants.BASE_DELIVERY_FEE_DISTANCE
        additional_fees = (additional_distance // constants.ADDITIONAL_FEE_DISTANCE) + 1
        fee += constants.BASE_DELIVERY_FEE + (additional_fees * constants.ADDITIONAL_FEE)
    else:
        fee += constants.BASE_DELIVERY_FEE

    # Item count surcharge
    if order.number_of_items >= constants.ADDITIONAL_ITEM_LIMIT:
        extra_items = order.number_of_items - constants.ADDITIONAL_ITEM_LIMIT - 1
        fee += (extra_items * constants.ADDITIONAL_ITEM_SURCHARGE)
        if order.number_of_items > constants.BULK_FEE_THRESHOLD:
            fee += constants.BULK_FEE

    # Cap the fee at maximum
    fee = min(fee, constants.MAX_FEE)

    # Friday rush hour multiplier
    if order.time.weekday() == constants.RUSH_DELIVERY_DAY and time(constants.RUSH_DELIVERY_START, 0) <= order.time.time() <= time(
            constants.RUSH_DELIVERY_END, 0):
        fee *= constants.RUSH_MULTIPLIER

    # Cap the final fee to be equal or under MAX_FEE
    return min(fee, constants.MAX_FEE)
