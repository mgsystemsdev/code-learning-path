# Example: Using receipt classes from another file

from mini_project_cafe_nova import CafeOrder, ReceiptPrinter

# Create order and printer
business = "Coffee Shop"
customer = "jane smith" 
product = "latte"
quantity = 3
price_per_item = 4.25

order = CafeOrder(business, customer, product, quantity, price_per_item)
printer = ReceiptPrinter(
    order.business, 
    order.customer, 
    order.product, 
    order.quantity, 
    order.price_per_item, 
    CafeOrder.TAX_PERCENT, 
    CafeOrder.LINES
)

print(printer.build_receipt())
