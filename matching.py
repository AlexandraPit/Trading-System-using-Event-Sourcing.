from datetime import datetime
from events import TradeExecuted, FundsCredited, FundsDebited

def match_orders(event_store, order_book, account):
    # Get active buy/sell orders sorted by matching priority
    buy_orders = sorted(
        [o for o in order_book.orders.values() if o.side == "buy" and o.quantity > 0],
        key=lambda o: (-o.price, o.timestamp)
    )
    sell_orders = sorted(
        [o for o in order_book.orders.values() if o.side == "sell" and o.quantity > 0],
        key=lambda o: (o.price, o.timestamp)
    )

    # Attempt to match orders
    for buy in buy_orders:
        for sell in sell_orders:
            if sell.quantity == 0:
                continue  # Already matched

            if buy.price >= sell.price and sell.quantity > 0:
                quantity = min(buy.quantity, sell.quantity)
                price = sell.price

                # Emit trade event
                event_store.append(TradeExecuted(
                    timestamp=datetime.now(),
                    buy_order_id=buy.order_id,
                    sell_order_id=sell.order_id,
                    price=price,
                    quantity=quantity,
                    buyer_id=buy.user_id,
                    seller_id=sell.user_id
                ))

                # Emit account updates
                event_store.append(FundsDebited(
                    timestamp=datetime.now(),
                    user_id=buy.user_id,
                    amount=quantity * price
                ))
                event_store.append(FundsCredited(
                    timestamp=datetime.now(),
                    user_id=sell.user_id,
                    amount=quantity * price
                ))

                # Create and apply updated orders
                updated_buy_order = OrderPlaced(
                    timestamp=buy.timestamp,
                    order_id=buy.order_id,
                    user_id=buy.user_id,
                    side=buy.side,
                    quantity=buy.quantity - quantity,
                    price=buy.price
                )
                updated_sell_order = OrderPlaced(
                    timestamp=sell.timestamp,
                    order_id=sell.order_id,
                    user_id=sell.user_id,
                    side=sell.side,
                    quantity=sell.quantity - quantity,
                    price=sell.price
                )

                # Update the order book with the new orders
                order_book.apply(updated_buy_order)
                order_book.apply(updated_sell_order)

                # Stop the loop if the buy order is completely filled
                if updated_buy_order.quantity == 0:
                    break

    # Replay updated state
    order_book.replay(event_store.get_all_events())
    account.replay(event_store.get_all_events())
