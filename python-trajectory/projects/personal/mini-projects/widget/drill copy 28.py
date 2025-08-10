
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
import sys



# -------------------------------------
# DRILL 28: Accept Parameters on Init
# -------------------------------------
# We're customizing a component via init args — like a factory

class FieldGroup(QWidget):
    def __init__(self, label_text, placeholder):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(label_text))
        self.field = QLineEdit()
        self.field.setPlaceholderText(placeholder)
        layout.addWidget(self.field)
        self.setLayout(layout)

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(FieldGroup("Username", "Enter your name"))
layout.addWidget(FieldGroup("Email", "example@domain.com"))
window.setLayout(layout)
window.setWindowTitle("Drill 28 - Param Widgets")
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Param-driven component logic
# - Supports reusable forms and custom widgets
# - Prevents duplication across similar input sections