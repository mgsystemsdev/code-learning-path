# Author:      Miguel Gonzalez Almonte  
# Created:     2025-05-24  
# File:        log_utils.py  
# Description: Logger: write/read .log file  

import os
import json
from datetime import datetime

class Logger:
    def __init__(self, file_path):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def write(self, mode_name, user):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode_name,
            "user": user
        }

        logs = self.read()
        logs.append(entry)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)

    def read(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

