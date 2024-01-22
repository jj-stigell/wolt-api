from fastapi import Body

from app.constants import CALCULATE_ENDPOINT
from app.docs import examples, responses
from app.order import Order
from app.server import app


@app.post(CALCULATE_ENDPOINT, responses=responses)
def delivery_fee(order: Order = Body(openapi_examples=examples)):
    return {
        "delivery_fee": order.calculate_delivery_fee()
    }
