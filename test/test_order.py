from datetime import datetime

from app.order import Order
from app import constants

not_rush_hour_date = datetime(2024, 1, 20, 12)


def test_free_delivery():
    order = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )

    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is True
    assert order.calculate_delivery_fee() == 0

    order = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD - 1,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )

    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False
    assert order.calculate_delivery_fee() != 0


def test_maximum_delivery_fee_cap():
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=(constants.MAX_FEE / constants.ADDITIONAL_ITEM_SURCHARGE) + constants.ADDITIONAL_ITEM_LIMIT,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )

    assert order.calculate_delivery_fee() == constants.MAX_FEE
    assert order.calculate_bulk_fee() == constants.BULK_FEE
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=(constants.MAX_FEE / constants.ADDITIONAL_FEE) * constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )

    assert order.calculate_delivery_fee() == constants.MAX_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False


def test_no_small_order_surcharge():
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_small_order_surcharge_fee() == 0
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD + 1,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_small_order_surcharge_fee() == 0
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False


def test_small_order_surcharge():
    order = Order(
        cart_value=max(constants.SMALL_ORDER_THRESHOLD - 1, 0),
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = 1 + constants.BASE_DELIVERY_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_small_order_surcharge_fee() == 1.0
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False


def test_base_delivery_fee_distance_not_exceed():
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE - 1,
        time=not_rush_hour_date
    )

    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_distance_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )

    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_distance_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + 1,
        time=not_rush_hour_date
    )

    assert order.calculate_delivery_fee() > constants.BASE_DELIVERY_FEE
    assert order.calculate_distance_fee() == constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False


def test_base_delivery_fee_distance_exceeded():
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + 1,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_distance_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + constants.ADDITIONAL_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_distance_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Multiples of additional fee
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + constants.ADDITIONAL_FEE_DISTANCE * 3,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE * 3

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_distance_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False


def test_bulk_fee_and_item_count_over_surcharge_limit():
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=constants.BULK_FEE_THRESHOLD + 1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    surcharge_fee = (constants.BULK_FEE_THRESHOLD + 1 - constants.ADDITIONAL_ITEM_LIMIT + 1) * constants.ADDITIONAL_ITEM_SURCHARGE
    expected_fee = constants.BASE_DELIVERY_FEE + surcharge_fee + constants.BULK_FEE

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == constants.BULK_FEE
    assert order.calculate_item_count_surcharge_fee() == surcharge_fee
    assert order.free_delivery() is False


def test_rush_hour_multiplier():
    # Date and time in rush hour, when rush hour time starts
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 19, constants.RUSH_DELIVERY_START)
    )
    expected_fee = constants.BASE_DELIVERY_FEE * constants.RUSH_MULTIPLIER

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Date and time in rush hour, when rush hour time ends
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 19, constants.RUSH_DELIVERY_END)
    )
    expected_fee = constants.BASE_DELIVERY_FEE * constants.RUSH_MULTIPLIER

    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Rush hour date but not time
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=max(constants.ADDITIONAL_ITEM_LIMIT - 1, 1),
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 19, constants.RUSH_DELIVERY_START - 1)
    )

    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_bulk_fee() == 0
    assert order.free_delivery() is False

    # Max delivery fee should work despite rush hour
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=(constants.MAX_FEE / constants.ADDITIONAL_ITEM_SURCHARGE) + constants.ADDITIONAL_ITEM_LIMIT,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=datetime(2024, 1, 19, constants.RUSH_DELIVERY_START)
    )

    assert order.calculate_delivery_fee() == constants.MAX_FEE
    assert order.calculate_bulk_fee() == constants.BULK_FEE
    assert order.free_delivery() is False
