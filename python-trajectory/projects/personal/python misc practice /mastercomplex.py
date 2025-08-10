import os

def get_structure(app_name, mode):
    beginner = mode == "beginner"

    return {
        app_name: {
            "config": {
                "settings.py": "# Constants and paths\n",
                "themes.py": "# Theme switcher and QSS logic\n",
            },
            "ui": {
                "__init__.py": "",
                ("pages" if beginner else "screens"): {
                    "login.py": "# Login screen UI\n",
                    "dashboard.py": "# Main window with tabbed views\n",
                    "settings.py": "# User-configurable preferences\n",
                },
                ("components" if beginner else "widgets"): {
                    "sidebar.py": "# Navigation component\n",
                    "input_group.py": "# Reusable field group\n",
                }
            },
            ("logic" if beginner else "backend"): {
                "__init__.py": "",
                "auth_manager.py": "# Login and session logic\n",
                "settings_manager.py": "# Read/write user preferences\n",
                "dashboard_logic.py": "# Data flow for dashboard\n",
                ("events.py" if beginner else "signal_bus.py"): "# Application-wide signals\n",
            },
            "data": {
                "__init__.py": "",
                "encryption.py": "# Encrypt/decrypt with Fernet\n",
                ("file_manager.py" if beginner else "file_store.py"): "# Safe file I/O\n",
                ("data_model.py" if beginner else "schema.py"): "# Data validation and default structure\n",
            },
            "assets": {
                "logo.png": "",
                "styles.qss": "# Default styling rules\n",
            },
            "tests": {
                "test_auth.py": "# Test login/session flow\n",
                "test_dashboard.py": "# Test dashboard logic\n",
            },
            ("start.py" if beginner else "run.py"): "# App entry point\n",
            "main.py": "# App controller and screen switching\n",
            "README.md": f"# {app_name.capitalize()}\n\nModular PySide6 app scaffold.\n"
        }
    }

def create_structure(base_path, node):
    for name, content in node.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            os.makedirs(base_path, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    app_name = input("Enter your app name (e.g. dashboard_app): ").strip()
    if not app_name:
        print("\u26a0\ufe0f App name cannot be empty.")
    else:
        mode = input("Choose naming style (beginner/advanced): ").strip().lower()
        if mode not in ("beginner", "advanced"):
            print("\u26a0\ufe0f Invalid mode. Please choose 'beginner' or 'advanced'.")
        else:
            structure = get_structure(app_name, mode)
            create_structure(os.getcwd(), structure)
            print(f"\n\u2705 App '{app_name}' scaffolded successfully with '{mode}' naming style.")
