from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QSizePolicy
)
import sys


# -------------------------------------
# DRILL 25: Layout Within Layout with Stretch
# -------------------------------------
# We're composing responsive nested layouts with proportional control

app = QApplication(sys.argv)
window = QWidget()
outer_layout = QVBoxLayout()

top_row = QHBoxLayout()
top_row.addWidget(QPushButton("A"), 1)
top_row.addWidget(QPushButton("B"), 2)
top_row.addWidget(QPushButton("C"), 1)

bottom_label = QLabel("Fills remaining space")
bottom_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

outer_layout.addLayout(top_row)
outer_layout.addWidget(bottom_label)

window.setLayout(outer_layout)
window.setWindowTitle("Drill 25 - Nested Responsive Layouts")
window.resize(500, 300)
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Combined nested layouts and stretch logic
# - Created flexible proportional rows
# - Enabled fluid resizing across multiple layout layer