# Author:      Miguel Gonzalez Almonte  # Created:     2025-05-24  # File:        log_utils.py  # Description: Appends to logs  
# log_utils.py
# Appends to logs/launch.log

from datetime import datetime
import os

LOG_FILE = os.path.join("logs", "launch.log")

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
