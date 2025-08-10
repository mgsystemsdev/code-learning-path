# demo_qprogressbar.py
# Demo: QProgressBar with fixed value

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QProgressBar Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Task Progress:")
    progress = QProgressBar()
    progress.setRange(0, 100)
    progress.setValue(75)

    layout.addWidget(label)
    layout.addWidget(progress)

    window.setLayout(layout)
    window.resize(300, 120)
    window.show()
    return window
