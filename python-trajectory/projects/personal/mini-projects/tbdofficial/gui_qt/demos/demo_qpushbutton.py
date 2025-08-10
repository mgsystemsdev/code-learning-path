# demo_qpushbutton.py
# Simple QPushButton behaviors demo

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QPushButton Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Click a button below:")
    layout.addWidget(label)

    btn_hello = QPushButton("Say Hello")
    btn_hello.clicked.connect(lambda: label.setText("👋 Hello there!"))
    layout.addWidget(btn_hello)

    btn_popup = QPushButton("Show MessageBox")
    btn_popup.clicked.connect(lambda: QMessageBox.information(window, "Message", "This is a QMessageBox!"))
    layout.addWidget(btn_popup)

    btn_close = QPushButton("Close Window")
    btn_close.clicked.connect(window.close)
    layout.addWidget(btn_close)

    window.setLayout(layout)
    window.resize(300, 200)
    window.show()
    return window  # ✅ critical to keep it alive
