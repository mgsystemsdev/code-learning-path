import sqlite3

# === DATABASE PATH (local SQLite file) ===
DB_PATH = "lookup_data.db"

# === 🔎 READ values from a lookup table ===
def get_lookup_values(table_name):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Use table-appropriate field
        if table_name in ("vendors", "employees"):
            cur.execute(f"SELECT name FROM {table_name} ORDER BY name")
        else:
            cur.execute(f"SELECT value FROM {table_name} ORDER BY value")

        rows = cur.fetchall()
        conn.close()
        return [r[0] for r in rows]

    except Exception as e:
        print(f"❌ Error reading from {table_name}: {e}")
        return []

# === ✅ ADD a simple value (property, status, etc.) ===
def add_value(table, value):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(f"INSERT OR IGNORE INTO {table} (value) VALUES (?)", (value,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error adding to {table}: {e}")
        return False

# === ✏️ EDIT a simple value ===
def edit_value(table, old_value, new_value):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(f"UPDATE {table} SET value = ? WHERE value = ?", (new_value, old_value))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error editing {table}: {e}")
        return False

# === ❌ DELETE a value ===
def delete_value(table, value):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        if table in ("vendors", "employees"):
            cur.execute(f"DELETE FROM {table} WHERE name = ?", (value,))
        else:
            cur.execute(f"DELETE FROM {table} WHERE value = ?", (value,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error deleting from {table}: {e}")

# === ✅ ADD vendor using multi-field data ===
def add_vendor_entry(name, type_, task_list):
    return _add_entity("vendors", name, type_, task_list)

# === ✅ ADD employee using multi-field data ===
def add_employee_entry(name, type_, task_list):
    return _add_entity("employees", name, type_, task_list)

# === 🔁 SHARED insert logic for vendors + employees ===
def _add_entity(table, name, type_, task_list):
    try:
        tasks = ",".join(task_list)  # Convert task list into "task1,task2,task3"
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Check if name already exists (no duplicates)
        cur.execute(f"SELECT name FROM {table} WHERE name = ?", (name,))
        if cur.fetchone():
            return False

        # Insert record
        cur.execute(f"""
            INSERT INTO {table} (name, type, tasks)
            VALUES (?, ?, ?)
        """, (name, type_, tasks))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Error adding to {table}: {e}")
        return False

# === 🧠 FUTURE IDEA: Load vendors for specific task type
def get_vendors_for_task(task_type, task_name):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            SELECT name FROM vendors
            WHERE type = ? AND tasks LIKE ?
        """, (task_type, f"%{task_name}%"))

        rows = cur.fetchall()
        conn.close()
        return [r[0] for r in rows]
    except Exception as e:
        print(f"❌ Error filtering vendors: {e}")
        return []
