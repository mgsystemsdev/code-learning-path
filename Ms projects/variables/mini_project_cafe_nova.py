





# Mini Project: Café Nova — Receipt Builder                # COMMENT

# ---------- Settings / Constants ----------
LINES = "-----------------------------------"               # CONSTANT
TAX_PERCENT = 8                                             # CONSTANT

# ---------- Customer & Product ----------
raw_business = "   Welcome to Café Nova!   "                # VARIABLE
business = raw_business.strip()                             # UPDATE

raw_customer = "maría "                                     # VARIABLE
customer = raw_customer.strip().title()                     # UPDATE

product = "latte"                                           # VARIABLE
quantity = 2                                                # VARIABLE
price_per_item = 3.5                                        # VARIABLE

# ---------- Totals ----------
total_before_tax = quantity * price_per_item                # UPDATE
tax = total_before_tax * TAX_PERCENT / 100                  # UPDATE
total_with_tax = total_before_tax + tax                     # UPDATE

# ---------- Print Receipt ----------
print("")                                                   # OUTPUT
print(LINES)                                                # OUTPUT
print(f"       {business}       ")                          # OUTPUT
print(LINES)                                                # OUTPUT
print("")                                                   # OUTPUT

print(f"Customer: {customer}")                              # OUTPUT
print(f"Order: {quantity} {product.upper()}(s)")            # OUTPUT
print(f"Price per item: ${price_per_item:.2f}")             # OUTPUT
print(f"Total before tax: ${total_before_tax:.2f}")         # OUTPUT
print("")                                                   # OUTPUT

print(f"Cafe Tax: {TAX_PERCENT}%")                          # OUTPUT
print(f"Total with tax: ${total_with_tax:.2f}")             # OUTPUT
print("")                                                   # OUTPUT

print(LINES)                                                # OUTPUT
print("   Thank you for your purchase!    ")                # OUTPUT
print(LINES)                                                # OUTPUT
print("")                                                   # OUTPUT
