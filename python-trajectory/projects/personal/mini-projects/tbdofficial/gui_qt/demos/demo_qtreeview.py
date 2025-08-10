# demo_qtreeview.py
# Demo: QTreeView with QFileSystemModel

import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileSystemModel

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QTreeView Demo")
    layout = QVBoxLayout(window)

    tree = QTreeView()
    model = QFileSystemModel()
    root_path = os.getcwd()
    model.setRootPath(root_path)
    tree.setModel(model)
    tree.setRootIndex(model.index(root_path))

    layout.addWidget(tree)
    window.setLayout(layout)
    window.resize(500, 300)
    window.show()
    return window
