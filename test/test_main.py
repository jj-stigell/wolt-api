from fastapi.testclient import TestClient

from app import constants
from app.main import app

client = TestClient(app)


def test_calculate_fee_endpoint():
    # Correct fee
    response = client.post(
        constants.calculate_endpoint,
        json={
            "cart_value": 10,
            "delivery_distance": 1,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z"
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 2.0}

    # Free delivery
    response = client.post(
        constants.calculate_endpoint,
        json={
            "cart_value": constants.FREE_DELIVERY_THRESHOLD,
            "delivery_distance": 1,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z"
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 0.0}

    # Max delivery fee reached
    response = client.post(
        constants.calculate_endpoint,
        json={
            "cart_value": 1,
            "delivery_distance": 1,
            "number_of_items": (constants.MAX_FEE / constants.ADDITIONAL_ITEM_SURCHARGE) + constants.ADDITIONAL_ITEM_LIMIT,
            "time": "2024-01-15T13:00:00Z"
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": constants.MAX_FEE}


def test_calculate_fee_endpoint_errors():
    # Invalid field
    response = client.post(
        constants.calculate_endpoint,
        json={
            "cart_valu": 10,
            "delivery_distance": 1,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "cart_value"
                ],
                "msg": "Field required",
                "input": {
                    "cart_valu": 10,
                    "delivery_distance": 1,
                    "number_of_items": 1,
                    "time": "2024-01-15T13:00:00Z"
                },
                "url": "https://errors.pydantic.dev/2.5/v/missing"
            }
        ]
    }

    # Invalid type on field
    response = client.post(
        constants.calculate_endpoint,
        json={
            "cart_value": "not valid type",
            "delivery_distance": 1,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": [
                    "body",
                    "cart_value"
                ],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "not valid type",
                "url": "https://errors.pydantic.dev/2.5/v/int_parsing"
            }
        ]
    }
