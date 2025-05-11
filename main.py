from datetime import datetime

from event_store import EventStore
from commands import place_order, cancel_order
from events import FundsCredited
from models import OrderBook, Account

event_store = EventStore()
account = Account()
order_book = OrderBook()

event_store.append(FundsCredited(
    timestamp=datetime.now(),
    user_id="user1",
    amount=100.0
))
account.replay(event_store.get_all_events())


order1_id = None
try:
    order1_id = place_order(event_store, account, user_id="user1", side="buy", quantity=10, price=5.0)
    print(f"Order1 ID: {order1_id}")

except ValueError as e:
    print("Error placing order1:", e)

account.replay(event_store.get_all_events())
order_book.replay(event_store.get_all_events());
order2_id = place_order(event_store, account,  user_id="user2", side="sell", quantity=8, price=5.0)
order_book.replay(event_store.get_all_events())

order3_id = place_order(event_store, account, user_id="user1", side="buy", quantity=8, price=5.0)
order_book.replay(event_store.get_all_events())

print("Current active orders:", list(order_book.active_orders.keys()))
print("Trying to cancel:", order1_id)

cancel_order(event_store, order_book, user_id="user1", order_id=order1_id)

order_book.replay(event_store.get_all_events())

account.replay(event_store.get_all_events())


print("\nActive Orders:")
for order in order_book.list_active_orders():
    print(f"- {order.side.upper()} | {order.user_id} | Qty: {order.quantity} @ {order.price}")

print("\nAccount Balances:")
for user_id, balance in account.balances.items():
    print(f"- {user_id}: ${balance:.2f}")

print("\nAll Events:")
for event in event_store.get_all_events():
    print(f"- {event}")
