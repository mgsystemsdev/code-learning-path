# demo_apicall.py
# Demo: Perform an API call and show response

import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox

def launch_demo():
    window = QWidget()
    window.setWindowTitle("API Call Demo")
    layout = QVBoxLayout(window)

    label = QLabel("Click to fetch data from an API.")
    layout.addWidget(label)

    def fetch_data():
        try:
            response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
            data = response.json()
            QMessageBox.information(window, "API Result", f"Title: {data['title']}")
        except Exception as e:
            QMessageBox.critical(window, "Error", str(e))

    btn = QPushButton("Fetch API Data")
    btn.clicked.connect(fetch_data)
    layout.addWidget(btn)

    window.setLayout(layout)
    window.resize(350, 150)
    window.show()
    return window
