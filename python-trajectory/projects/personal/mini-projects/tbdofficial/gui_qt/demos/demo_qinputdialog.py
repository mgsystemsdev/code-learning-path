# demo_qinputdialog.py
# Demo: Basic QInputDialog usage

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QInputDialog, QLabel

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QInputDialog Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Your input will appear here.")
    layout.addWidget(label)

    def get_text():
        text, ok = QInputDialog.getText(window, "Enter Name", "What is your name?")
        if ok and text:
            label.setText(f"Hello, {text}!")

    btn = QPushButton("Enter Your Name")
    btn.clicked.connect(get_text)
    layout.addWidget(btn)

    window.setLayout(layout)
    window.resize(300, 120)
    window.show()
    return window
