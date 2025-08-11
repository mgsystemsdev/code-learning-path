# scripts/export_demo_data.py
import os
import csv
from app.db import connect

OUT = os.path.join(os.path.dirname(__file__), "..", "web_demo", "demo_data.csv")

def export(limit=1000):
    con = connect()
    cur = con.cursor()
    cur.execute("""
        SELECT id, date, type, exercise_name, project_name, activity_name,
               description, lifecycle, hours_spent, tags, difficulty, domain,
               points_awarded, project_progress_pct
        FROM sessions
        ORDER BY date DESC, id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    con.close()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "ID","Date","Type","Exercise Name","Project Name","Activity Name",
            "Notes","Status","Hours","Tags","Difficulty","Topic",
            "Points","Progress %"
        ])
        for r in rows:
            w.writerow(r)
    print(f"Wrote {OUT} ({len(rows)} rows)")

if __name__ == "__main__":
    export()
