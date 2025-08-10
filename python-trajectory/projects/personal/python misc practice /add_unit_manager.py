import json
import os
from datetime import datetime

DATA_FILE = "temp_units.json"  # Temporary file-based "DB"

class AddUnitManager:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump([], f)

    def load_all_units(self):
        with open(self.data_file, "r") as f:
            return json.load(f)

    def is_duplicate(self, property_name, unit_number):
        units = self.load_all_units()
        return any(
            u["property"] == property_name and u["unit"] == unit_number
            for u in units
        )

    def fetch_unit_by_id(self, unit_id):
        units = self.load_all_units()
        return next((u for u in units if u["unit_id"] == unit_id), None)

    def save_unit(self, unit_payload: dict):
        units = self.load_all_units()
        units.append(unit_payload)
        with open(self.data_file, "w") as f:
            json.dump(units, f, indent=2)

    def build_unit_payload(self, form_fields: dict):
        return {
            "property": form_fields["property"],
            "unit": form_fields["unit"],
            "move_out": form_fields["move_out"],
            "move_in": form_fields["move_in"],
            "status": form_fields["status"],
            "unit_id": form_fields["unit_id"],
            "comment": form_fields.get("comment", ""),
            "created_at": datetime.now().isoformat()
        }
