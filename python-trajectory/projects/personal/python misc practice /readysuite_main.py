### STEP: Import system + PySide core
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout,
    QListWidget, QLabel, QToolBar, QPushButton
)
from PySide6.QtCore import Qt

### STEP: Import Dialogs
# ✅ Connects the Add Unit popup
from unit_form_dialog import UnitFormDialog

# ✅ Connects the Lookup Editor popup
# 🧠 This allows user to manage vendors, employees, etc.
from lookup_editor_dialog import LookupEditorDialog


### STEP: Main Window Class
class ReadySuiteMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReadySuite")
        self.setMinimumSize(1000, 600)

        self.setup_ui()  # Build the layout

    ### STEP: Setup all layout + toolbar
    def setup_ui(self):
        splitter = QSplitter(Qt.Horizontal)

        # 🧱 Sidebar — for list of units (placeholder for now)
        self.sidebar = QListWidget()
        self.sidebar.setMinimumWidth(200)

        # 🧱 Detail area — will hold the right-side views later
        self.detail = QWidget()

        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.detail)
        splitter.setStretchFactor(1, 1)

        # ✅ Toolbar with buttons
        toolbar = QToolBar("Main Toolbar")

        # ✅ Add Unit button — opens form dialog
        add_button = QPushButton("Add Unit")
        add_button.clicked.connect(self.open_add_unit_form)
        toolbar.addWidget(add_button)

        # ✅ Lookup Editor button — opens lookup manager
        # 🔁 This connects to your dialog with tabs for vendors, employees, etc.
        lookup_button = QPushButton("⚙️ Manage Lookups")
        lookup_button.clicked.connect(self.open_lookup_editor)
        toolbar.addWidget(lookup_button)

        self.addToolBar(toolbar)

        # 🧱 Main layout setup
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        container.setLayout(layout)
        self.setCentralWidget(container)

    ### STEP: Open the UnitFormDialog popup
    def open_add_unit_form(self):
        dialog = UnitFormDialog(self)
        dialog.exec()

    ### STEP: Open the LookupEditorDialog popup
    # ✅ This method connects the Manage Lookups button to open your new dialog
    def open_lookup_editor(self):
        dialog = LookupEditorDialog(self)
        dialog.exec()


### STEP: Run the App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReadySuiteMain()
    window.show()
    sys.exit(app.exec())
