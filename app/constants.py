"""
All application related constants/variables are set in this file.
This is to make sure the API and all tests work normally even if some values are adjusted.
"""

CALCULATE_ENDPOINT: str = "/feecalc"
"""
API endpoint string for calculating delivery fee.
"""

BASE_DELIVERY_FEE: int = 200
"""
Base delivery fee. Value in euro cents (e.g., value 200 = 2€).
"""

BASE_DELIVERY_FEE_DISTANCE: int = 1_000
"""
Distance (meters) under or equal which the base fee only is charged.
"""

ADDITIONAL_FEE: int = 100
"""
Additional fee (in euro cents) that is charged for delivery distances
over the base distance (BASE_DELIVERY_FEE_DISTANCE).
"""

ADDITIONAL_FEE_DISTANCE: int = 500
"""
Distance (meters) for which additional delivery fees apply.
"""

ADDITIONAL_ITEM_LIMIT: int = 5
"""
Item limit after which additional surcharge is charged for the delivery.
Surcharge is charged for the item that is on the limit and every item over the limit.
"""

ADDITIONAL_ITEM_SURCHARGE: int = 50
"""
Additional item surcharge value, in euro cents.
"""

MAX_FEE: int = 1_500
"""
Maximum fee for the delivery (in euro cents).
"""

RUSH_MULTIPLIER: float = 1.2
"""
Multiplier used for the delivery fee when order is delivered during rush hour period.
"""

RUSH_DELIVERY_DAY: int = 4
"""
Weekday on which the rush delivery applies.
Weekdays are numbered from 0 (Monday) to 6 (Sunday).
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
Free delivery cart value threshold (in euro cents).
If cart value is equal or over this limit, the delivery is free.
"""

SMALL_ORDER_THRESHOLD: int = 1_000
"""
Orders with value under the small order threshold will
have additional fee (in euro cents) added to them.
Fee is based on the cart value and threshold.
"""

BULK_FEE_THRESHOLD: int = 12
"""
Number of items after which the BULK_FEE is added to the order delivery fee.
"""

BULK_FEE: int = 120
"""
Bulk fee (in euro cents) value.
"""
