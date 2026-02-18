"""
Exercise 3.C.3 — Debugging with Logging
Guide: docs/python-guide/03-debugging.md

Tasks:
1. Replace print() debugging with the logging module
2. Use different log levels (DEBUG, INFO, WARNING, ERROR)
3. Add context to log messages
4. Configure log format with timestamp and level
"""

import logging

# TODO: Configure logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)-8s %(message)s',
# )
# logger = logging.getLogger(__name__)


def process_order(order):
    """Process an order with logging at each step."""
    # TODO: Replace comments with actual logging calls
    # logger.info(f"Processing order {order.get('id')}")

    if not order.get("items"):
        # logger.warning(f"Order {order.get('id')} has no items")
        return None

    total = 0
    for item in order["items"]:
        # logger.debug(f"  Item: {item['name']} x {item['qty']} @ ${item['price']}")
        subtotal = item["price"] * item["qty"]
        total += subtotal

    # logger.info(f"Order {order.get('id')} total: ${total:.2f}")
    return total


# TODO: Test with sample orders
orders = [
    {"id": 1, "items": [{"name": "Widget", "price": 10.0, "qty": 3}]},
    {"id": 2, "items": []},
    {"id": 3, "items": [
        {"name": "Gadget", "price": 25.0, "qty": 1},
        {"name": "Doohickey", "price": 5.0, "qty": 10},
    ]},
]

for order in orders:
    result = process_order(order)
    print(f"Order {order['id']}: ${result:.2f}" if result else f"Order {order['id']}: skipped")
