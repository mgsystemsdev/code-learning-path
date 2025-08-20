# demo_qtablewidget.py
# Demo: Tables with QTableWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QTableWidget Demo")
    layout = QVBoxLayout(window)

    table = QTableWidget(4, 3)
    table.setHorizontalHeaderLabels(["Name", "Age", "City"])

    data = [
        ("Alice", 30, "New York"),
        ("Bob", 25, "Los Angeles"),
        ("Charlie", 35, "Chicago"),
        ("Diana", 28, "Houston")
    ]

    for row, (name, age, city) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(name))
        table.setItem(row, 1, QTableWidgetItem(str(age)))
        table.setItem(row, 2, QTableWidgetItem(city))

    layout.addWidget(table)
    window.setLayout(layout)
    window.resize(400, 250)
    window.show()
    return window  # 🔁 Needed for window persistence
