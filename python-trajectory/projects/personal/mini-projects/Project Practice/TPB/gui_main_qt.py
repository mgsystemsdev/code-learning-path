# gui_main_qt.py
# PySide6 Showcase with headers and layout polish

import os
import importlib.util
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QScrollArea,
    QMainWindow, QApplication, QFrame
)
from PySide6.QtCore import Qt


class QtShowcaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Showcase")
        self.setMinimumSize(500, 600)

        self.demo_windows = []  # 🔒 Keep references

        scroll = QScrollArea()
        container = QWidget()
        self.layout = QVBoxLayout(container)

        self.add_section("📦 Core Widgets")
        self.load_demos("core")

        self.add_divider()

        self.add_section("🧩 Intermediate Widgets")
        self.load_demos("intermediate")

        self.add_divider()

        self.add_section("🧪 Advanced Patterns")
        self.load_demos("advanced")

        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

    def add_section(self, title):
        label = QLabel(title)
        label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 20px;")
        self.layout.addWidget(label)

    def add_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("margin-top: 10px; margin-bottom: 10px;")
        self.layout.addWidget(line)

    def load_demos(self, level):
        demo_path = os.path.join("gui_qt", "demos", level)
        if not os.path.exists(demo_path):
            self.layout.addWidget(QLabel(f"⚠️ No demos in {level}/"))
            return

        demo_files = sorted(f for f in os.listdir(demo_path) if f.startswith("demo_") and f.endswith(".py"))

        if not demo_files:
            self.layout.addWidget(QLabel("No demo_*.py files found."))
            return

        for demo_file in demo_files:
            name = demo_file.replace("demo_", "").replace(".py", "").replace("_", " ").title()
            btn = QPushButton(f"📦 {name}")
            btn.setStyleSheet("text-align: left; padding: 6px 10px;")
            btn.clicked.connect(lambda _, f=demo_file, p=demo_path: self.run_demo(p, f))
            self.layout.addWidget(btn)

    def run_demo(self, path_dir, filename):
        path = os.path.join(path_dir, filename)
        print(f"▶️ Running demo: {filename}")

        try:
            spec = importlib.util.spec_from_file_location("demo_module", path)
            demo_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(demo_module)

            if hasattr(demo_module, "launch_demo"):
                win = demo_module.launch_demo()
                if isinstance(win, QWidget):
                    self.demo_windows.append(win)
            else:
                print(f"⚠️ {filename} missing launch_demo()")
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")


if __name__ == "__main__":
    app = QApplication([])
    win = QtShowcaseWindow()
    win.show()
    app.exec()
