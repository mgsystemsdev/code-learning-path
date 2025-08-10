# filepaths.py
# Central paths for logs and config

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FILE = BASE_DIR / "logs" / "launch.log"
MODES_FILE = BASE_DIR / "system" / "modes.json"
EXPORTS_DIR = BASE_DIR / "exports"
DEMOS_QT_DIR = BASE_DIR / "gui_qt" / "demos"
DEMOS_TK_DIR = BASE_DIR / "gui_tk" / "demos"
