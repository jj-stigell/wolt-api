from fastapi import Body

from app.api import app
from app.calculator import calculate_delivery_fee
from app.constants import calculate_endpoint
from app.order import Order


@app.post(calculate_endpoint)
async def delivery_fee(
    order: Order = Body(
        openapi_examples={
            "normal": {
                "summary": "Normal delivery",
                "description": "A **normal** item works correctly.",
                "value": {
                    "cart_value": 790,
                    "delivery_distance": 2235,
                    "number_of_items": 4,
                    "time": "2024-01-15T13:00:00Z",
                },
            },
            "free": {
                "summary": "Delivery with no fee",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
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

