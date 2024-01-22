"""
All application related constants/variables are set in this file.
This is to make sure the API and all tests work normally even if some values are adjusted.

All fees are in represented in euro cents (e.g., value 200 = 2€).
All distances are represented in meters.
"""

CALCULATE_ENDPOINT: str = "/feecalc"
"""
API endpoint string for calculating delivery fee.
"""

BASE_DELIVERY_FEE: int = 200
"""
Base delivery fee for an order. Minimum fee charged unless free delivery applies.
"""

BASE_DELIVERY_FEE_DISTANCE: int = 1_000
"""
Distance under or equal which the base fee only is charged.
"""

ADDITIONAL_FEE: int = 100
"""
Additional fee that is charged for delivery distances over the base distance (BASE_DELIVERY_FEE_DISTANCE).
"""

ADDITIONAL_FEE_DISTANCE: int = 500
"""
Distance for which additional delivery fees (ADDITIONAL_FEE) apply.
"""

ADDITIONAL_ITEM_LIMIT: int = 5
"""
Item limit after which additional surcharge is charged for the delivery.
Surcharge is charged for the item that is on the limit and every item over the limit.
"""

ADDITIONAL_ITEM_SURCHARGE: int = 50
"""
Additional item surcharge value, charged for each additional item in the order.
"""

MAX_FEE: int = 1_500
"""
Maximum fee that can be charged for the delivery.
"""

RUSH_MULTIPLIER: float = 1.2
"""
Multiplier used for the delivery fee when order is delivered during rush hour period.
"""

RUSH_DELIVERY_DAY: int = 4
"""
Weekday on which the rush delivery applies. Weekdays are numbered from 0 (Monday) to 6 (Sunday).
"""

RUSH_DELIVERY_START: int = 15
"""
Start time of the rush hour. Given in 24-hour clock.
"""

RUSH_DELIVERY_END: int = 19
"""
End time of the rush hour. Given in 24-hour clock.
"""

FREE_DELIVERY_THRESHOLD: int = 20_000
"""
Free delivery cart value threshold. If cart value is equal or over this limit, the delivery is free.
"""

SMALL_ORDER_THRESHOLD: int = 1_000
"""
Orders with value under the small order threshold will have additional fee added to them.
Fee is based on the cart value and threshold.
"""

BULK_FEE_THRESHOLD: int = 12
"""
Number of items after which the BULK_FEE is added to the order delivery fee.
"""

BULK_FEE: int = 120
"""
Bulk fee value, charged only once per order if applicable.
"""
