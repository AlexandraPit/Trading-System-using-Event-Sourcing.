from datetime import datetime

from events import TradeExecuted, FundsCredited


def match_orders(event_store, order_book, account):
    buy_orders = sorted(
        [o for o in order_book.list_active_orders() if o.side == "buy" and o.quantity > 0],
        key=lambda o: (-o.price, o.timestamp)
    )
    sell_orders = sorted(
        [o for o in order_book.list_active_orders() if o.side == "sell" and o.quantity > 0],
        key=lambda o: (o.price, o.timestamp)
    )

    # Attempt to match orders
    for buy in buy_orders:
        for sell in sell_orders:
            if sell.quantity == 0:
                continue  # Already matched

            if buy.price == sell.price and buy.quantity == sell.quantity:
                quantity = buy.quantity
                price = sell.price

                timestamp = datetime.now()

                # Emit trade event
                event_store.append(TradeExecuted(
                    timestamp=timestamp,
                    buy_order_id=buy.order_id,
                    sell_order_id=sell.order_id,
                    price=price,
                    quantity=quantity,
                    buyer_id=buy.user_id,
                    seller_id=sell.user_id
                ))

                # Emit account updates
                event_store.append(FundsCredited(
                    timestamp=timestamp,
                    user_id=sell.user_id,
                    amount=quantity * price
                ))

                if buy.quantity == 0:
                    break

    order_book.replay(event_store.get_all_events())
    account.replay(event_store.get_all_events())
