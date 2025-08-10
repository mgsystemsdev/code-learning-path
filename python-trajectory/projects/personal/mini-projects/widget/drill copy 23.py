from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QSizePolicy
)
import sys



# SUMMARY:
# - Illustrated how different widgets behave on resize
# - Shows how fixed dimensions resist layout growth
# - Use to control exact vs fluid layout zones


# -------------------------------------
# DRILL 23: Stretch Factor
# -------------------------------------
# We're controlling how extra space is distributed using stretch factors

app = QApplication(sys.argv)
window = QWidget()
layout = QHBoxLayout()

btn1 = QPushButton("25%")
btn2 = QPushButton("75%")

layout.addWidget(btn1, 1)  # Stretch weight = 1
layout.addWidget(btn2, 3)  # Stretch weight = 3

window.setLayout(layout)
window.setWindowTitle("Drill 23 - Stretch Ratio")
window.resize(400, 100)
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Controlled space distribution with stretch weights
# - Essential for proportionally balanced UIs
# - Enables layout tuning without pixel math