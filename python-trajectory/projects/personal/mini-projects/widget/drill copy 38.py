from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys



# DRILL 38: Pass View into Controller with Custom Signal
# -------------------------------------
# We're letting controller respond to signal from custom component

class Notifier(QWidget):
    sendNotice = Signal(str)

    def __init__(self):
        super().__init__()
        btn = QPushButton("Notify")
        btn.clicked.connect(lambda: self.sendNotice.emit("Hello!"))

        layout = QVBoxLayout()
        layout.addWidget(btn)
        self.setLayout(layout)

class Display(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("...")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class NoticeController:
    def __init__(self, sender: Notifier, receiver: Display):
        sender.sendNotice.connect(self.handle_notice)
        self.view = receiver

    def handle_notice(self, msg):
        self.view.label.setText(f"MSG: {msg}")

app = QApplication(sys.argv)
source = Notifier()
target = Display()
ctrl = NoticeController(source, target)

host = QWidget()
layout = QVBoxLayout()
layout.addWidget(source)
layout.addWidget(target)
host.setLayout(layout)
host.setWindowTitle("Drill 38 - Multi-View Controller")
host.show()
sys.exit(app.exec())

# SUMMARY:
# - Controller links sender and receiver
# - Widgets don’t know about each other
# - Promotes plug-and-play UI structure
