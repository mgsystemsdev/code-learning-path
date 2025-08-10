
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
import sys


# -------------------------------------
# DRILL 26: Wrapping Label + Button in Class
# -------------------------------------
# We're packaging a small UI block into its own widget class

class LabelButtonWidget(QWidget):
    def __init__(self, label_text, button_text):
        super().__init__()
        layout = QHBoxLayout()

        self.label = QLabel(label_text)
        self.button = QPushButton(button_text)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

# Use inside window
app = QApplication(sys.argv)
window = QWidget()
main_layout = QVBoxLayout()
main_layout.addWidget(LabelButtonWidget("Name:", "Edit"))
main_layout.addWidget(LabelButtonWidget("Email:", "Update"))
window.setLayout(main_layout)
window.setWindowTitle("Drill 26 - Widget Class")
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Wrapped a repeated layout pattern in a QWidget subclass
# - Enabled reuse across screens
# - Foundation for modular UI component design