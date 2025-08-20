# demo_custom_dialog.py
# Demo: Custom modal QDialog subclass

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Dialog")
        self.resize(300, 120)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is a custom QDialog."))
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

def launch_demo():
    dialog = MyDialog()
    dialog.show()
    return dialog
