# demo_qlineedit.py
# Demo for QLineEdit basic text input

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QLineEdit Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Enter your name:")
    input_field = QLineEdit()
    output = QLabel("")

    def show_greeting():
        name = input_field.text().strip()
        output.setText(f"Hello, {name}!" if name else "Please enter a name.")

    submit_btn = QPushButton("Greet Me")
    submit_btn.clicked.connect(show_greeting)

    layout.addWidget(label)
    layout.addWidget(input_field)
    layout.addWidget(submit_btn)
    layout.addWidget(output)

    window.setLayout(layout)
    window.resize(300, 150)
    window.show()
    return window  # 🔒 for demo tracking
