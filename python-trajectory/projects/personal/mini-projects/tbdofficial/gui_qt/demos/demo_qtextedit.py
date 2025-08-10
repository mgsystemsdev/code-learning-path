# demo_qtextedit.py
# Demo: QTextEdit multi-line text editor

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QTextEdit Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Type below:")
    text_edit = QTextEdit()
    text_edit.setPlaceholderText("Start typing...")

    layout.addWidget(label)
    layout.addWidget(text_edit)

    window.setLayout(layout)
    window.resize(400, 250)
    window.show()
    return window
