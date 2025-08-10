import os
from pathlib import Path
import subprocess
from datetime import date

# --- Header Template ---
HEADER_TEMPLATE = """# Author: Miguel Gonzalez Almonte
# Created: 2025-07-06
# File: {filename}
# Description: {description}
"""

# --- File Structure Map ---
structure = {
    "dmrb": {
        "run.py": "App entry point",
        "main.py": "Backend boot/init logic",
        "README.md": "Project overview",
        ".gitignore": "__pycache__/\n*.pyc\n*.sqlite\n.env\nvenv/\n",

        "backend": {
            "__init__.py": "",
            "databases": {
                "__init__.py": "",
                "lookup.db": None,
                "unit_inventory.db": None,
                "lifecycle.db": None
            },
            "populators": {
                "__init__.py": "",
                "init_lookup_db.py": "Initialize lookup DB schema",
                "init_unit_db.py": "Initialize unit inventory schema",
                "init_lifecycle_db.py": "Initialize lifecycle DB schema"
            },
            "managers": {
                "__init__.py": "",
                "task_manager.py": "Manage task data logic",
                "lookup_manager.py": "Read/write from lookup DB",
                "entity_manager.py": "Manage vendors/employees/etc.",
                "unit_lifecycle_manager.py": "Handle lifecycle stage updates",
                "user_manager.py": "User role and login access",
                "report_manager.py": "Generate reports and summaries",
                "sync_manager.py": "Handle mobile sync logic"
            },
            "connectors": {
                "__init__.py": "",
                "db_connect.py": "Database connection logic"
            }
        },

        "config": {
            "__init__.py": "",
            "settings.py": "App default settings",
            "env_loader.py": "Read .env environment configs"
        },

        "utils": {
            "__init__.py": "",
            "tools.py": "Reusable helper functions",
            "extra_tools.py": "Additional shared utilities",
            "formatters.py": "Format helpers for text, date, etc."
        },

        "ui": {
            "__init__.py": "",
            "windows": {
                "__init__.py": "",
                "main_window.py": "Primary app container"
            },
            "dialogs": {
                "__init__.py": "",
                "unit_dialog.py": "Add/edit unit dialog",
                "task_dialog.py": "Add task dialog",
                "lookup_dialog.py": "Manage lookups dialog",
                "import_dialog.py": "Import Excel dialog",
                "export_dialog.py": "Export options dialog",
                "final_walk_dialog.py": "Final walk confirmation",
                "snapshot_dialog.py": "NVMS snapshot dialog",
                "delay_dialog.py": "Delayed tasks dialog",
                "report_dialog.py": "Generate report dialog",
                "settings_dialog.py": "App preferences dialog"
            },
            "components": {
                "__init__.py": "",
                "dashboard_widget.py": "Summary widget",
                "nav_button.py": "Sidebar buttons",
                "task_card.py": "Drag task cards",
                "user_avatar.py": "User icon with initials"
            },
            "screens": {
                "__init__.py": "",
                "login_screen.py": "User login interface",
                "launcher.py": "Switch login/main"
            },
            "views": {
                "__init__.py": "",
                "dashboard_view.py": "Stats + overview",
                "table_view.py": "Main grid view",
                "task_template_view.py": "Drag task template",
                "delay_view.py": "Delayed task view",
                "sync_review_view.py": "Phone sync review",
                "report_view.py": "Reports section",
                "notification_view.py": "System alerts",
                "make_ready_view.py": "Kanban board",
                "calendar_view.py": "Task calendar",
                "vendor_view.py": "Vendor assignments",
                "notes_log_view.py": "Freeform notes",
                "property_unit_view.py": "Unit/property db",
                "unit_insight_view.py": "Insights per unit",
                "user_manager_view.py": "Admin role mgmt",
                "roles": {
                    "__init__.py": "",
                    "make_ready_coordinator.py": "Coordinator view",
                    "property_manager.py": "PM view",
                    "assistant_property_manager.py": "APM view",
                    "leasing_agent_view.py": "Leasing view",
                    "make_ready_tech_view.py": "Tech view",
                    "service_tech_view.py": "Service tech view"
                }
            }
        },

        "data": {
            "sample_import.xlsx": None
        },

        "tests": {
            "__init__.py": "",
            "test_task_logic.py": "Test task logic",
            "test_units.py": "Test unit flow",
            "test_exports.py": "Test export logic",
            "test_lifecycle.py": "Test lifecycle transitions"
        }
    }
}

# --- Folder & File Creation ---
def create_structure(base_path, node):
    for name, content in node.items():
        path = base_path / name
        if isinstance(content, dict):
            path.mkdir(parents=True, exist_ok=True)
            create_structure(path, content)
        elif content is None:
            continue
        else:
            with open(path, "w", encoding="utf-8") as f:
                if name.endswith(".py"):
                    f.write(HEADER_TEMPLATE.format(filename=name, description=content))
                else:
                    f.write(content)

# --- Post Setup Steps ---
def post_setup(path):
    subprocess.run(["git", "init"], cwd=path)
    subprocess.run(["python3", "-m", "venv", "venv"], cwd=path)
    with open(path / "requirements.txt", "w") as f:
        f.write("PySide6\npandas\nopenpyxl\n")
    print("✅ Git, venv, and requirements.txt created")

# --- Execute ---
if __name__ == "__main__":
    root = Path.home() / "Documents/dmrb_scaffolded"
    create_structure(root, structure)
    post_setup(root)
    print(f"✅ Project generated at {root}")
