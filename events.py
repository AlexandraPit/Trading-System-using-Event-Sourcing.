from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Event:
    timestamp: datetime

@dataclass(frozen=True)
class OrderPlaced(Event):
    order_id: str
    user_id: str
    side: str
    quantity: int
    price: float

@dataclass(frozen=True)
class OrderCancelled(Event):
    order_id: str

@dataclass(frozen=True)
class TradeExecuted(Event):
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: int
    buyer_id: str
    seller_id: str

@dataclass(frozen=True)
class FundsDebited(Event):
    user_id: str
    amount: float

@dataclass(frozen=True)
class FundsCredited(Event):
    user_id: str
    amount: float
