# === PySide Widgets and Dialogs ===
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QListWidget, QPushButton,
    QWidget, QLabel, QInputDialog, QMessageBox, QLineEdit, QComboBox,
    QListWidgetItem, QAbstractItemView
)

# === Import the data handlers ===
from lookup_manager import (
    get_lookup_values, add_value, edit_value, delete_value,
    add_vendor_entry, add_employee_entry  # ✅ We’ll define both
)

# === MAIN LOOKUP EDITOR CLASS ===
class LookupEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lookup Editor")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # 🧠 Define your editable tables
        self.tables = {
            "Properties": "properties",   # Single-column only
            "Vendors": "vendors",         # 3-column editor
            "Employees": "employees",     # 3-column editor
            "Statuses": "statuses"        # Single-column only
        }

        self.list_widgets = {}

        # 🔁 Build one tab per table
        for tab_name, table_name in self.tables.items():
            tab = QWidget()
            tab_layout = QVBoxLayout()
            list_widget = QListWidget()
            self.list_widgets[table_name] = list_widget

            tab_layout.addWidget(QLabel(f"{tab_name} List"))
            tab_layout.addWidget(list_widget)

            # 🔘 Add/Edit/Delete Buttons
            btn_layout = QHBoxLayout()
            add_btn = QPushButton("Add")
            edit_btn = QPushButton("Edit")
            delete_btn = QPushButton("Delete")

            add_btn.clicked.connect(lambda _, t=table_name: self.handle_add(t))
            edit_btn.clicked.connect(lambda _, t=table_name: self.handle_edit(t))
            delete_btn.clicked.connect(lambda _, t=table_name: self.handle_delete(t))

            for btn in [add_btn, edit_btn, delete_btn]:
                btn_layout.addWidget(btn)

            tab_layout.addLayout(btn_layout)
            tab.setLayout(tab_layout)
            self.tabs.addTab(tab, tab_name)

            self.refresh_list(table_name)

    # === REFRESH LIST ===
    def refresh_list(self, table_name):
        widget = self.list_widgets[table_name]
        widget.clear()
        widget.addItems(get_lookup_values(table_name))

    # === ADD HANDLER ===
    def handle_add(self, table):
        if table in ("vendors", "employees"):
            dialog = EntityFormDialog(
                entity_type=table,
                core_tasks=["Prep", "Paint", "Make Ready", "Housekeeping", "Carpet Clean", "Final Walk"],
                extended_tasks=[
                    "Acid Wash", "Tub Replacement", "Cabinet & Countertop Repairs", "Doors Replacement",
                    "Sheetrock Repairs", "Appliances Inspections", "Stove Clean Up",
                    "Resurface", "Vinyl Replacement", "Carpet Replacement", "Duct Cleaning", "HVAC Repairs"
                ],
                parent=self
            )
            if dialog.exec():
                name, type_, tasks = dialog.get_data()
                if not name or not tasks:
                    QMessageBox.warning(self, "Missing Info", "Name and at least one task required.")
                    return
                success = add_vendor_entry(name, type_, tasks) if table == "vendors" else add_employee_entry(name, type_, tasks)
                if success:
                    self.refresh_list(table)
                else:
                    QMessageBox.warning(self, "Error", f"{name} already exists or is invalid.")
        else:
            text, ok = QInputDialog.getText(self, "Add Value", "Enter new value:")
            if ok and text.strip():
                if add_value(table, text.strip()):
                    self.refresh_list(table)
                else:
                    QMessageBox.warning(self, "Error", f"{text} already exists or is invalid.")

    # === EDIT HANDLER (Basic, can improve later) ===
    def handle_edit(self, table):
        QMessageBox.information(self, "Not Yet", "Edit not supported for this entity yet.")

    # === DELETE HANDLER ===
    def handle_delete(self, table):
        widget = self.list_widgets[table]
        selected = widget.currentItem()
        if not selected:
            return
        value = selected.text()
        confirm = QMessageBox.question(
            self, "Confirm Delete", f"Are you sure you want to delete '{value}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_value(table, value)
            self.refresh_list(table)


# === UNIVERSAL ENTITY FORM (Vendor + Employee) ===
class EntityFormDialog(QDialog):
    def __init__(self, entity_type, core_tasks, extended_tasks, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add New {entity_type[:-1].capitalize()}")
        self.setMinimumWidth(400)

        self.core_tasks = core_tasks
        self.extended_tasks = extended_tasks

        layout = QVBoxLayout()

        # ✏️ Name input
        self.name_input = QLineEdit()
        layout.addWidget(QLabel(f"{entity_type[:-1].capitalize()} Name:"))
        layout.addWidget(self.name_input)

        # 🧡 Type dropdown
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["core", "optional"])
        self.type_dropdown.currentTextChanged.connect(self.update_task_list)
        layout.addWidget(QLabel("Assignment Type:"))
        layout.addWidget(self.type_dropdown)

        # ✅ Task selector
        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.task_list.setMaximumHeight(100)
        layout.addWidget(QLabel("Assign Tasks:"))
        layout.addWidget(self.task_list)

        # 📂 Save / Cancel
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.accept)

        self.update_task_list()

    def update_task_list(self):
        self.task_list.clear()
        task_set = self.core_tasks if self.type_dropdown.currentText() == "core" else self.extended_tasks
        for task in task_set:
            item = QListWidgetItem(task)
            self.task_list.addItem(item)

    def get_data(self):
        name = self.name_input.text().strip()
        type_ = self.type_dropdown.currentText()
        tasks = [item.text() for item in self.task_list.selectedItems()]
        return name, type_, tasks
