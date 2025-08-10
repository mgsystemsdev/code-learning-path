import sqlite3

conn = sqlite3.connect("lookup_data.db")
cur = conn.cursor()

# --- Add properties table ---
cur.execute("""
CREATE TABLE IF NOT EXISTS properties (
    value TEXT PRIMARY KEY
)
""")

# --- Add statuses table ---
cur.execute("""
CREATE TABLE IF NOT EXISTS statuses (
    value TEXT PRIMARY KEY
)
""")

# Optionally pre-fill statuses (N, V, M)
cur.executemany("INSERT OR IGNORE INTO statuses (value) VALUES (?)", [
    ("N",), ("V",), ("M",)
])

conn.commit()
conn.close()

print("✅ Properties and Statuses tables are created and prefilled.")
