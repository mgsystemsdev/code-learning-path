import os

# Project folder structure
folders = [
    "watcher",
    "router",
    "ui",
    "utils",
    "config",
    "logs"
]

files_with_descriptions = {
    "main.py": "Entry point. Loads contexts, runs initial catch-up scan, and starts folder watcher.",
    "watcher/file_watcher.py": "Watches folders using watchdog and triggers the routing engine.",
    "watcher/context_loader.py": "Loads folder contexts from contexts.yaml.",
    "router/routing_engine.py": "Main router logic. Orchestrates routing via matcher, extractor, and folder handler.",
    "router/rule_matcher.py": "Matches files against known routing rules.",
    "router/noun_extractor.py": "Extracts key nouns from filenames for routing logic.",
    "router/folder_handler.py": "Decides if folders are exploded or moved whole, and does the moving.",
    "router/title_cleaner.py": "Cleans up file and folder titles before final routing.",
    "ui/log_viewer.py": "PySide6 GUI: log viewer with table and notifications.",
    "utils/logger.py": "Central logger. Handles console, file, and in-memory buffer.",
    "utils/processed_tracker.py": "Tracks processed files to prevent re-routing.",
    "config/contexts.yaml": "",
    "config/routing_rules.json": "",
    "config/disallowed_folders.json": "",
    "logs/system.log": ""
}

header_template = '''"""
Author: Miguel A Gonzalez Amonte
Description: {desc}
"""
'''

# Create folders and files
for folder in folders:
    os.makedirs(f"project_root/{folder}", exist_ok=True)

for filepath, desc in files_with_descriptions.items():
    full_path = f"project_root/{filepath}"
    if not filepath.endswith('.py'):
        open(full_path, 'a').close()  # Create empty config/log files
    else:
        with open(full_path, 'w') as f:
            f.write(header_template.format(desc=desc))
