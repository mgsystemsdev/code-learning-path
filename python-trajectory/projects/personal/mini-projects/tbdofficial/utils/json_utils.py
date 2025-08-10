# Author:      Miguel Gonzalez Almonte  # Created:     2025-05-24  # File:        json_utils.py  # Description: Safe JSON load/save  
# log_utils.py
# Appends to logs/launch.log

# json_utils.py
# Safe JSON load/save

import json
from typing import Any

def load_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

