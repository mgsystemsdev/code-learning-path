# gui_main_qt.py
# PySide6 Showcase with visual headers and button clarity

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

        self.demo_windows = []

        scroll = QScrollArea()
        container = QWidget()
        self.layout = QVBoxLayout(container)

        # === CORE WIDGETS ===
        self.add_section("📦 Core Widgets", [
            "demo_qpushbutton.py", "demo_qslider.py", "demo_qcheckbox.py", "demo_qlineedit.py",
            "demo_qcombobox.py", "demo_qfiledialog.py", "demo_qtablewidget.py", "demo_qtextedit.py"
        ])

        # === INTERMEDIATE WIDGETS ===
        self.add_section("🧩 Intermediate Widgets", [
            "demo_qprogressbar.py", "demo_qtabwidget.py", "demo_qspinbox.py",
            "demo_qformlayout.py", "demo_qmessagebox.py", "demo_qinputdialog.py",
            "demo_qradiobutton.py", "demo_qlistwidget.py", "demo_qtreeview.py", "demo_qdockwidget.py"
        ])

        # === ADVANCED PATTERNS ===
        self.add_section("🧪 Advanced Patterns", [
            "demo_qtimer.py", "demo_qthread.py", "demo_qstackedwidget.py",
            "demo_layouts.py", "demo_dragdrop.py", "demo_qshortcut.py",
            "demo_qclipboard.py", "demo_qsystemtray.py", "demo_apicall.py", "demo_customdialog.py"
        ])

        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

    def add_section(self, title, demo_files):
        label = QLabel(title)
        label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 16px;")
        self.layout.addWidget(label)

        for demo_file in demo_files:
            path = os.path.join("gui_qt", "demos", demo_file)
            name = demo_file.replace("demo_", "").replace(".py", "").replace("_", " ").title()
            btn = QPushButton(f"📦 {name}")
            btn.clicked.connect(lambda _, f=demo_file: self.run_demo(f))
            self.layout.addWidget(btn)

        self.layout.addWidget(self.make_divider())

    def make_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

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
