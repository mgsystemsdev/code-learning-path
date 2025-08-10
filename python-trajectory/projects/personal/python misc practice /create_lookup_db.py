import sqlite3

# Connect (creates file if not exist)
conn = sqlite3.connect("lookup_data.db")
cur = conn.cursor()

# --- Create Vendors Table ---
cur.execute("""
CREATE TABLE IF NOT EXISTS vendors (
    value TEXT PRIMARY KEY
)
""")
cur.executemany("INSERT OR IGNORE INTO vendors (value) VALUES (?)", [
    ("RR Paint",), ("Angel Clean",), ("Lo Painting",)
])

# --- Create Employees Table ---
cur.execute("""
CREATE TABLE IF NOT EXISTS employees (
    value TEXT PRIMARY KEY
)
""")
cur.executemany("INSERT OR IGNORE INTO employees (value) VALUES (?)", [
    ("Jose M.",), ("Rosa V.",), ("Anthony R.",)
])

conn.commit()
conn.close()

print("✅ lookup_data.db is ready with vendors and employees.")
