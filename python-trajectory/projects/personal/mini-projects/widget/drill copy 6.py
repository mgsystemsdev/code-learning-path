
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox, QLineEdit
)
import sys


# -------------------------------------
# DRILL 6: Nested Layouts (V-in-H)
# -------------------------------------
# We're composing a window with an HBox layout that embeds a VBox inside

app = QApplication(sys.argv)
window = QWidget()
outer_layout = QHBoxLayout()

left_column = QVBoxLayout()
left_column.addWidget(QLabel("Left 1"))
left_column.addWidget(QLabel("Left 2"))

outer_layout.addLayout(left_column)  # Insert layout into layout
outer_layout.addWidget(QPushButton("Right"))

window.setLayout(outer_layout)
window.setWindowTitle("Drill 6 - Nested Layouts")
window.show()
sys.exit(app.exec())
