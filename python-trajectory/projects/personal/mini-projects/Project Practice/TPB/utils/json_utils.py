# Author:      Miguel Gonzalez Almonte  
# Created:     2025-05-24  
# File:        json_utils.py  
# Description: Load/validate modes.json  

import json
import os

class ModeLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        if not os.path.exists(self.file_path):
            print(f"❌ File not found: {self.file_path}")
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return self.validate(data)
        except Exception as e:
            print(f"❌ Failed to load JSON: {e}")
            return []

    def validate(self, data):
        if not isinstance(data, list):
            print("❌ Invalid JSON format: expected a list.")
            return []
        if not all(isinstance(item, str) for item in data):
            print("❌ All items in modes.json must be strings.")
            return []
        return data

