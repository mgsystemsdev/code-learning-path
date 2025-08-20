# demo_qspinbox.py
# Demo: QSpinBox with value display

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox

def launch_demo():
    dialog = QDialog()
    dialog.setWindowTitle("QSpinBox Demo")
    dialog.resize(300, 100)

    layout = QVBoxLayout(dialog)

    label = QLabel("Value: 0")
    spin = QSpinBox()
    spin.setRange(0, 100)
    spin.valueChanged.connect(lambda val: label.setText(f"Value: {val}"))

    layout.addWidget(spin)
    layout.addWidget(label)

    dialog.setLayout(layout)
    dialog.show()
    return dialog
