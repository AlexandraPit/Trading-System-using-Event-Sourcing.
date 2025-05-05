from dataclasses import dataclass
from datetime import datetime
from typing import Literal

@dataclass(frozen=True)
class Event:
    timestamp: datetime

@dataclass(frozen=True)
class OrderPlaced(Event):
    order_id: str
    user_id: str
    side: Literal["buy", "sell"]
    quantity: int
    price: float

@dataclass(frozen=True)
class OrderCancelled(Event):
    order_id: str
    user_id: str

@dataclass(frozen=True)
class TradeExecuted(Event):
    trade_id: str
    buy_order_id: str
    sell_order_id: str
    quantity: int
    price: float

@dataclass(frozen=True)
class FundsDebited(Event):
    user_id: str
    amount: float

@dataclass(frozen=True)
class FundsCredited(Event):
    user_id: str
    amount: float
