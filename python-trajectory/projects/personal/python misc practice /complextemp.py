import os

def get_structure(app_name):
    return {
        app_name: {
            "config": {
                "settings.py": "# Constants and paths\n",
                "themes.py": "# Theme switcher and QSS logic\n",
            },
            "ui": {
                "__init__.py": "",
                "screens": {
                    "login.py": "# Login screen UI\n",
                    "dashboard.py": "# Main window with tabbed views\n",
                    "settings.py": "# User-configurable preferences\n",
                },
                "widgets": {
                    "sidebar.py": "# Navigation component\n",
                    "input_group.py": "# Reusable field group\n",
                }
            },
            "backend": {
                "__init__.py": "",
                "auth_manager.py": "# Login and session logic\n",
                "settings_manager.py": "# Read/write user preferences\n",
                "dashboard_logic.py": "# Data flow for dashboard\n",
                "signal_bus.py": "# Application-wide signals\n",
            },
            "data": {
                "__init__.py": "",
                "encryption.py": "# Encrypt/decrypt with Fernet\n",
                "file_store.py": "# Safe file I/O\n",
                "schema.py": "# Data validation and default structure\n",
            },
            "assets": {
                "logo.png": "",
                "styles.qss": "# Default styling rules\n",
            },
            "tests": {
                "test_auth.py": "# Test login/session flow\n",
                "test_dashboard.py": "# Test dashboard logic\n",
            },
            "run.py": "# App entry point\n",
            "main.py": "# App controller and screen switching\n",
            "README.md": f"# {app_name.capitalize()}\n\nComplex, modular PySide6 app.\n"
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
        print("⚠️ App name cannot be empty.")
    else:
        structure = get_structure(app_name)
        create_structure(os.getcwd(), structure)
        print(f"\n✅ Complex app '{app_name}' scaffolded successfully.")
