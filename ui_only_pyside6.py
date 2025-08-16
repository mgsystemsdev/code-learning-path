# ui_only_pyside6.py
"""
Self-bootable, UI-only PySide6 dashboard window:
- Toolbar (Add, Save, Cancel, Clear Filters, Delete) -> no-op handlers with status feedback.
- Dashboard table with a visible filter row (UI only, no filtering logic).
- Compact two-row form embedded below the table.
- No business logic, I/O, or external app.* imports.

Run:  python ui_only_pyside6.py
Requires: PySide6
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSplitter, QFrame, QStatusBar,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QSpinBox,
    QSizePolicy
)
from PySide6.QtCore import Qt, QTimer

# ---------------------------
# Embedded CompactForm (UI-only)
# ---------------------------
class CompactForm(QWidget):
    """A two-row form layout with 14 fields matching the table columns."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(96)
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(8)

        for row in range(2):
            hl = QHBoxLayout()
            hl.setSpacing(8)
            root.addLayout(hl)

            # Add 7 fields per row (14 total)
            for i in range(7):
                w = QLineEdit()
                w.setFixedHeight(32)
                hl.addWidget(w)

# ---------------------------
# Simple UI-only DashboardTable
# ---------------------------
class DashboardTable(QWidget):
    """A table with a filter row UI (no filter logic) and 14 columns."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.columns = [
            "ID", "Date", "Language", "Type", "Category", "Title",
            "Difficulty", "Progress", "Duration", "Status", "Tags", "Notes", "Score", "Emoji"
        ]

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Filter bar (pure UI; no logic)
        self.filter_bar = QFrame()
        self.filter_bar.setFrameStyle(QFrame.StyledPanel)
        self.filter_bar.setFixedHeight(48)
        self.filter_bar.setStyleSheet("QFrame {{ background:#0f172a; border-bottom:1px solid #334155; }}")
        fl = QHBoxLayout(self.filter_bar)
        fl.setContentsMargins(8, 6, 8, 6)
        fl.setSpacing(8)

        self.filters: Dict[str, QWidget] = {}
        for i, name in enumerate(self.columns):
            w: QWidget
            # make a few of them combos to suggest taxonomy; rest are line edits
            if name in ("Language", "Type", "Status"):
                cb = QComboBox()
                cb.setEditable(True)
                # seed some example values (UI only)
                if name == "Language": cb.addItems(["", "English", "Spanish", "French", "Other"])
                if name == "Type": cb.addItems(["", "Reading", "Listening", "Speaking", "Writing"])
                if name == "Status": cb.addItems(["", "Planned", "In Progress", "Done"])
                w = cb
            elif name in ("Difficulty", "Score"):
                w = QSpinBox()
                w.setRange(0, 10)
            else:
                w = QLineEdit()
                w.setPlaceholderText(f"Filter {{name}}")
            w.setFixedHeight(30)
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.filters[name] = w
            fl.addWidget(w)

        root.addWidget(self.filter_bar)

        # Table
        self.table = QTableWidget(0, len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        root.addWidget(self.table, 1)

        # Fill with a few placeholder rows (UI showcase only)
        self._seed_rows()

    def _seed_rows(self):
        placeholder = [
            ["1", "2025-08-01", "English", "Reading", "News article", "Skim + summarize",
             "5", "1.0", "00:45", "Done", "news, daily", "Short summary...", "8", "👍"],
            ["2", "2025-08-03", "Spanish", "Listening", "Podcast", "Episode 12",
             "6", "0.5", "00:30", "In Progress", "audio", "Notes...", "7", ""],
        ]
        for row in placeholder:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                if c in (0,):  # read-only ID
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(r, c, item)

# ---------------------------
# Main Dashboard Window (UI-only)
# ---------------------------
class DashboardWindow(QMainWindow):
    """Full-screen layout: toolbar on top, table + form split vertically."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("UI-Only Dashboard")
        self.resize(1280, 800)

        self._create_toolbar()
        self._create_status_bar()
        self._build_layout()

    # ---- Top toolbar (UI only) ----
    def _create_toolbar(self):
        self.toolbar = QFrame()
        self.toolbar.setFrameStyle(QFrame.StyledPanel)
        self.toolbar.setFixedHeight(52)
        self.toolbar.setStyleSheet(
            "QFrame {{ background-color:#1e293b; border-bottom:2px solid #475569; }}"
        )
        hl = QHBoxLayout(self.toolbar)
        hl.setContentsMargins(12, 8, 12, 8)
        hl.setSpacing(10)

        self.add_btn = QPushButton("➕ Add")
        self.save_btn = QPushButton("💾 Save")
        self.cancel_btn = QPushButton("↩️ Cancel")
        self.clear_filters_btn = QPushButton("🔍 Clear Filters")
        self.delete_btn = QPushButton("🗑️ Delete")

        for b in (self.add_btn, self.save_btn, self.cancel_btn, self.clear_filters_btn, self.delete_btn):
            b.setFixedHeight(34)

        # Wire to no-op UI feedback
        self.add_btn.clicked.connect(lambda: self._status("Ready to add (UI only)."))
        self.save_btn.clicked.connect(lambda: self._status("Pretend save (UI only)."))
        self.cancel_btn.clicked.connect(lambda: self._status("Canceled (UI only)."))
        self.clear_filters_btn.clicked.connect(lambda: self._status("Filters cleared (UI only)."))
        self.delete_btn.clicked.connect(lambda: self._status("Pretend delete (UI only)."))

        hl.addWidget(self.add_btn)
        hl.addWidget(self.save_btn)
        hl.addWidget(self.cancel_btn)
        hl.addStretch(1)
        hl.addWidget(self.clear_filters_btn)
        hl.addWidget(self.delete_btn)

    # ---- Status bar ----
    def _create_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.records_label = QLabel("📊 Records: 2")
        self.status_label = QLabel("")
        self.status.addPermanentWidget(self.records_label)
        self.status.addWidget(self.status_label, 1)

    # ---- Central layout ----
    def _build_layout(self):
        central = QWidget()
        v = QVBoxLayout(central)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        v.addWidget(self.toolbar)

        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)

        # Top: table
        self.table = DashboardTable()
        splitter.addWidget(self.table)

        # Bottom: compact form
        self.form = CompactForm()
        splitter.addWidget(self.form)

        # Set proportions
        splitter.setStretchFactor(0, 3)  # table
        splitter.setStretchFactor(1, 1)  # form

        v.addWidget(splitter, 1)
        self.setCentralWidget(central)

    def _status(self, msg: str):
        self.status_label.setText(msg)
        self.status_label.show()
        QTimer.singleShot(2500, self.status_label.hide)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = DashboardWindow()
    win.showMaximized()
    sys.exit(app.exec())
