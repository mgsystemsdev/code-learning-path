# === PySide6 Widgets and Core ===
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QDateEdit, QComboBox,
    QLabel, QPushButton, QTextEdit, QFrame, QGroupBox, QCheckBox, QScrollArea, QWidget
)
from PySide6.QtCore import Qt

# ✅ Connect to lookup database
from lookup_manager import get_lookup_values


class UnitFormDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ready Suite")
        self.setMinimumSize(1000, 720)

        # --- SCROLLABLE WRAPPER ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 6)

        # --- SECTION 0: TITLE ---
        title = QLabel("MR BOARD")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        # --- SECTION 1: INPUT + AUTO PANEL ROW ---
        row_layout = QHBoxLayout()
        left_column = QVBoxLayout()
        left_column.setAlignment(Qt.AlignTop)

        def labeled_row(label_text, widget):
            row = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(80)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            widget.setFixedWidth(120)
            row.addWidget(label)
            row.addWidget(widget)
            return row

        self.property_field = QComboBox(); self.property_field.setEditable(True)
        self.property_field.addItems(get_lookup_values("properties"))
        self.unit_number_field = QLineEdit()
        self.move_out_date = QDateEdit(); self.move_out_date.setCalendarPopup(True)
        self.move_in_date = QDateEdit(); self.move_in_date.setCalendarPopup(True)
        self.condition_field = QComboBox(); self.condition_field.setEditable(True)
        self.condition_field.addItems(get_lookup_values("statuses"))
        self.task_code_field = QLineEdit()

        self.property_field.currentTextChanged.connect(self.update_task_code)
        self.unit_number_field.textChanged.connect(self.update_task_code)

        left_column.addLayout(labeled_row("Property:", self.property_field))
        left_column.addLayout(labeled_row("Unit:", self.unit_number_field))
        left_column.addLayout(labeled_row("M/O:", self.move_out_date))
        left_column.addLayout(labeled_row("M/I:", self.move_in_date))
        left_column.addLayout(labeled_row("Condition:", self.condition_field))
        left_column.addLayout(labeled_row("Task code:", self.task_code_field))
        row_layout.addLayout(left_column)

        # CENTER BUTTONS
        center_column = QVBoxLayout()
        center_column.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        submit_btn = QPushButton("Submit")
        reload_btn = QPushButton("Reload")
        clear_btn = QPushButton("Clear")
        for btn in [submit_btn, reload_btn, clear_btn]:
            btn.setFixedWidth(100)
            center_column.addWidget(btn, alignment=Qt.AlignCenter)
            center_column.addSpacing(8)
        row_layout.addLayout(center_column)

        # RIGHT AUTO FIELDS
        right_column = QVBoxLayout()
        right_column.setAlignment(Qt.AlignTop)
        self.dtbr_label = QLabel("—")
        self.days_vacant_label = QLabel("—")
        self.unit_type_label = QLabel("—")
        self.sqft_label = QLabel("—")
        self.task_code_display = QLabel("—")
        self.status_label = QLabel("—")
        self.nvm_label = QLabel("—")

        auto_labels = [
            ("DTBR:", self.dtbr_label),
            ("Days Vacant:", self.days_vacant_label),
            ("Unit Type:", self.unit_type_label),
            ("SQFT:", self.sqft_label),
            ("Task Code:", self.task_code_display),
            ("Status:", self.status_label),
            ("N/V/M:", self.nvm_label),
        ]

        auto_frame = QFrame()
        auto_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        auto_frame.setLineWidth(1)
        auto_frame.setStyleSheet("background-color: #222; color: white; border: 1px solid #555;")
        auto_layout = QGridLayout()
        auto_layout.setContentsMargins(8, 6, 8, 6)
        auto_layout.setHorizontalSpacing(8)
        auto_layout.setVerticalSpacing(4)

        for i, (label_text, label_widget) in enumerate(auto_labels):
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            label.setAlignment(Qt.AlignRight)
            label_widget.setAlignment(Qt.AlignCenter)
            auto_layout.addWidget(label, i, 0)
            auto_layout.addWidget(label_widget, i, 1)

        auto_frame.setLayout(auto_layout)
        right_column.addWidget(auto_frame)
        row_layout.addLayout(right_column)
        layout.addLayout(row_layout)

        # --- TASK CHECKLIST GRID ---
        self.task_fields = {}
        task_group = QGroupBox("")
        task_grid = QGridLayout()
        task_grid.setHorizontalSpacing(10)
        task_grid.setVerticalSpacing(3)
        task_grid.setContentsMargins(6, 4, 6, 4)
        headers = ["Task", "Vendor", "Vendor Date", "Status", "Override"]
        for col, title in enumerate(headers):
            header_label = QLabel(title)
            header_label.setStyleSheet("font-weight: bold;")
            task_grid.addWidget(header_label, 0, col)

        core_tasks = ["Prep", "Paint", "Make Ready", "Housekeeping", "Carpet Clean", "Final Walk"]
        for row, task in enumerate(core_tasks, start=1):
            label = QLabel(task)
            vendor = QComboBox(); vendor.setEditable(True)
            vendor.addItems(get_lookup_values("vendors"))
            vendor_date = QDateEdit(); vendor_date.setCalendarPopup(True)
            status = QComboBox(); status.addItems(["n/a"] + get_lookup_values("statuses"))
            override = QDateEdit(); override.setCalendarPopup(True)
            self.task_fields[task] = {
                "vendor": vendor, "vendor_date": vendor_date,
                "status": status, "override": override
            }
            task_grid.addWidget(label, row, 0)
            task_grid.addWidget(vendor, row, 1)
            task_grid.addWidget(vendor_date, row, 2)
            task_grid.addWidget(status, row, 3)
            task_grid.addWidget(override, row, 4)

        task_group.setLayout(task_grid)
        layout.addWidget(task_group)

        # --- EXTENDED TASK CHECKLIST ---
        self.optional_toggle = QCheckBox("Show Extended Task")
        self.optional_toggle.setChecked(False)
        layout.addWidget(self.optional_toggle)

        extended_group = QGroupBox("")
        extended_grid = QGridLayout()
        extended_grid.setHorizontalSpacing(10)
        extended_grid.setVerticalSpacing(3)
        extended_grid.setContentsMargins(6, 4, 6, 4)
        extended_tasks = [
            "Acid Wash", "Tub Replacement", "Cabinet & Countertop Repairs", "Doors Replacement",
            "Sheetrock Repairs", "Appliances Inspections", "Stove Clean Up",
            "Resurface", "Vinyl Replacement", "Carpet Replacement", "Duct Cleaning", "HVAC Repairs"
        ]

        for col, title in enumerate(headers):
            extended_grid.addWidget(QLabel(title), 0, col)

        for row, task in enumerate(extended_tasks, start=1):
            label = QLabel(task)
            vendor = QComboBox(); vendor.setEditable(True)
            vendor.addItems(get_lookup_values("vendors"))
            vendor_date = QDateEdit(); vendor_date.setCalendarPopup(True)
            status = QComboBox(); status.addItems(["n/a"] + get_lookup_values("statuses"))
            override = QDateEdit(); override.setCalendarPopup(True)
            self.task_fields[task] = {
                "vendor": vendor, "vendor_date": vendor_date,
                "status": status, "override": override
            }
            extended_grid.addWidget(label, row, 0)
            extended_grid.addWidget(vendor, row, 1)
            extended_grid.addWidget(vendor_date, row, 2)
            extended_grid.addWidget(status, row, 3)
            extended_grid.addWidget(override, row, 4)

        extended_group.setLayout(extended_grid)
        extended_group.setVisible(False)
        layout.addWidget(extended_group)
        self.optional_toggle.stateChanged.connect(
            lambda state: extended_group.setVisible(bool(state))
        )

        # --- COMMENTS SECTION ---
        layout.addWidget(QLabel("Comment"))
        self.comment_field = QTextEdit()
        self.comment_field.setFixedHeight(80)
        layout.addWidget(self.comment_field)

        # --- WRAP LAYOUT ---
        scroll_area.setWidget(content_widget)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # ✅ Wipe all fields on open
        self.clear_form()

    def update_task_code(self):
        property_name = self.property_field.currentText().strip()
        unit_number = self.unit_number_field.text().strip()
        if property_name and unit_number:
            code = f"{property_name[0].upper()}-{unit_number}"
            self.task_code_field.setText(code)
            if hasattr(self, "task_code_display"):
                self.task_code_display.setText(code)
        else:
            self.task_code_field.clear()
            if hasattr(self, "task_code_display"):
                self.task_code_display.setText("—")

    # ✅ Clear everything in the form
    def clear_form(self):
        self.property_field.setCurrentIndex(-1)
        self.unit_number_field.clear()
        self.move_out_date.setDate(self.move_out_date.minimumDate())
        self.move_in_date.setDate(self.move_in_date.minimumDate())
        self.condition_field.setCurrentIndex(-1)
        self.task_code_field.clear()

        for label in [
            self.dtbr_label, self.days_vacant_label, self.unit_type_label,
            self.sqft_label, self.task_code_display, self.status_label, self.nvm_label
        ]:
            label.setText("—")

        for fields in self.task_fields.values():
            fields["vendor"].setCurrentIndex(-1)
            fields["vendor_date"].setDate(fields["vendor_date"].minimumDate())
            fields["status"].setCurrentIndex(0)
            fields["override"].setDate(fields["override"].minimumDate())

        self.comment_field.clear()
