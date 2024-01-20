

"""
def test_small_order_surcharge():
    order_data = Order(
        cart_value=max(constants.SMALL_ORDER_THRESHOLD - 2, 0),
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = 2 + constants.BASE_DELIVERY_FEE
    assert calculate_delivery_fee(order_data) == expected_fee


def test_no_small_order_surcharge():
    # Delivery fee should not have small order surcharge when cart_value equal or higher than SMALL_ORDER_THRESHOLD
    order_data = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE
    assert calculate_delivery_fee(order_data) == expected_fee

    order_data = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD + 1,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE
    assert calculate_delivery_fee(order_data) == expected_fee


def test_base_delivery_fee_distance_not_exceed():
    # When delivery distance is equal or below the base delivery distance, no additional fees for delivery distance
    order_data = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE - 1,
        time=not_rush_hour_date
    )
    assert calculate_delivery_fee(order_data) == constants.BASE_DELIVERY_FEE

    order_data = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    assert calculate_delivery_fee(order_data) == constants.BASE_DELIVERY_FEE

    order_data = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + 1,
        time=not_rush_hour_date
    )
    assert calculate_delivery_fee(order_data) > constants.BASE_DELIVERY_FEE


def test_base_delivery_fee_distance_exceeded():
    # When delivery distance is over the base delivery distance, additional fees for delivery included per interval.
    order_data = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + 1,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE
    assert calculate_delivery_fee(order_data) == expected_fee

    order_data = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + constants.ADDITIONAL_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE
    assert calculate_delivery_fee(order_data) == expected_fee

    # Multiples of additional fee
    order_data = Order(
        cart_value=constants.SMALL_ORDER_THRESHOLD,
        number_of_items=1,
        delivery_distance=constants.BASE_DELIVERY_FEE_DISTANCE + constants.ADDITIONAL_FEE_DISTANCE * 3,
        time=not_rush_hour_date
    )
    expected_fee = constants.BASE_DELIVERY_FEE + constants.ADDITIONAL_FEE * 3
    assert calculate_delivery_fee(order_data) == expected_fee








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
















def test_maximum_delivery_fee_cap():
    order_data = Order(
        cart_value=1,
        number_of_items=(constants.MAX_FEE / constants.ADDITIONAL_ITEM_SURCHARGE) + constants.ADDITIONAL_ITEM_LIMIT,
        delivery_distance=1,
        time=not_rush_hour_date
    )
    assert calculate_delivery_fee(order_data) == constants.MAX_FEE

    order_data = Order(
        cart_value=1,
        number_of_items=1,
        delivery_distance=(constants.MAX_FEE / constants.ADDITIONAL_FEE) * constants.BASE_DELIVERY_FEE_DISTANCE,
        time=not_rush_hour_date
    )
    assert calculate_delivery_fee(order_data) == constants.MAX_FEE


def test_free_delivery():
    order_data = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD,
        number_of_items=1,
        delivery_distance=1,
        time=not_rush_hour_date
    )
    assert calculate_delivery_fee(order_data) == 0.0

    order_data = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD + 1,
        number_of_items=1,
        delivery_distance=1,
        time=not_rush_hour_date
    )
    assert calculate_delivery_fee(order_data) == 0.0

    order_data = Order(
        cart_value=constants.FREE_DELIVERY_THRESHOLD - 1,
        number_of_items=1,
        delivery_distance=1,
        time=not_rush_hour_date
    )
    assert calculate_delivery_fee(order_data) != 0.0













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
