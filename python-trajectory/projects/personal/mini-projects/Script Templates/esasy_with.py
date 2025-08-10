import os
from pathlib import Path

def get_structure(app_name):
    return {
        app_name: {
            "run.py": """# Author:      Miguel Gonzalez Almonte  \n# Created:     2025-05-24  \n# File:        main.py  \n# Description: run the start of the system\n\nimport sys\nfrom PySide6.QtWidgets import QApplication\nfrom backend.launcher.app_launcher import launch_app\n\ndef main():\n    app = QApplication(sys.argv)\n    launch_app(app)\n    sys.exit()\n\nif __name__ == \"__main__\":\n    main()\n""",
            "main.py": """# Author:      Miguel Gonzalez Almonte  \n# Created:     2025-05-24  \n# File:        main.py  \n# Description: Main application window shell; blank with CLPMG title\n\nfrom PySide6.QtWidgets import QMainWindow\n\nclass MainAppWindow(QMainWindow):\n    def __init__(self, parent=None):\n        super().__init__(parent)\n        self.setWindowTitle(\"Empty\")\n""",
            "login.py": """# Author:      Miguel Gonzalez Almonte  \n# Created:     2025-05-24  \n# File:        main.py  \n# Description: \n\nfrom PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton\n\nclass LoginDialog(QDialog):\n    def __init__(self, parent=None):\n        super().__init__(parent)\n        self.setWindowTitle(\"Empty\")\n        layout = QVBoxLayout()\n\n        btn1 = QPushButton(\"Empty\")\n        btn1.clicked.connect(self.accept)\n        layout.addWidget(btn1)\n\n        btn2 = QPushButton(\"Empty\")\n        btn2.clicked.connect(self.reject)\n        layout.addWidget(btn2)\n\n        self.setLayout(layout)\n""",
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
                    "app_launcher.py": """# Author:      Miguel Gonzalez Almonte  \n# Created:     2025-05-24  \n# File:        main.py  \n# Description: control\n\nfrom login import LoginDialog\nfrom main import MainAppWindow\n\n_main_window_ref = None\n\ndef launch_app(app):\n    global _main_window_ref\n    login = LoginDialog()\n    result = login.exec()\n    if result == LoginDialog.Accepted:\n        _main_window_ref = MainAppWindow()\n        _main_window_ref.show()\n        app.exec()\n"""
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
