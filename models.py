from typing import Dict, List
from events import (
    OrderPlaced, OrderCancelled, TradeExecuted,
    Event
)


class OrderBook:
    def __init__(self):
        self.active_orders: Dict[str, OrderPlaced] = {}

    def apply(self, event: Event):
        if isinstance(event, OrderPlaced):
            self.active_orders[event.order_id] = event

        elif isinstance(event, OrderCancelled):
            self.active_orders.pop(event.order_id, None)

        elif isinstance(event, TradeExecuted):
            self.active_orders.pop(event.buy_order_id, None)
            self.active_orders.pop(event.sell_order_id, None)

    def replay(self, events: List[Event]):
        for event in events:
            self.apply(event)

    def get_active_order(self, order_id: str):
        return self.active_orders.get(order_id)

    def list_active_orders(self):
        return list(self.active_orders.values())
