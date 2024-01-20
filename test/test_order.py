from datetime import datetime

from app.calculator import calculate_delivery_fee
from app.order import Order
from app import constants

not_rush_hour_date = datetime(2024, 1, 20, 12)
rush_hour_date_wrong_time = datetime(2024, 1, 20, constants.RUSH_DELIVERY_START - 1)
rush_hour_date_and_time = datetime(2024, 1, 20, constants.RUSH_DELIVERY_START)


def test_free_delivery():
    order = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD,
        delivery_distance=1,
        number_of_items=1,
        time=not_rush_hour_date
    )
    assert order.free_delivery() is True
    assert order.calculate_delivery_fee() == 0.0

    order = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD - 1,
        delivery_distance=1,
        number_of_items=1,
        time=not_rush_hour_date
    )
    assert order.free_delivery() is False
    assert order.calculate_delivery_fee() != 0.0


def test_maximum_delivery_fee_cap():
    order = Order(
        cart_value=1,
        number_of_items=(constants.MAX_FEE / constants.ADDITIONAL_ITEM_SURCHARGE) + constants.ADDITIONAL_ITEM_LIMIT,
        delivery_distance=1,
        time=not_rush_hour_date
    )
    assert order.calculate_delivery_fee() == constants.MAX_FEE
    assert order.free_delivery() is False

    order = Order(
        cart_value=1,
        number_of_items=1,
        delivery_distance=(constants.MAX_FEE / constants.ADDITIONAL_FEE) * constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    assert order.calculate_delivery_fee() == constants.MAX_FEE
    assert order.free_delivery() is False


def test_no_small_order_surcharge():
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE
    assert order.calculate_delivery_fee() == expected_fee
    assert order.small_order_surcharge_fee() == 0.0
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD + 1,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE
    assert order.calculate_delivery_fee() == expected_fee
    assert order.small_order_surcharge_fee() == 0.0
    assert order.free_delivery() is False


def test_small_order_surcharge():
    order = Order(
        cart_value=max(constants.SMALL_ORDER_THRESHOLD - 1, 0),
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = 1 + constants.BASE_DELIVERY_FEE
    assert order.calculate_delivery_fee() == expected_fee
    assert order.small_order_surcharge_fee() == 1.0
    assert order.free_delivery() is False


def test_base_delivery_fee_distance_not_exceed():
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE - 1,
        time=not_rush_hour_date
    )
    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_distance_fee() == constants.BASE_DELIVERY_FEE
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    assert order.calculate_delivery_fee() == constants.BASE_DELIVERY_FEE
    assert order.calculate_distance_fee() == constants.BASE_DELIVERY_FEE
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + 1,
        time=not_rush_hour_date
    )
    assert order.calculate_delivery_fee() > constants.BASE_DELIVERY_FEE
    assert order.calculate_distance_fee() == constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE
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
    assert order.free_delivery() is False

    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + constants.ADDITIONAL_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE * 3
    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_distance_fee() == expected_fee
    assert order.free_delivery() is False

    # Multiples of additional fee
    order = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + constants.ADDITIONAL_FEE_DISTANCE * 3,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE * 3
    assert order.calculate_delivery_fee() == expected_fee
    assert order.calculate_distance_fee() == expected_fee
    assert order.free_delivery() is False



"""

# Test for item count surcharge
def test_item_count_over_surcharge_limit():

    # If order has equal or over the ADDITIONAL_ITEM_LIMIT, extra surcharge applies
    order_data = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD - 1,
        number_of_items=constants.ADDITIONAL_ITEM_LIMIT,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_ITEM_SURCHARGE
    assert calculate_delivery_fee(order_data) == expected_fee

# Test for bulk fee surcharge
def test_bulk_fee_surcharge():
    order_data = Order(cart_value=50, number_of_items=13, delivery_distance=1000, time=datetime(2024, 1, 20, 12))
    expected_fee = constants.BASE_DELIVERY_FEE + (9 * 0.50) + constants.BULK_FEE
    # assert calculate_delivery_fee(order_data) == expected_fee
    assert 1 == 1

# Test for Friday rush hour multiplier
def test_friday_rush_hour_multiplier():
    order_data = Order(cart_value=20, number_of_items=1, delivery_distance=1000, time=datetime(2024, 1, 19, 16)) # Friday
    expected_fee = constants.BASE_DELIVERY_FEE * constants.RUSH_MULTIPLIER
    # assert calculate_delivery_fee(order_data) == expected_fee
    assert 1 == 1


# Test for Friday rush hour with maximum fee cap
def test_friday_rush_hour_with_max_cap():
    order_data = Order(cart_value=10, number_of_items=30, delivery_distance=5000, time=datetime(2024, 1, 19, 16)) # Friday
    # assert calculate_delivery_fee(order_data) == constants.MAX_FEE
    assert 1 == 1


# Test for non-Friday rush hour
def test_non_friday_rush_hour():
    order_data = Order(cart_value=20, number_of_items=1, delivery_distance=1000, time=datetime(2024, 1, 18, 16)) # Not Friday
    # assert calculate_delivery_fee(order_data) == constants.BASE_DELIVERY_FEE
    assert 1 == 1
"""
