
import sys, sqlite3, os
from pathlib import Path

# Import the same module your app uses
try:
    from app import db as DB
except Exception:
    import db as DB

print("db.py loaded from:", DB.__file__)
print("DB_PATH:", DB.DB_PATH)

db_path = Path(DB.DB_PATH)
print("DB exists:", db_path.exists(), "size:", db_path.stat().st_size if db_path.exists() else "n/a")

# List any similarly named DBs nearby
root = db_path.parent
candidates = list(root.glob("learning_tracker.db*"))
print("Sibling DB files:", [p.name for p in candidates])

# Show sessions schema
con = sqlite3.connect(str(DB.DB_PATH))
cur = con.cursor()
try:
    cur.execute("PRAGMA table_info(sessions)")
    cols = cur.fetchall()
    print("sessions columns:", [c[1] for c in cols])
except Exception as e:
    print("PRAGMA error:", e)
finally:
    con.close()
