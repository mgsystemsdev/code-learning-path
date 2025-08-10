import os

# Set target location — Documents folder
BASE_DIR = os.path.expanduser("~/Documents")
project_root = os.path.join(BASE_DIR, "SimStand")

folders = [
    os.path.join(project_root, "modes"),
    os.path.join(project_root, "utils")
]

files = {
    os.path.join(project_root, "menu_bar_launcher.py"): "Mac menu bar launcher using rumps. Hooks to run mode scripts.",
    os.path.join(project_root, "modes/mode_alpha.py"): "Simulated automation mode: Alpha routine.",
    os.path.join(project_root, "modes/mode_beta.py"): "Simulated automation mode: Beta routine.",
    os.path.join(project_root, "utils/logger.py"): "Basic logger placeholder.",
    os.path.join(project_root, "README.md"): "Setup and usage for SimStand Tray app.",
    os.path.join(project_root, ".gitignore"): "Ignore logs and system cache."
}

header = '''"""
Author: Miguel A Gonzalez Amonte
Description: {desc}
"""
'''

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with header or content
for path, desc in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if path.endswith(".py"):
        with open(path, "w") as f:
            f.write(header.format(desc=desc))
    elif path.endswith(".gitignore"):
        with open(path, "w") as f:
            f.write("__pycache__/\n*.pyc\nlogs/\n")
    elif path.endswith("README.md"):
        with open(path, "w") as f:
            f.write("# SimStand Tray\n\nRun `menu_bar_launcher.py` via Platypus for macOS tray support.\n")

print(f"✅ SimStand project created at: {project_root}")
