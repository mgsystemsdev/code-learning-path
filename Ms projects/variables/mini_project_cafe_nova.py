# Mini Project: Café Nova — Receipt Builder                # COMMENT
# variables/mini_project_cafe_nova.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Final

# ---------- Settings / Constants ----------
TAX_PERCENT: Final[int] = 8
LINE: Final[str] = "-" * 35
RECEIPT_WIDTH: Final[int] = len(LINE)
BUSINESS_NAME: Final[str] = "Café Nova"


def _money(n: float) -> str:
    return f"${n:,.2f}"


def _plural(word: str, qty: int) -> str:
    return f"{word}" if abs(qty) == 1 else f"{word}s"


@dataclass(frozen=True, slots=True)
class CafeOrder:
    business: str
    customer: str
    product: str
    quantity: int
    price_per_item: float
    tax_percent: int = TAX_PERCENT

    def __post_init__(self) -> None:
        # normalize input
        object.__setattr__(self, "business", self.business.strip())
        object.__setattr__(self, "customer", self.customer.strip().title())
        object.__setattr__(self, "product", self.product.strip())

        # lightweight validation
        if self.quantity < 0:
            raise ValueError("quantity must be >= 0")
        if self.price_per_item < 0:
            raise ValueError("price_per_item must be >= 0")
        if not (0 <= self.tax_percent <= 100):
            raise ValueError("tax_percent must be between 0 and 100")

    @property
    def subtotal(self) -> float:
        return self.quantity * self.price_per_item

    @property
    def tax(self) -> float:
        return self.subtotal * (self.tax_percent / 100.0)

    @property
    def total(self) -> float:
        return self.subtotal + self.tax


class ReceiptPrinter:
    """Pure string builder—no I/O."""

    def __init__(self, line: str = LINE, width: int = RECEIPT_WIDTH) -> None:
        self.line = line
        self.width = width

    def build(self, order: CafeOrder) -> str:
        headline = order.business.center(self.width)
        thanks = "Thank you for your purchase!".center(self.width)

        receipt = [
            "",
            self.line,
            headline,
            self.line,
            "",
            f"Customer: {order.customer}",
            f"Order: {order.quantity} {_plural(order.product.upper(), order.quantity)}",
            f"Price per item: {_money(order.price_per_item)}",
            f"Total before tax: {_money(order.subtotal)}",
            "",
            f"Cafe Tax: {order.tax_percent}%",
            f"Total with tax: {_money(order.total)}",
            "",
            self.line,
            thanks,
            self.line,
            "",
        ]
        return "\n".join(receipt)


def run_demo() -> str:
    order = CafeOrder(
        business=BUSINESS_NAME,
        customer="john doe",
        product="coffee",
        quantity=2,
        price_per_item=3.50,
    )
    return ReceiptPrinter().build(order)


if __name__ == "__main__":
    # Minimal demo if executed directly
    print(run_demo())

# Example usage:
# printer = ReceiptPrinter(business, customer, product, quantity, price_per_item, TAX_PERCENT, LINES)
# print(printer.build_receipt())



# print("")                                                   # OUTPUT
# print(LINES)                                                # OUTPUT
# print(f"       {business}       ")                          # OUTPUT
# print(LINES)                                                # OUTPUT
# print("")                                                   # OUTPUT

# print(f"Customer: {customer}")                              # OUTPUT
# print(f"Order: {quantity} {product.upper()}(s)")            # OUTPUT
# print(f"Price per item: ${price_per_item:.2f}")             # OUTPUT
# print(f"Total before tax: ${total_before_tax:.2f}")         # OUTPUT
# print("")                                                   # OUTPUT

# print(f"Cafe Tax: {TAX_PERCENT}%")                          # OUTPUT
# print(f"Total with tax: ${total_with_tax:.2f}")             # OUTPUT
# print("")                                                   # OUTPUT

# print(LINES)                                                # OUTPUT
# print("   Thank you for your purchase!    ")                # OUTPUT
# print(LINES)                                                # OUTPUT
# print("")                                                   # OUTPUT
