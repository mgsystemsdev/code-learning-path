
# demo_qformlayout.py
# Demo: QFormLayout with input fields

from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QVBoxLayout

def launch_demo():
    dialog = QDialog()
    dialog.setWindowTitle("QFormLayout Demo")
    dialog.resize(300, 150)

    form = QFormLayout()
    form.addRow("First Name:", QLineEdit())
    form.addRow("Last Name:", QLineEdit())
    form.addRow("Email:", QLineEdit())

    container = QVBoxLayout(dialog)
    container.addLayout(form)

    dialog.setLayout(container)
    dialog.show()
    return dialog
