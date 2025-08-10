
# ===============================
# DRILL BLOCK: SK31-B04
# Styling and Themes via CSS and Object Names
# ===============================

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
)
import sys
# -------------------------------------
# DRILL 19: Hover and Focus State Styling
# -------------------------------------
# We're adding interactivity using pseudo-selectors

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

field = QLineEdit()
field.setObjectName("emailInput")
field.setPlaceholderText("Your email")

field.setStyleSheet("""
QLineEdit#emailInput {
    border: 1px solid gray;
    padding: 6px;
}
QLineEdit#emailInput:hover {
    border-color: orange;
}
QLineEdit#emailInput:focus {
    border-color: green;
}
""")

layout.addWidget(field)
window.setLayout(layout)
window.setWindowTitle("Drill 19 - Hover & Focus")
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Added state-based visual changes (hover, focus)
# - Enhances UX and accessibility
# - Must-know for form systems and validation feedback