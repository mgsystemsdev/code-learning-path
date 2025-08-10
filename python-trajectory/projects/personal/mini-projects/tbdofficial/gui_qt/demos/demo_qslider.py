# demo_qslider.py
# Basic QSlider with live label update

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QSlider Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Value: 0")
    layout.addWidget(label)

    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(0)
    slider.setMaximum(100)
    slider.setValue(0)
    slider.valueChanged.connect(lambda val: label.setText(f"Value: {val}"))
    layout.addWidget(slider)

    window.setLayout(layout)
    window.resize(300, 100)
    window.show()
    return window  # ✅ needed for window persistence
