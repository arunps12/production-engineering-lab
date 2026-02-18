"""
Exercise 3.C.2 — Logic Error Investigation
Guide: docs/python-guide/03-debugging.md

The ShoppingCart class produces wrong totals.
Use debugging techniques to find and fix the logic errors.
"""


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity=1):
        """Add item to cart."""
        for item in self.items:
            if item["name"] == name:
                item["quantity"] = quantity  # BUG: should += not =
                return
        self.items.append({"name": name, "price": price, "quantity": quantity})

    def remove_item(self, name):
        """Remove item from cart."""
        for i, item in enumerate(self.items):
            if item["name"] == name:
                del self.items[i]
                # BUG: should return after deletion
                # (deleting while iterating can skip items)

    def get_total(self):
        """Calculate total price."""
        total = 0
        for item in self.items:
            total += item["price"]  # BUG: not multiplying by quantity
        return total

    def apply_discount(self, percent):
        """Apply percentage discount to all items."""
        for item in self.items:
            item["price"] = item["price"] * percent / 100  # BUG: should be (1 - percent/100)

    def __str__(self):
        lines = [f"Shopping Cart ({len(self.items)} items):"]
        for item in self.items:
            lines.append(f"  {item['name']}: ${item['price']:.2f} x {item['quantity']}")
        lines.append(f"  Total: ${self.get_total():.2f}")
        return "\n".join(lines)


# TODO: Fix all bugs and verify with these tests:
cart = ShoppingCart()
cart.add_item("Apple", 1.50, 3)
cart.add_item("Bread", 3.00, 1)
cart.add_item("Apple", 1.50, 2)  # Should now have 5 apples
print(cart)
print(f"Total should be: ${1.50 * 5 + 3.00 * 1:.2f}")
