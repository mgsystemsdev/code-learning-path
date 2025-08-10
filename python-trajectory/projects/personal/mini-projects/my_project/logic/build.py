# logic/build.py

import

from typing import Optional

def build_task_code(property_name: str, unit_number: str) -> Optional[str]:
    """Return task code like 'P-201' or None if inputs are blank."""
    property_name = property_name.strip()
    unit_number = unit_number.strip()

    if not (property_name and unit_number):
        return None
    return f"{property_name[0].upper()}-{unit_number}"
