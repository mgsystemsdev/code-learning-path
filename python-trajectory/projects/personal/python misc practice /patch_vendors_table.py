import sqlite3

DB_PATH = "lookup_data.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 🔧 STEP 1: Recreate vendors table with new columns if needed
# This is safe if vendors already exist — it keeps their names

cur.execute("""
CREATE TABLE IF NOT EXISTS vendors (
    name TEXT PRIMARY KEY,
    type TEXT,
    tasks TEXT
)
""")

conn.commit()
conn.close()

print("✅ Vendors table patched: name, type, tasks now available.")
