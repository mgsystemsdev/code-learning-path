# gui_main_qt.py
# Main PySide6 GUI showcase window — auto-loads all demos from gui_qt/demos/

import os
import importlib.util
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QScrollArea,
    QMainWindow, QApplication
)
from PySide6.QtCore import Qt


class QtShowcaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Showcase")
        self.setMinimumSize(500, 600)

        self.demo_windows = []  # 🔒 Store windows to prevent garbage collection

        scroll = QScrollArea()
        container = QWidget()
        self.layout = QVBoxLayout(container)

        self.load_demos()

        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

    def load_demos(self):
        demo_path = os.path.join("gui_qt", "demos")
        if not os.path.exists(demo_path):
            self.layout.addWidget(QLabel("No demos found."))
            return

        demos = sorted(f for f in os.listdir(demo_path) if f.startswith("demo_") and f.endswith(".py"))

        if not demos:
            self.layout.addWidget(QLabel("No demo_*.py files found."))
            return

        for demo_file in demos:
            name = demo_file.replace("demo_", "").replace(".py", "").replace("_", " ").title()
            btn = QPushButton(f"📦 {name}")
            btn.clicked.connect(lambda _, f=demo_file: self.run_demo(f))
            self.layout.addWidget(btn)

        self.layout.addStretch()

    def run_demo(self, filename):
        path = os.path.join("gui_qt", "demos", filename)
        print(f"▶️ Running demo: {filename}")

        try:
            spec = importlib.util.spec_from_file_location("demo_module", path)
            demo_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(demo_module)

            if hasattr(demo_module, "launch_demo"):
                win = demo_module.launch_demo()
                if isinstance(win, QWidget):
                    self.demo_windows.append(win)  # 🔒 Keep demo alive
            else:
                print(f"⚠️ {filename} missing launch_demo()")
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")


# Run manually for testing
if __name__ == "__main__":
    app = QApplication([])
    win = QtShowcaseWindow()
    win.show()
    app.exec()
