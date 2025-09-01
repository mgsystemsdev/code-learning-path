


from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys
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

# ---------- Build receipt text ----------
receipt_text = "\n".join([
    "",
    LINES,
    f"    Welcome To {STORE_NAME.strip()}!    ",
    LINES,
    "",
    STRIP_COS.title(),
    "",
    "Purchase:",
    "",
    f"{STRIP_I1.title()} - ${PRICE_1}",
    f"{STRIP_I2.title()}  - ${PRICE_2}",
    LINES_2,
    f"Subtotal: ${TOTAL}",
    f"Sales Tax: {STORE_TAX}%",
    LINES_2,
    f"Total: ${FINAL_TOTAL:.2f}",
    "",
    "",
    LINES,
    FINAL_GREET,
    LINES,
    ""
])

# ---------- Qt App ----------
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Receipt")

layout = QVBoxLayout(window)

label = QLabel(receipt_text)
# Keep spaces/alignment and use a monospaced font
label.setTextFormat(Qt.TextFormat.PlainText)  # treat text as plain; preserves spaces
label.setFont(QFont("Courier New", 11))  # mono font for alignment (fallbacks will apply if missing)
label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # optional: allow copy

layout.addWidget(label)

# Nice default size
window.resize(420, 520)
window.show()

sys.exit(app.exec())
