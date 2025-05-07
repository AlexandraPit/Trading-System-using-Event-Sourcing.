from event_store import EventStore
from commands import place_order, cancel_order
from models import OrderBook

event_store = EventStore()

# User 1 places a buy order
order1_id = place_order(event_store, user_id="user1", side="buy", quantity=10, price=5.0)

# User 2 places a sell order
order2_id = place_order(event_store, user_id="user2", side="sell", quantity=8, price=5.0)

# User 1 cancels their order
order_book = OrderBook()
order_book.replay(event_store.get_all_events())

cancel_order(event_store, order_book, user_id="user1", order_id=order1_id)

order_book = OrderBook()
order_book.replay(event_store.get_all_events())

print("\nActive Orders:")
for order in order_book.list_active_orders():
    print(f"- {order.side.upper()} | {order.user_id} | Qty: {order.quantity} @ {order.price}")

print("\nAll Events:")
for event in event_store.get_all_events():
    print(f"- {event}")
