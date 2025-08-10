from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys



# -------------------------------------
# DRILL 39: Event-Driven Logic from Controller
# -------------------------------------
# We're triggering multiple behaviors from one slot

class Emitter(QWidget):
    signal = Signal()

    def __init__(self):
        super().__init__()
        btn = QPushButton("Emit")
        btn.clicked.connect(self.signal)
        layout = QVBoxLayout()
        layout.addWidget(btn)
        self.setLayout(layout)

class OutputA(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("A")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class OutputB(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("B")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class BroadcastController:
    def __init__(self, emitter: Emitter, a: OutputA, b: OutputB):
        emitter.signal.connect(lambda: self.update_all(a, b))

    def update_all(self, a, b):
        a.label.setText("Updated A")
        b.label.setText("Updated B")

app = QApplication(sys.argv)
send = Emitter()
a = OutputA()
b = OutputB()
ctrl = BroadcastController(send, a, b)

host = QWidget()
layout = QVBoxLayout()
layout.addWidget(send)
layout.addWidget(a)
layout.addWidget(b)
host.setLayout(layout)
host.setWindowTitle("Drill 39 - Broadcast Logic")
host.show()
sys.exit(app.exec())

# SUMMARY:
# - One signal affects multiple receivers
# - Controller manages the routing logic
# - Decoupled event graph = scalable system
