# dmrb_project_generator.py
# Author: Miguel Gonzalez Almonte
# Created: 2025-07-06
# Description: Full generator script for the DMRB folder + file structure, headers, git, venv, requirements, and empty database shell

import os
from pathlib import Path
import subprocess
from datetime import date

AUTHOR = "Miguel Gonzalez Almonte"
TODAY = date.today().isoformat()

HEADER_TEMPLATE = """# Author: {author}
# Created: {created}
# File: {filename}
# Description: {description}
"""

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def add_header(path, description=""):
    header = HEADER_TEMPLATE.format(author=AUTHOR, created=TODAY, filename=path.name, description=description)
    write_file(path, header)

def make_init(folder):
    init_path = folder / "__init__.py"
    if not init_path.exists():
        write_file(init_path, "")

def make_folders_and_files(base_path, structure):
    for name, content in structure.items():
        current = base_path / name
        if isinstance(content, dict):
            current.mkdir(parents=True, exist_ok=True)
            make_init(current)
            make_folders_and_files(current, content)
        else:
            add_header(current, content)

def initialize_git(project_path):
    subprocess.run(["git", "init"], cwd=project_path)
    write_file(project_path / ".gitignore", "__pycache__/\n*.pyc\n*.sqlite\n.env\nvenv/\n")
    print("✅ Git initialized")

def create_venv(project_path):
    subprocess.run(["python3", "-m", "venv", "venv"], cwd=project_path)
    print("✅ Virtual environment created")

def generate_requirements(project_path):
    reqs = "PySide6\npandas\nopenpyxl\n"
    write_file(project_path / "requirements.txt", reqs)
    print("✅ requirements.txt created")

def run_seed_scripts(project_path):
    scripts = ["init_lookup_db.py", "init_unit_db.py", "init_lifecycle_db.py"]
    for script in scripts:
        script_path = project_path / "backend" / "populators" / script
        if script_path.exists():
            subprocess.run(["python3", script_path])
    print("✅ Seed scripts executed (if present)")

# Define folder/file structure with headers
PROJECT_STRUCTURE = {
    "dmrb": {
        "run.py": "Entry point to start the app",
        "main.py": "Boot + init logic",
        "README.md": "DMRB Overview",
        "backend": {
            "__init__.py": "",
            "databases": {
                "__init__.py": "",
                "lookup.db": "Empty lookup DB",
                "unit_inventory.db": "Empty inventory DB",
                "lifecycle.db": "Empty lifecycle DB"
            },
            "populators": {
                "__init__.py": "",
                "init_lookup_db.py": "Create empty lookup.db schema",
                "init_unit_db.py": "Create empty unit_inventory.db schema",
                "init_lifecycle_db.py": "Create empty lifecycle.db schema"
            },
            "managers": {
                "__init__.py": "",
                "task_manager.py": "Handle task logic",
                "lookup_manager.py": "Handle lookups",
                "entity_manager.py": "Generic entities",
                "unit_lifecycle_manager.py": "Track units in lifecycle",
                "user_manager.py": "Role + auth logic",
                "report_manager.py": "Export reporting",
                "sync_manager.py": "Offline sync logic"
            },
            "connectors": {
                "__init__.py": "",
                "db_connect.py": "Connect to SQLite"
            }
        },
        "config": {
            "__init__.py": "",
            "settings.py": "Default config",
            "env_loader.py": "Read .env vars"
        },
        "utils": {
            "__init__.py": "",
            "tools.py": "Common functions",
            "extra_tools.py": "Additional helpers",
            "meta_tools.py": "Shared advanced logic"
        },
        "data": {
            "sample_import.xlsx": "Sample import file"
        },
        "tests": {
            "__init__.py": "",
            "test_task_logic.py": "Task tests",
            "test_units.py": "Unit tests",
            "test_exports.py": "Export tests",
            "test_lifecycle.py": "Lifecycle flow tests"
        },
        "ui": {
            "__init__.py": ""  # UI scaffolded elsewhere
        }
    }
}

if __name__ == "__main__":
    base_path = Path.home() / "Documents"
    project_path = base_path / "dmrb_scaffolded"
    
    project_path.mkdir(parents=True, exist_ok=True)
    make_folders_and_files(project_path, PROJECT_STRUCTURE)
    initialize_git(project_path)
    create_venv(project_path)
    generate_requirements(project_path)
    run_seed_scripts(project_path)
    print(f"\n✅ DMRB fully scaffolded at {project_path}")
