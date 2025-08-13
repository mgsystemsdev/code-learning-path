# app/dialogs.py
"""
Reusable dialogs and item delegates for Smart Learning Tracker.
Includes:
- SuggestionDialog
- TargetTimeDialog
- DateDelegate
- HoursDelegate
- ComboDelegate
"""

from __future__ import annotations

from typing import Callable, Iterable, Optional

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QDialogButtonBox,
    QHBoxLayout,
    QDoubleSpinBox,
    QDateEdit,
    QComboBox,
    QStyledItemDelegate,
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QValidator


# ---------- Suggestion Dialog ----------
class SuggestionDialog(QDialog):
    """
    Presents a list of similar items and lets the user select one
    or choose to create a new item instead.
    """

    def __init__(self, suggestions: Iterable[dict], work_item_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Similar Items Found")
        self.setModal(True)

        self.selected_item_id: Optional[int] = None
        self.create_new: bool = False

        layout = QVBoxLayout(self)

        # Message
        msg = QLabel(
            f"Found similar items to '{work_item_name}'. Choose one or create new:"
        )
        msg.setWordWrap(True)
        layout.addWidget(msg)

        # Suggestion list
        self.list_widget = QListWidget()
        for suggestion in suggestions or []:
            name = suggestion.get("name", "Unnamed")
            hint = suggestion.get("similarity_hint", "")
            item_text = f"{name} ({hint})" if hint else name
            list_item = QListWidgetItem(item_text)
            list_item.setData(Qt.UserRole, suggestion.get("id"))
            self.list_widget.addItem(list_item)
        self.list_widget.itemDoubleClicked.connect(self.accept_suggestion)
        layout.addWidget(self.list_widget)

        # Buttons
        button_box = QDialogButtonBox()
        use_btn = QPushButton("Use Selected")
        use_btn.clicked.connect(self.accept_suggestion)
        button_box.addButton(use_btn, QDialogButtonBox.AcceptRole)

        new_btn = QPushButton("Create New")
        new_btn.clicked.connect(self.create_new_item)
        button_box.addButton(new_btn, QDialogButtonBox.AcceptRole)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_box.addButton(cancel_btn, QDialogButtonBox.RejectRole)

        layout.addWidget(button_box)

        # Select first item by default
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    # Slots
    def accept_suggestion(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            self.selected_item_id = current_item.data(Qt.UserRole)
            self.accept()

    def create_new_item(self):
        self.create_new = True
        self.accept()


# ---------- Target Time Dialog ----------
class TargetTimeDialog(QDialog):
    """
    Quick-pick or custom set target hours for an item.
    """

    def __init__(self, item_name: str, suggested_target: float = 5.0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Target Time")
        self.setModal(True)
        self.target_hours: float = float(suggested_target)

        layout = QVBoxLayout(self)

        # Message
        msg = QLabel(f"Set target hours for '{item_name}':")
        layout.addWidget(msg)

        # Quick buttons
        quick_layout = QHBoxLayout()
        for hours in [5, 10, 15, 20, 30, 50]:
            btn = QPushButton(f"{hours}h")
            btn.clicked.connect(lambda _checked=False, h=hours: self._set_and_accept(h))
            quick_layout.addWidget(btn)
        layout.addLayout(quick_layout)

        # Custom input
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(QLabel("Custom:"))
        self.custom_spin = QDoubleSpinBox()
        self.custom_spin.setRange(0, 1000)
        self.custom_spin.setSingleStep(0.5)
        self.custom_spin.setDecimals(2)
        self.custom_spin.setValue(self.target_hours)
        self.custom_spin.setSuffix(" hours")
        custom_layout.addWidget(self.custom_spin)
        layout.addLayout(custom_layout)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self._accept_custom)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    # Internal helpers
    def _set_and_accept(self, hours: float):
        self.target_hours = float(hours)
        self.accept()

    def _accept_custom(self):
        self.target_hours = float(self.custom_spin.value())
        self.accept()


# ---------- Delegates ----------
class DateDelegate(QStyledItemDelegate):
    """
    Table cell editor for ISO date (yyyy-MM-dd) with calendar popup.
    """

    def createEditor(self, parent, option, index):
        ed = QDateEdit(parent)
        ed.setCalendarPopup(True)
        ed.setDisplayFormat("yyyy-MM-dd")
        return ed

    def setEditorData(self, editor: QDateEdit, index):
        txt = index.data() or QDate.currentDate().toString("yyyy-MM-dd")
        try:
            if isinstance(txt, str) and len(txt) == 10:
                y, m, d = [int(x) for x in txt.split("-")]
                editor.setDate(QDate(y, m, d))
            else:
                editor.setDate(QDate.currentDate())
        except Exception:
            editor.setDate(QDate.currentDate())

    def setModelData(self, editor: QDateEdit, model, index):
        model.setData(index, editor.date().toString("yyyy-MM-dd"))


class HoursDelegate(QStyledItemDelegate):
    """
    Table cell editor for fractional hours [0..24] with 0.25 step.
    """

    def createEditor(self, parent, option, index):
        sp = QDoubleSpinBox(parent)
        sp.setRange(0, 24)
        sp.setSingleStep(0.25)
        sp.setDecimals(2)
        return sp

    def setEditorData(self, editor: QDoubleSpinBox, index):
        try:
            v = float(index.data() or 0.0)
        except (ValueError, TypeError):
            v = 0.0
        editor.setValue(v)

    def setModelData(self, editor: QDoubleSpinBox, model, index):
        model.setData(index, f"{editor.value():.2f}")


class ComboDelegate(QStyledItemDelegate):
    """
    Table cell editor that renders a QComboBox populated by a callable.
    """

    def __init__(self, choices_func: Callable[[], Iterable[str]], allow_blank: bool = True, parent=None):
        super().__init__(parent)
        self.choices_func = choices_func
        self.allow_blank = allow_blank

    def createEditor(self, parent, option, index):
        cb = QComboBox(parent)
        if self.allow_blank:
            cb.addItem("")
        try:
            choices = list(self.choices_func() or [])
            if choices:
                cb.addItems([str(c) for c in choices])
        except Exception:
            # Fail gracefully if provider raises
            pass
        return cb

    def setEditorData(self, editor: QComboBox, index):
        val = str(index.data() or "")
        idx = editor.findText(val)
        editor.setCurrentIndex(max(0, idx))

    def setModelData(self, editor: QComboBox, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)
