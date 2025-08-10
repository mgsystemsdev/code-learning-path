# ============================================================
#  File:        gui_main_qt.py
#  Author:      Miguel Gonzalez Almonte
#  Created:     2025-05-24
#  Description: PySide6 main GUI – mode launcher and log viewer
# ============================================================

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QScrollArea, QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt
from utils.json_utils import ModeLoader
from utils.log_utils import Logger
import subprocess


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎯 Training Python Board – PySide6 GUI")
        self.setMinimumSize(600, 500)

        self.logger = Logger("logs/launch.log")
        self.modes = ModeLoader("modes.json").load_modes()

        layout = QVBoxLayout()

        title = QLabel("Select a mode to launch:")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Mode buttons
        for mode in self.modes:
            btn = QPushButton(mode)
            btn.clicked.connect(lambda checked, m=mode: self.launch_mode(m))
            layout.addWidget(btn)

        # Log table
        self.log_table = QTableWidget(0, 2)
        self.log_table.setHorizontalHeaderLabels(["Timestamp", "Mode"])
        layout.addWidget(self.log_table)
        self.update_log_table()

        container = QWidget()
        container.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        self.setCentralWidget(scroll)
        self.setStatusBar(QStatusBar())

    def launch_mode(self, mode):
        try:
            subprocess.Popen(["python3", f"{mode}.py"])
            self.logger.write(mode)
            self.update_log_table()
            self.statusBar().showMessage(f"Launched: {mode}")
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", f"Could not launch {mode}.py\n{e}")

    def update_log_table(self):
        logs = self.logger.read_last(10)
        self.log_table.setRowCount(len(logs))

        for row, (timestamp, mode) in enumerate(logs):
            self.log_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.log_table.setItem(row, 1, QTableWidgetItem(mode))
