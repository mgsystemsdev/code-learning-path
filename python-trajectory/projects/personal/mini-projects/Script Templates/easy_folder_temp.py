import os
from pathlib import Path

def get_structure(app_name):
    return {
        app_name: {
            "run.py": "",
            "main.py": "",
            "login.py": "",
            "ui": {
                "__init__.py": "",
                "screens": {
                    "__init__.py": ""
                },
                "dialogs": {
                    "__init__.py": ""
                }
            },
            "backend": {
                "__init__.py": "",
                "launcher": {
                    "__init__.py": "",
                    "app_launcher.py": ""
                },
                "managers": {
                    "__init__.py": ""
                }
            },
            "databases": {
                "__init__.py": ""
            }
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
    app_name = input("Enter your app name (e.g. login_app): ").strip()
    if not app_name:
        print("⚠️ App name cannot be empty.")
    else:
        documents_path = Path.home() / "Documents"
        project_path = documents_path / app_name
        structure = get_structure(app_name)
        create_structure(documents_path, structure)
        print(f"\n✅ App '{app_name}' scaffolded in your Documents folder: {project_path}")
