from collections import defaultdict
from typing import Dict, List
from events import (
    OrderPlaced, OrderCancelled, TradeExecuted,
    Event, FundsDebited, FundsCredited
)

class OrderBook:
    def __init__(self):
        self.active_orders: Dict[str, OrderPlaced] = {}
        self.filled_quantities: Dict[str, int] = defaultdict(int)

    def apply(self, event: Event):
        if isinstance(event, OrderPlaced):
            self.active_orders[event.order_id] = event

        elif isinstance(event, OrderCancelled):
            self.active_orders.pop(event.order_id, None)

        elif isinstance(event, TradeExecuted):

            if event.buy_order_id in self.active_orders:
                self.active_orders.pop(event.buy_order_id)
            if event.sell_order_id in self.active_orders:
                self.active_orders.pop(event.sell_order_id)

    def replay(self, events: List[Event]):
        self.active_orders = {}
        self.filled_quantities = defaultdict(int)
        for event in events:
            self.apply(event)

    def get_active_order(self, order_id: str):
        return self.active_orders.get(order_id)

    def list_active_orders(self):
        return list(self.active_orders.values())

class Account:
    def __init__(self):
        self.balances: Dict[str, float] = {}

    def apply(self, event: Event):
        if isinstance(event, FundsCredited):
            self.balances[event.user_id] = self.balances.get(event.user_id, 0) + event.amount

        elif isinstance(event, FundsDebited):
            self.balances[event.user_id] = self.balances.get(event.user_id, 0) - event.amount

    def replay(self, events: List[Event]):
        self.balances = {}
        for event in events:
            self.apply(event)

    def get_balance(self, user_id: str) -> float:
        return self.balances.get(user_id, 0.0)