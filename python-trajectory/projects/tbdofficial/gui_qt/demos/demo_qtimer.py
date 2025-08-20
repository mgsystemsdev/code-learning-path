# demo_qtimer.py
# Demo: QTimer to update label periodically

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QTimer Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Time elapsed: 0 seconds")
    layout.addWidget(label)

    counter = {"seconds": 0}

    timer = QTimer(window)
    timer.timeout.connect(lambda: update_label(label, counter))
    timer.start(1000)

    window.setLayout(layout)
    window.resize(300, 100)
    window.show()
    return window  # 🔁 Needed for window persistence

def update_label(label, counter):
    counter["seconds"] += 1
    label.setText(f"Time elapsed: {counter['seconds']} seconds")
