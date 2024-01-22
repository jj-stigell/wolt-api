from fastapi.testclient import TestClient

from app import constants
from app.main import app

client = TestClient(app)


def test_calculate_fee_endpoint_successful():
    # Base fee
    response = client.post(
        constants.CALCULATE_ENDPOINT,
        json={
            "cart_value": constants.SMALL_ORDER_THRESHOLD,
            "delivery_distance": constants.BASE_DELIVERY_FEE_DISTANCE,
            "number_of_items": constants.ADDITIONAL_ITEM_LIMIT - 1,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": constants.BASE_DELIVERY_FEE}

    # Free delivery
    response = client.post(
        constants.CALCULATE_ENDPOINT,
        json={
            "cart_value": constants.FREE_DELIVERY_THRESHOLD,
            "delivery_distance": constants.BASE_DELIVERY_FEE_DISTANCE,
            "number_of_items": constants.ADDITIONAL_ITEM_LIMIT - 1,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 0}

    # Max delivery fee reached
    response = client.post(
        constants.CALCULATE_ENDPOINT,
        json={
            "cart_value": constants.SMALL_ORDER_THRESHOLD,
            "delivery_distance": constants.BASE_DELIVERY_FEE_DISTANCE,
            "number_of_items": (constants.MAX_FEE / constants.ADDITIONAL_ITEM_SURCHARGE) + constants.ADDITIONAL_ITEM_LIMIT,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": constants.MAX_FEE}

    # Assignment example data
    response = client.post(
        constants.CALCULATE_ENDPOINT,
        json={
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}


def test_calculate_fee_endpoint_errors():
    # Invalid/missing field in request body
    response = client.post(
        constants.CALCULATE_ENDPOINT,
        json={
            "cart_valu": 10,
            "delivery_distance": 1,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "cart_value",
                ],
                "msg": "Field required",
                "input": {
                    "cart_valu": 10,
                    "delivery_distance": 1,
                    "number_of_items": 1,
                    "time": "2024-01-15T13:00:00Z",
                },
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
        ],
    }

    # Invalid type on field
    response = client.post(
        constants.CALCULATE_ENDPOINT,
        json={
            "cart_value": "not valid type",
            "delivery_distance": 1,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": [
                    "body",
                    "cart_value",
                ],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "not valid type",
                "url": "https://errors.pydantic.dev/2.5/v/int_parsing",
            },
        ],
    }

    # Invalid date
    response = client.post(
        constants.CALCULATE_ENDPOINT,
        json={
            "cart_value": 1,
            "delivery_distance": 1,
            "number_of_items": 1,
            "time": "2024-0:00Z",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "datetime_parsing",
                "loc": [
                    "body",
                    "time",
                ],
                "msg": "Input should be a valid datetime, invalid character in month",
                "input": "2024-0:00Z",
                "ctx": {
                    "error": "invalid character in month",
                },
                "url": "https://errors.pydantic.dev/2.5/v/datetime_parsing",
            },
        ],
    }

    # Negative value when positive value over 0 expected
    response = client.post(
        constants.CALCULATE_ENDPOINT,
        json={
            "cart_value": -1,
            "delivery_distance": -1,
            "number_of_items": -1,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than",
                "loc": [
                    "body",
                    "cart_value",
                ],
                "msg": "Input should be greater than 0",
                "input": -1,
                "ctx": {
                    "gt": 0,
                },
                "url": "https://errors.pydantic.dev/2.5/v/greater_than",
            },
            {
                "type": "greater_than",
                "loc": [
                    "body",
                    "delivery_distance",
                ],
                "msg": "Input should be greater than 0",
                "input": -1,
                "ctx": {
                    "gt": 0,
                },
                "url": "https://errors.pydantic.dev/2.5/v/greater_than",
            },
            {
                "type": "greater_than",
                "loc": [
                    "body",
                    "number_of_items",
                ],
                "msg": "Input should be greater than 0",
                "input": -1,
                "ctx": {
                    "gt": 0,
                },
                "url": "https://errors.pydantic.dev/2.5/v/greater_than",
            },
        ],
    }

    # 0 value when positive value over 0 expected
    response = client.post(
        constants.CALCULATE_ENDPOINT,
        json={
            "cart_value": 0,
            "delivery_distance": 0,
            "number_of_items": 0,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than",
                "loc": [
                    "body",
                    "cart_value",
                ],
                "msg": "Input should be greater than 0",
                "input": 0,
                "ctx": {
                    "gt": 0,
                },
                "url": "https://errors.pydantic.dev/2.5/v/greater_than",
            },
            {
                "type": "greater_than",
                "loc": [
                    "body",
                    "delivery_distance",
                ],
                "msg": "Input should be greater than 0",
                "input": 0,
                "ctx": {
                    "gt": 0,
                },
                "url": "https://errors.pydantic.dev/2.5/v/greater_than",
            },
            {
                "type": "greater_than",
                "loc": [
                    "body",
                    "number_of_items",
                ],
                "msg": "Input should be greater than 0",
                "input": 0,
                "ctx": {
                    "gt": 0,
                },
                "url": "https://errors.pydantic.dev/2.5/v/greater_than",
            },
        ],
    }
