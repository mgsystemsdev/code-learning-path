import sqlite3

DB_PATH = "lookup_data.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 🔄 DROP old vendor table if exists (to upgrade schema)
cur.execute("DROP TABLE IF EXISTS vendors")

# ✅ Recreate vendors table with name/type/tasks
cur.execute("""
CREATE TABLE vendors (
    name TEXT PRIMARY KEY,
    type TEXT,
    tasks TEXT
)
""")

# 🔄 DROP old employees table if exists
cur.execute("DROP TABLE IF EXISTS employees")

# ✅ Recreate employees table with name/type/tasks
cur.execute("""
CREATE TABLE employees (
    name TEXT PRIMARY KEY,
    type TEXT,
    tasks TEXT
)
""")

conn.commit()
conn.close()

print("✅ vendors and employees tables recreated with full schema.")
