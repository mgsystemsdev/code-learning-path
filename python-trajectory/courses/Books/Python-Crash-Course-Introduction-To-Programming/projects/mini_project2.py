



# Arcade Atlas — Play Pass Receipt                              # COMMENT

# ---------- Settings / Constants ----------
LINES = "-----------------------------------"                   # CONSTANT
ARCADE_FEE_PERCENT = 9                                          # CONSTANT
PRICE_PER_TOKEN = 0.75                                          # CONSTANT

# ---------- Core Data ----------
tokens = 12                                                     # VARIABLE
subtotal = tokens * PRICE_PER_TOKEN                             # UPDATE
total_with_fees = subtotal + (subtotal * ARCADE_FEE_PERCENT / 100)  # UPDATE

# ---------- Header ----------
raw_business = "   Welcome to Arcade Atlas!   "                 # VARIABLE
business = raw_business.strip()                                 # UPDATE
print(LINES)                                                    # OUTPUT
print(f"       {business}       ")                              # OUTPUT
print(LINES)                                                    # OUTPUT
print("")                                                       # OUTPUT

# ---------- Player & Package ----------
raw_customer = "miguel "                                        # VARIABLE
customer = raw_customer.strip().title()                         # UPDATE
print(f"Player: {customer}")                                    # OUTPUT

package_name = "power pack"                                     # VARIABLE
print(package_name.title())                                     # OUTPUT
package_name = "turbo pack"                                     # UPDATE
print(package_name.upper())                                     # OUTPUT

print(f"Tokens: {tokens}")                                      # OUTPUT
print(f"Price per token: {PRICE_PER_TOKEN:.2f}")                # OUTPUT
print(f"Subtotal: {subtotal:.2f}")                              # OUTPUT
print("")                                                       # OUTPUT

print(f"Arcade fee: {ARCADE_FEE_PERCENT}%")                     # OUTPUT
print(f"Total with fee: {total_with_fees:.2f}")                 # OUTPUT
print("")                                                       # OUTPUT

print(LINES)                                                    # OUTPUT
print("       Enjoy your play time!       ")                    # OUTPUT
print(LINES)                                                    # OUTPUT
