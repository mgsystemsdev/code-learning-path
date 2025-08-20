# demo_qtabwidget.py
# Demo: QTabWidget with multiple tabs

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QTabWidget Demo")
    layout = QVBoxLayout(window)

    tabs = QTabWidget()
    tabs.addTab(QLabel("This is Tab 1"), "Tab 1")
    tabs.addTab(QLabel("This is Tab 2"), "Tab 2")
    tabs.addTab(QLabel("This is Tab 3"), "Tab 3")

    layout.addWidget(tabs)
    window.setLayout(layout)
    window.resize(300, 150)
    window.show()
    return window
