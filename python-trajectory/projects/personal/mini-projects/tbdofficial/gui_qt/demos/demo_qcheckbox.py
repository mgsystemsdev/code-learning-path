# demo_qcheckbox.py
# Demo of basic QCheckBox interactions

from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QCheckBox Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Choose your options:")
    layout.addWidget(label)

    cb1 = QCheckBox("Enable Feature A")
    cb2 = QCheckBox("Enable Feature B")

    def update_label():
        selected = []
        if cb1.isChecked():
            selected.append("A")
        if cb2.isChecked():
            selected.append("B")
        label.setText("Enabled: " + ", ".join(selected) if selected else "Nothing selected")

    cb1.stateChanged.connect(update_label)
    cb2.stateChanged.connect(update_label)

    layout.addWidget(cb1)
    layout.addWidget(cb2)

    window.setLayout(layout)
    window.resize(300, 150)
    window.show()
    return window
