from datetime import datetime

from app.order import Order
from app import constants

not_rush_hour_date = datetime(2024, 1, 20, 12)


"""
Emphasis on testing is put on the edge cases of each class method.
e.g., is the value equal or below a certain level after which additional costs are added.
"""


def test_free_delivery():
    # Delivery should be 0 when the cart value is equal or higher than FREE_DELIVERY_THRESHOLD.
    order = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD + 1,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )

    assert order.calculate_bulk_fee() == 0
    assert order.calculate_delivery_fee() == 0
    assert order.free_delivery() is True

    order = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )

    assert order.calculate_bulk_fee() == 0
    assert order.calculate_delivery_fee() == 0
    assert order.free_delivery() is True

    # Not free when cart value just below the threshold.
    order = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD - 1,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )

    assert order.calculate_bulk_fee() == 0
    assert order.calculate_delivery_fee() != 0
    assert order.free_delivery() is False


def test_maximum_delivery_fee():
    # Order delivery fee should cap at max value, if delivery distance, number of items etc. is high enough.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=(constants.MAX_FEE / constants.ADDITIONAL_ITEM_SURCHARGE) + constants.ADDITIONAL_ITEM_LIMIT,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )

    assert order.calculate_delivery_fee() == constants.MAX_FEE
    assert order.calculate_bulk_fee() == constants.BULK_FEE
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=(constants.MAX_FEE / constants.ADDITIONAL_FEE) * constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )

    assert order.calculate_delivery_fee() == constants.MAX_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False


def test_small_order_surcharge():
    # No small order surcharge when cart value equal or higher than the small order threshold.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    expected_fee = constants.BASE_DELIVERY_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_small_order_surcharge_fee() == 0
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # No small order surcharge when cart value equal or higher than the small order threshold.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD + 1,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    expected_fee = constants.BASE_DELIVERY_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_small_order_surcharge_fee() == 0
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Small order surcharge charged, when cart value below the small order threshold.
    order = Order(
        cart_value=max(constants.SMALL_ORDER_THRESHOLD - 1, 0),
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    expected_fee = 1 + constants.BASE_DELIVERY_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_small_order_surcharge_fee() == 1
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    order = Order(
        cart_value=max(constants.SMALL_ORDER_THRESHOLD - 47, 0),
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    expected_fee = 47 + constants.BASE_DELIVERY_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_small_order_surcharge_fee() == 47
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False


def test_delivery_distance_fee():
    # Order delivery fee should be base fee when distance is equal or below BASE_DELIVERY_FEE_DISTANCE.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )

    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_distance_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE - 1,
        time=not_rush_hour_date,
    )

    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_distance_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Distance over the BASE_DELIVERY_FEE_DISTANCE, extra fee charged.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + 1,
        time=not_rush_hour_date,
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_distance_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Additional delivery fee should be charged once for each distance equal or below to the ADDITIONAL_FEE_DISTANCE.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + constants.ADDITIONAL_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_distance_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + constants.ADDITIONAL_FEE_DISTANCE - 1,
        time=not_rush_hour_date,
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_distance_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Multiples of additional fee should be charged correctly.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + constants.ADDITIONAL_FEE_DISTANCE * 3,
        time=not_rush_hour_date,
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE * 3

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_distance_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False


def test_bulk_fee():
    # Bulk fee should be applied only when the number of items is over the BULK_FEE_THRESHOLD.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=constants.BULK_FEE_THRESHOLD + 1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    surcharge_fee = (constants.BULK_FEE_THRESHOLD + 1 - constants.ADDITIONAL_ITEM_LIMIT + 1) * constants.ADDITIONAL_ITEM_SURCHARGE
    expected_fee = constants.BASE_DELIVERY_FEE + surcharge_fee + constants.BULK_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == constants.BULK_FEE
    assert order.calculate_item_count_surcharge_fee() == surcharge_fee
    assert order.free_delivery() is False

    # Not charged when items equal or below the limit.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=constants.BULK_FEE_THRESHOLD,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    surcharge_fee = (constants.BULK_FEE_THRESHOLD - constants.ADDITIONAL_ITEM_LIMIT + 1) * constants.ADDITIONAL_ITEM_SURCHARGE
    expected_fee = constants.BASE_DELIVERY_FEE + surcharge_fee

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.calculate_item_count_surcharge_fee() == surcharge_fee
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=constants.BULK_FEE_THRESHOLD - 1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    surcharge_fee = (constants.BULK_FEE_THRESHOLD - constants.ADDITIONAL_ITEM_LIMIT) * constants.ADDITIONAL_ITEM_SURCHARGE
    expected_fee = constants.BASE_DELIVERY_FEE + surcharge_fee

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.calculate_item_count_surcharge_fee() == surcharge_fee
    assert order.free_delivery() is False


def test_item_count_over_surcharge_limit():
    # Surcharge should be applied if amount of items is over ADDITIONAL_ITEM_LIMIT (this includes the item on the limit).

    # Amount of items equal to the limit.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=constants.ADDITIONAL_ITEM_LIMIT,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_ITEM_SURCHARGE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.calculate_item_count_surcharge_fee() == constants.ADDITIONAL_ITEM_SURCHARGE
    assert order.free_delivery() is False

    # Amount of items is over the limit.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=constants.ADDITIONAL_ITEM_LIMIT + 1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_ITEM_SURCHARGE * 2

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.calculate_item_count_surcharge_fee() == constants.ADDITIONAL_ITEM_SURCHARGE * 2
    assert order.free_delivery() is False

    # Amount of items is below the limit, no surcharges apply.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=constants.ADDITIONAL_ITEM_LIMIT - 1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date,
    )

    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.calculate_item_count_surcharge_fee() == 0
    assert order.free_delivery() is False


def test_rush_hour_multiplier():
    # Date and time in rush hour, when rush hour time starts.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 19, constants.RUSH_DELIVERY_START),
    )
    expected_fee = constants.BASE_DELIVERY_FEE * constants.RUSH_MULTIPLIER

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Date and time in rush hour, when rush hour time ends.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 19, constants.RUSH_DELIVERY_END),
    )
    expected_fee = constants.BASE_DELIVERY_FEE * constants.RUSH_MULTIPLIER

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Rush hour date but not inside the timeframe, multiplier should not be applied.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 19, constants.RUSH_DELIVERY_START - 1),
    )

    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Rush hour date but not inside the timeframe, multiplier should not be applied.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 19, constants.RUSH_DELIVERY_END + 1),
    )

    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Rush time but not rush hour date, multiplier should not be applied.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 18, constants.RUSH_DELIVERY_START),
    )

    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Max delivery fee should work despite rush hour.
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=(constants.MAX_FEE / constants.ADDITIONAL_ITEM_SURCHARGE) + constants.ADDITIONAL_ITEM_LIMIT,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 19, constants.RUSH_DELIVERY_START),
    )

    assert order.calculate_delivery_fee() == constants.MAX_FEE
    assert order.calculate_bulk_fee() == constants.BULK_FEE
    assert order.free_delivery() is False
