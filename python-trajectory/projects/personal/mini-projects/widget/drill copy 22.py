from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QSizePolicy
)
import sys


# -------------------------------------
# DRILL 22: Fixed vs Expanding Contrast
# -------------------------------------
# We're comparing fixed-size and expanding widgets side by side

app = QApplication(sys.argv)
window = QWidget()
layout = QHBoxLayout()

fixed_btn = QPushButton("Fixed")
fixed_btn.setFixedWidth(100)  # Locked size

expand_btn = QPushButton("Expands")
expand_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

layout.addWidget(fixed_btn)
layout.addWidget(expand_btn)
window.setLayout(layout)
window.setWindowTitle("Drill 22 - Fixed vs Expanding")
window.resize(400, 100)
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Illustrated how different widgets behave on resize
# - Shows how fixed dimensions resist layout growth
# - Use to control exact vs fluid layout zones