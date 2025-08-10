import os
from pathlib import Path

def get_structure(app_name):
    def header(filename, description):
        return f"""# Author:      Miguel Gonzalez Almonte  \
# Created:     2025-05-24  \
# File:        {filename}  \
# Description: {description}  \
\n"""

    return {
        app_name: {
            "startup.py": header("startup.py", "Starts app → login dialog → main GUI"),
            "gui_login.py": header("gui_login.py", "QDialog login (username/password)"),
            "constants.py": header("constants.py", "Paths, VALID_USERS, messages"),
            "gui_main_qt.py": header("gui_main_qt.py", "PySide6 version of main GUI"),
            "gui_main_tk.py": header("gui_main_tk.py", "Tkinter version (same flow)"),
            "launcher.py": header("launcher.py", "Launch external mode (simulated subprocess)"),
            "server_flask.py": header("server_flask.py", "Basic Flask server with /launch, /log, /export"),
            "server_fastapi.py": header("server_fastapi.py", "FastAPI version (async drill)"),
            "modes.json": "",
            "logs": {
                "launch.log": ""
            },
            "exports": {
                "modes.xlsx": ""
            },
            "utils": {
                "json_utils.py": header("json_utils.py", "Load/validate modes.json"),
                "log_utils.py": header("log_utils.py", "Logger: write/read .log file"),
                "export_utils.py": header("export_utils.py", "Excel/CSV export functions")
            },
            "broken_versions": {},
            ".gitignore": "",
            "README.md": ""
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
    app_name = input("Enter your app name (e.g. training_python_board): ").strip()
    if not app_name:
        print("⚠️ App name cannot be empty.")
    else:
        documents_path = Path.home() / "Documents" / "Manual" / "Python class"
        project_path = documents_path / app_name
        structure = get_structure(app_name)
        create_structure(documents_path, structure)
        print(f"\n✅ App '{app_name}' scaffolded in your Documents folder: {project_path}")
