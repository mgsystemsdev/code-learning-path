# demo_qcombobox.py
# QComboBox selection demo

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QComboBox Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Choose your favorite fruit:")
    combo = QComboBox()
    combo.addItems(["Apple", "Banana", "Cherry", "Dragonfruit", "Mango"])
    result = QLabel("Selected: None")

    combo.currentTextChanged.connect(lambda text: result.setText(f"Selected: {text}"))

    layout.addWidget(label)
    layout.addWidget(combo)
    layout.addWidget(result)

    window.setLayout(layout)
    window.resize(300, 150)
    window.show()
    return window  # 🔒 for demo tracking
