
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
import sys


# -------------------------------------
# DRILL 29: Extract + Inject Behavior
# -------------------------------------
# We're letting caller define what happens on interaction (callback injection)

class ActionButton(QWidget):
    def __init__(self, label, on_click):
        super().__init__()
        layout = QHBoxLayout()
        self.button = QPushButton(label)
        self.button.clicked.connect(on_click)
        layout.addWidget(self.button)
        self.setLayout(layout)

def say_hello():
    print("Hello from injected function!")

app = QApplication(sys.argv)
window = ActionButton("Greet", say_hello)
window.setWindowTitle("Drill 29 - Callback Injection")
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Accepted external logic and wired it to button
# - Promotes stateless widget design
# - Makes components reusable across use cases
