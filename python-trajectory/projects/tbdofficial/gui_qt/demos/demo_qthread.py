# demo_qthread.py
# Demo: QThread for background counting task

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QThread, Signal
import time

class CounterThread(QThread):
    update = Signal(int)

    def run(self):
        for i in range(1, 6):
            time.sleep(1)
            self.update.emit(i)

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QThread Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Press start to begin counting...")
    layout.addWidget(label)

    btn = QPushButton("Start Counting")
    layout.addWidget(btn)

    thread = CounterThread()
    thread.update.connect(lambda val: label.setText(f"Count: {val}"))
    btn.clicked.connect(thread.start)

    window.setLayout(layout)
    window.resize(300, 120)
    window.show()
    return window  # 🔁 Needed for window persistence
