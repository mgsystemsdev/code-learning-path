from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QSizePolicy
)
import sys


# -------------------------------------
# DRILL 24: Minimum Size Enforcement
# -------------------------------------
# We're preventing widgets from shrinking below a usable size

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

field = QLineEdit()
field.setMinimumWidth(200)  # Can't shrink smaller than this

layout.addWidget(field)
window.setLayout(layout)
window.setWindowTitle("Drill 24 - Minimum Width")
window.resize(300, 100)
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Added minimum width to protect UX
# - Often used with responsive layouts
# - Prevents content from becoming unreadable