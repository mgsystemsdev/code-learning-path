from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys

# -------------------------------------
# DRILL 37: Controller Class Pattern
# -------------------------------------
# We're defining a separate class to control the UI

class LabeledButton(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("...")
        self.button = QPushButton("Go")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

class LabelController:
    def __init__(self, view: LabeledButton):
        self.view = view
        self.view.button.clicked.connect(self.on_click)

    def on_click(self):
        self.view.label.setText("Controller Triggered")

app = QApplication(sys.argv)
view = LabeledButton()
ctrl = LabelController(view)
view.setWindowTitle("Drill 37 - View + Controller")
view.show()
sys.exit(app.exec())

# SUMMARY:
# - Full separation of view and behavior
# - Enables unit testing of logic without GUI
# - Encourages clear role boundaries