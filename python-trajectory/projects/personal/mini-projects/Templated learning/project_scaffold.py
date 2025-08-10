


import os       
from pathlib import Path

target_path = Path.home() / "Documents" / "Python class"



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

def created_structure(base_path, node):
    for name, content in node.items():
        Path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(Path, exist_ok=True)
            created_structure(Path, content)
        else:
            os.makedirs(base_path, exist_ok=True)
            with open(Path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    app_name = input("📝 Enter your app name (e.g. artisan_app): ").strip()

    if not app_name:
        print("⚠️ App name cannot be empty.")
    else:
        project_path = target_path / app_name
        structure = get_structure(app_name)
        created_structure(target_path, structure)


        print(f" \n project' {app_name}' scaffolded at:{project_path}")
        print(f"All files placed inside:{target_path}")


   