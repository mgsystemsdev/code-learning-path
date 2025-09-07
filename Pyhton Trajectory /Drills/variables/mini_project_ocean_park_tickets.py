# =========================
# Ocean Park Tickets – Demo
# =========================

# ---------- Constants ---------- # CONSTANT
LINES       = "-----------------------------------"   # CONSTANT
LINES_2     = "------------------"                    # CONSTANT
STORE_NAME  = "Ocean Park Tickets "                  # CONSTANT
STORE_TAX   = 10                                     # CONSTANT
CHILD, TICKET, VIP = 4.5, 12.5, 100                  # CONSTANT (multiple assignment)
SUBTOTAL    = TICKET * 4                             # CONSTANT
SALES_TAX   = SUBTOTAL * STORE_TAX / 100             # CONSTANT
FINAL_GREET = "  Thank you for shopping with us!   " # CONSTANT
BIG_NUMBER  = 1_000_000_000                          # CONSTANT (for demo)

# ---------- Customer ---------- # VARIABLE
customer_name = " sofia ".strip().title()            # VARIABLE

# ---------- Outputs ---------- # OUTPUT
print("")                                            # OUTPUT
print(LINES)                                         # OUTPUT
print(f"  Welcome To {STORE_NAME.strip()}!  ")       # OUTPUT
print(LINES)                                         # OUTPUT
print("")                                            # OUTPUT

print(f"Customer: {customer_name}")                  # OUTPUT
print("")                                            # OUTPUT

print("Menu Prices:")                                # OUTPUT
print(f"  Child Ticket: ${CHILD:.2f}")               # OUTPUT
print(f"  Adult Ticket: ${TICKET:.2f}")              # OUTPUT
print(f"  VIP Ticket:   ${VIP:.2f} (one-time payment per year)")  # OUTPUT
print("")                                            # OUTPUT

print("Purchase:")                                    # OUTPUT
print(f"  Tickets: 4 Tickets @ ${TICKET:.2f} = ${SUBTOTAL:.2f}")  # OUTPUT
print("")                                             # OUTPUT

print(LINES_2)                                        # OUTPUT
print(f"Subtotal:  ${SUBTOTAL:.2f}")                  # OUTPUT
print(f"Sales Tax: {STORE_TAX}%")                     # OUTPUT
print(f"Total:     ${SUBTOTAL + SALES_TAX:.2f}")      # OUTPUT
print(LINES_2)                                        # OUTPUT
print("")                                             # OUTPUT

print(LINES)                                          # OUTPUT
print(FINAL_GREET)                                    # OUTPUT
print(LINES)                                          # OUTPUT
print("")                                             # OUTPUT

print(f"Raw big number: {BIG_NUMBER}")                # OUTPUT
print(f"Divided by 1,000: {BIG_NUMBER / 1_000}")      # OUTPUT
