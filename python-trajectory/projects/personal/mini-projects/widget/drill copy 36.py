from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys


# -------------------------------------
# DRILL 36: External Method Injection
# -------------------------------------
# We're controlling a widget from an outside function

class ActionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Waiting...")
        button = QPushButton("Trigger")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(button)
        self.setLayout(layout)

        self.button = button  # Store reference for controller

def external_controller(widget: ActionWidget):
    widget.button.clicked.connect(lambda: widget.label.setText("Updated externally"))

app = QApplication(sys.argv)
view = ActionWidget()
external_controller(view)
view.setWindowTitle("Drill 36 - External Behavior")
view.show()
sys.exit(app.exec())

# SUMMARY:
# - Logic lives outside the widget class
# - Enables reuse of widget with different controllers
# - First step toward behavioral inversi
