from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QCalendarWidget, QLabel, QToolBar
)
from PySide6.QtGui import QFont, QAction   # ✅ FIXED: QAction is here
from PySide6.QtCore import Qt

import sys

# -----------------------------
# Vintage Calendar Main Window
# -----------------------------
class VintageCalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vintage Calendar — Memory Edition")
        self.setMinimumSize(600, 500)

        # Apply layout
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        # Toolbar with navigation actions
        self.toolbar = QToolBar("Navigation")
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        today_action = QAction("Today", self)
        today_action.triggered.connect(self.focus_today)
        self.toolbar.addAction(today_action)

        # Central widget
        central = QWidget()
        layout = QVBoxLayout(central)

        # Header label
        self.title_label = QLabel("My Vintage Calendar")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Georgia", 18, QFont.Bold))
        layout.addWidget(self.title_label)

        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        layout.addWidget(self.calendar)

        self.setCentralWidget(central)

    def focus_today(self):
        self.calendar.setSelectedDate(self.calendar.selectedDate().currentDate())

    def _apply_styles(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #f8f3e8;
        }

        QLabel {
            color: #4e342e;
            font-family: "Georgia";
        }

        QCalendarWidget {
            background-color: #fdf9f4;
            border: 2px solid #d6c5aa;
            border-radius: 14px;
            font-family: "Courier New", monospace;
            font-size: 16px;
            color: #3e2723;
        }

        QCalendarWidget QToolButton {
            background-color: #c1a78f;
            color: #2e1c13;
            font-family: "Georgia";
            font-weight: bold;
            padding: 6px 12px;
            border-radius: 6px;
        }

        QCalendarWidget QToolButton:hover {
            background-color: #a1887f;
        }

        QCalendarWidget QMenu {
            background-color: #f2e2cf;
            color: #5d4037;
            border: 1px solid #b89f87;
        }

        QCalendarWidget QSpinBox {
            background: #efe1d3;
            border: 1px solid #bfa78a;
        }

        QCalendarWidget QAbstractItemView {
            background-color: #fbf5ef;
            selection-background-color: #e4b6a4;
            selection-color: #2f1b0e;
            gridline-color: #d0c0b0;
            alternate-background-color: #f4e9de;
            color: #4e342e; 
        }

        QCalendarWidget QWidget#qt_calendar_navigationbar {
            background-color: #e4d4c1;
            border-bottom: 1px solid #c8b49a;
        }
        """)


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VintageCalendarApp()
    window.show()
    sys.exit(app.exec())
