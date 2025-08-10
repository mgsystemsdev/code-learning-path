
# ===============================
# DRILL BLOCK: SK31-B04
# Styling and Themes via CSS and Object Names
# ===============================

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
)
import sys


# -------------------------------------
# DRILL 17: Styling via Object Name
# -------------------------------------
# We're naming widgets for targeted styling

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

field = QLineEdit()
field.setObjectName("usernameField")
field.setPlaceholderText("Username")

field.setStyleSheet("""
    QLineEdit#usernameField {
        background-color: #222;
        color: #FFF;
        border: 2px solid #0af;
        padding: 6px;
    }
""")

layout.addWidget(field)
window.setLayout(layout)
window.setWindowTitle("Drill 17 - Object Name Style")
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Used `setObjectName()` and `QLineEdit#name` CSS selector
# - Scoped style to only one widget, despite shared type
# - Pattern supports precise visual targeting in teams