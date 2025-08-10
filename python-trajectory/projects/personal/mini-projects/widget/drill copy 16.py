
# ===============================
# DRILL BLOCK: SK31-B04
# Styling and Themes via CSS and Object Names
# ===============================

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
)
import sys


# -------------------------------------
# DRILL 16: Basic Inline Styling
# -------------------------------------
# We're adding background and font styling via `.setStyleSheet`

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

label = QLabel("Styled Label")
label.setStyleSheet("color: white; background-color: darkblue; padding: 10px; font-size: 18px;")

layout.addWidget(label)
window.setLayout(layout)
window.setWindowTitle("Drill 16 - Basic Styling")
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Applied inline stylesheet to QLabel
# - Demonstrated control over color, font, padding
# - First step to full CSS-driven theming
