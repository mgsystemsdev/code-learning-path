
# ===============================
# DRILL BLOCK: SK31-B04
# Styling and Themes via CSS and Object Names
# ===============================

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
)
import sys


# -------------------------------------
# DRILL 18: Multiple Styled Widgets by Class
# -------------------------------------
# We're using a stylesheet string applied to the whole window

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

label = QLabel("Label")
field = QLineEdit()
button = QPushButton("Submit")

style = """
QLabel {
    color: darkgreen;
    font-weight: bold;
}

QLineEdit {
    border: 1px solid gray;
    padding: 4px;
    background: #f0f0f0;
}

QPushButton {
    background-color: darkcyan;
    color: white;
    padding: 8px;
    border-radius: 4px;
}
"""

window.setStyleSheet(style)

layout.addWidget(label)
layout.addWidget(field)
layout.addWidget(button)
window.setLayout(layout)
window.setWindowTitle("Drill 18 - Class-Based Theme")
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Applied app-wide stylesheet using class selectors (QLabel, QLineEdit, etc.)
# - Centralized design control
# - Cleanest way to theme by widget class