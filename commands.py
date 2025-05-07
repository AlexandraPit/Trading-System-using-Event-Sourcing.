from datetime import datetime
from typing import Literal
from uuid import uuid4

from events import OrderPlaced, FundsDebited, OrderCancelled, FundsCredited
from event_store import EventStore
from models import OrderBook


def place_order(event_store: EventStore, user_id: str, side: Literal["buy", "sell"], quantity: int, price: float):
    assert quantity > 0
    assert price > 0

    order_id = str(uuid4())
    timestamp = datetime.utcnow()

    if side == "buy":
        total_cost = quantity * price
        event_store.append(FundsDebited(
            timestamp=timestamp,
            user_id=user_id,
            amount=total_cost
        ))

    event_store.append(OrderPlaced(
        timestamp=timestamp,
        order_id=order_id,
        user_id=user_id,
        side=side,
        quantity=quantity,
        price=price
    ))

    print(f"Placed order {order_id}")
    return order_id


def cancel_order(event_store: EventStore, order_book: OrderBook, user_id: str, order_id: str):
    order = order_book.get_active_order(order_id)
    if order is None:
        raise ValueError("Order not found or already inactive")
    if order.user_id != user_id:
        raise ValueError("User is not the owner of this order")

    timestamp = datetime.utcnow()
    event_store.append(OrderCancelled(
        timestamp=timestamp,
        order_id=order_id,
        user_id=user_id
    ))

    if order.side == "buy":
        refund = order.quantity * order.price
        event_store.append(FundsCredited(
            timestamp=timestamp,
            user_id=user_id,
            amount=refund
        ))

    print(f"Cancelled order {order_id}")

