# Author:      Miguel Gonzalez Almonte  
# Created:     2025-05-24  
# File:        export_utils.py  
# Description: Excel/CSV export functions  

import json
import csv
import os
from openpyxl import Workbook

class Exporter:
    def __init__(self, log_path, export_dir="exports"):
        self.log_path = log_path
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)

    def read_logs(self):
        if not os.path.exists(self.log_path):
            return []
        with open(self.log_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def to_csv(self, filename="modes.csv"):
        logs = self.read_logs()
        path = os.path.join(self.export_dir, filename)

        with open(path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "mode", "user"])
            writer.writeheader()
            writer.writerows(logs)

    def to_excel(self, filename="modes.xlsx"):
        logs = self.read_logs()
        path = os.path.join(self.export_dir, filename)

        wb = Workbook()
        ws = wb.active
        ws.append(["Timestamp", "Mode", "User"])

        for entry in logs:
            ws.append([entry["timestamp"], entry["mode"], entry["user"]])

        wb.save(path)
