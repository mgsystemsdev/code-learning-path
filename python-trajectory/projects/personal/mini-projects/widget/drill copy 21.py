from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QSizePolicy
)
import sys


# -------------------------------------
# DRILL 21: Size Policy — Expanding
# -------------------------------------
# We're setting a widget to grow with its container

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

label = QLabel("Expanding Label")
label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow growth

layout.addWidget(label)
window.setLayout(layout)
window.setWindowTitle("Drill 21 - Expanding Policy")
window.resize(300, 200)
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Demonstrated how widgets can grow
# - Both horizontal and vertical expand policies used
# - Important for adaptive container behavior
