pass



from typing import Optional

def build_task_code(property_name: str, unit_number: str) -> Optional[str]:
    """Return task code like 'P-201' or None if inputs are blank."""
    property_name = property_name.strip()
    unit_number = unit_number.strip()

    if not (property_name and unit_number):
        return None
    return f"{property_name[0].upper()}-{unit_number}"


def main() -> None:
    property_name = input("Enter property name: ").strip()
    unit_number   = input("Enter unit number: ").strip()

    code =build_task_code (property_name, unit_number)
    if code is None:
        print("❌  Both fields are required.")
    else:
        print(f"✅  Task code: {code}")

if __name__ == "__main__":
    main()

