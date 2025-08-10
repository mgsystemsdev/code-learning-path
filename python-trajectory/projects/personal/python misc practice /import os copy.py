import os
from pathlib import Path

def get_structure(app_name):
    def header(filename, description):
        return f"""# Author:      Miguel Gonzalez Almonte  \\
# Created:     2025-05-24  \\
# File:        {filename}  \\
# Description: {description}  \\
\n"""

    return {
        app_name: {
            "run.py": header("run.py", "Launches QApplication and login dialog"),
            "system": {
                "launcher.py": header("launcher.py", "Handles CLI or prelaunch flags"),
                "startup.py": header("startup.py", "Reads launch_target and dispatches GUI"),
                "login_dialog.py": header("login_dialog.py", "Three-stage unified QDialog"),
                "constants.py": header("constants.py", "Shared enums and UI strings"),
                "modes.json": '{\n  "launch_target": "qt",\n  "api_mode": "none"\n}\n'
            },
            "gui_qt": {
                "gui_main_qt.py": header("gui_main_qt.py", "Main PySide6 GUI showcase window")
            },
            "gui_tk": {
                "gui_main_tk.py": header("gui_main_tk.py", "Main Tkinter GUI showcase window")
            },
            "utils": {
                "json_utils.py": header("json_utils.py", "Helpers to load/save JSON safely"),
                "log_utils.py": header("log_utils.py", "Appends to launch.log"),
                "export_utils.py": header("export_utils.py", "Exports to CSV/XLSX (optional)")
            },
            "backend": {
                "server_flask.py": header("server_flask.py", "Flask backend server"),
                "server_fastapi.py": header("server_fastapi.py", "FastAPI version with Swagger")
            },
            "logs": {
                "launch.log": ""
            },
            "exports": {
                "modes.xlsx": ""
            },
            "broken_versions": {},
            "docs": {
                "README.md": "# Training Python Board\n\nWelcome to your training simulator board!\n"
            },
            ".gitignore": (
                "__pycache__/\n*.py[cod]\n*.pyo\nlogs/*\n!logs/.keep\nexports/*\n!exports/.keep\n"
                ".env\n.vscode/\n.idea/\n.DS_Store\nThumbs.db\n*.sqlite3\n*.egg-info/\n.eggs/\nbuild/\ndist/\n*.ui.py\n"
            )
        }
    }

def create_structure(base_path, node):
    for name, content in node.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    app_name = input("Enter your app name (e.g. training_python_board): ").strip()
    if not app_name:
        print("⚠️ App name cannot be empty.")
    else:
        documents_path = Path.home() / "Documents" / "Python class"
        project_path = documents_path / app_name
        structure = get_structure(app_name)
        create_structure(documents_path, structure)
        print(f"\n✅ Project '{app_name}' scaffolded in: {project_path}")
