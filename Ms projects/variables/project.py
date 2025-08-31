# ---------- Constants ----------
LINES = "-----------------------------------"                   # CONSTANT
LINES_2 = "------------------"                                  # CONSTANT
STORE_NAME = "Galaxy Gear Store "                               # CONSTANT
STORE_TAX = 7                                                   # CONSTANT
COSTUMER = "   miguel   "                                       # CONSTANT
STRIP_COS = (f"Customer: {COSTUMER.strip()}    ")               # CONSTANT
ITEM_1 = "   KAYAKS   "                                         # CONSTANT
STRIP_I1 = (f"{ITEM_1.strip()}")                                # CONSTANT
ITEM_2 = "   COOLER  "                                          # CONSTANT
STRIP_I2 = (f"{ITEM_2.strip()}")                                # CONSTANT
PRICE_1 = 1000                                                  # CONSTANT
PRICE_2 = 50                                                    # CONSTANT
TOTAL = PRICE_1 + PRICE_2                                       # CONSTANT
FINAL_TOTAL = TOTAL + (TOTAL * STORE_TAX / 100)                 # CONSTANT
FINAL_GREET = "  Thank you for shopping with us!   "            # CONSTANT

# ---------- Outputs ----------
print("")                                                       # OUTPUT
print(LINES)                                                    # OUTPUT
print(f"    Welcome To {STORE_NAME.strip()}!    ")              # OUTPUT
print(LINES)                                                    # OUTPUT
print("")                                                       # OUTPUT
print(STRIP_COS.title())                                        # OUTPUT
print("")
print("Purchase:")
print("")
print(f"{STRIP_I1.title()} - ${PRICE_1}")
print(f"{STRIP_I2.title()}  - ${PRICE_2}")
print(LINES_2)
print(f"Subtotal: ${TOTAL}")
print(f"Sales Tax: {STORE_TAX}%")
print(LINES_2)
print(f"Total: ${FINAL_TOTAL:.2f}")
print("")
print("")
print(LINES)
print(FINAL_GREET)
print(LINES)
print("")

