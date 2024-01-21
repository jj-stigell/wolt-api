from fastapi import Body

from app import constants
from app.api import app
from app.constants import CALCULATE_ENDPOINT
from app.order import Order


@app.post(CALCULATE_ENDPOINT, responses={
    200: {
        "description": "Calculated delivery fee, in euro cents.",
        "content": {
            "application/json": {
                "example": {
                    "delivery_fee": 250,
                },
            },
        },
    },
})
async def delivery_fee(
    order: Order = Body(
        openapi_examples={
            "normal": {
                "summary": "Normal delivery",
                "description": "Calculate delivery fee for a basic delivery.",
                "value": {
                    "cart_value": constants.SMALL_ORDER_THRESHOLD,
                    "delivery_distance": constants.BASE_DELIVERY_FEE_DISTANCE,
                    "number_of_items": constants.ADDITIONAL_ITEM_LIMIT - 1,
                    "time": "2024-01-21T13:00:00Z",
                },
            },
            "free": {
                "summary": "Free delivery",
                "description": "When cart value is over the free delivery threshold ({} euro cents), delivery is free.".format(constants.FREE_DELIVERY_THRESHOLD),
                "value": {
                    "cart_value": constants.FREE_DELIVERY_THRESHOLD,
                    "delivery_distance": constants.BASE_DELIVERY_FEE_DISTANCE,
                    "number_of_items": constants.ADDITIONAL_ITEM_LIMIT,
                    "time": "2024-01-21T13:00:00Z",
                },
            },
            "max": {
                "summary": "Delivery with maximum fee charged",
                "description": "Deliveries have maximum fee that can be charged from for the order.",
                "value": {
                    "cart_value": constants.SMALL_ORDER_THRESHOLD,
                    "delivery_distance": constants.BASE_DELIVERY_FEE_DISTANCE,
                    "number_of_items": (constants.MAX_FEE / constants.ADDITIONAL_ITEM_SURCHARGE) + constants.ADDITIONAL_ITEM_LIMIT,
                    "time": "2024-01-21T13:00:00Z",
                },
            },
            "wolt_example": {
                "summary": "Wolt assignment example",
                "description": "Example values given in Wolt assignment, should return 710 if assignment values used.",
                "value": {
                    "cart_value": 790,
                    "delivery_distance": 2235,
                    "number_of_items": 4,
                    "time": "2024-01-15T13:00:00Z",
                },
            },
        },
    ),
):

    return {"delivery_fee": order.calculate_delivery_fee()}

