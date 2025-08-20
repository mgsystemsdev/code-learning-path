# demo_qfiledialog.py
# QFileDialog demo for open/save file

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog

def launch_demo():
    window = QWidget()
    window.setWindowTitle("QFileDialog Demo")
    layout = QVBoxLayout(window)

    path_label = QLabel("No file selected")

    btn_open = QPushButton("📂 Open File")
    btn_open.clicked.connect(lambda: open_file(path_label))

    btn_save = QPushButton("💾 Save File")
    btn_save.clicked.connect(lambda: save_file(path_label))

    layout.addWidget(btn_open)
    layout.addWidget(btn_save)
    layout.addWidget(path_label)

    window.setLayout(layout)
    window.resize(400, 150)
    window.show()
    return window  # 🔒 track demo window

def open_file(label):
    path, _ = QFileDialog.getOpenFileName(None, "Open File")
    if path:
        label.setText(f"Opened: {path}")

def save_file(label):
    path, _ = QFileDialog.getSaveFileName(None, "Save File As")
    if path:
        label.setText(f"Saved: {path}")
