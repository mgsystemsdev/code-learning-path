# scripts/export_demo_data.py
import os
import csv
from app.db import connect

OUT = os.path.join(os.path.dirname(__file__), "..", "web_demo", "demo_data.csv")

def export(limit=1000):
    con = connect()
    cur = con.cursor()
    # Join sessions with items to pull the canonical name and type
    cur.execute("""
        SELECT s.id, s.date, i.type, i.canonical_name,
               s.status, s.hours_spent, s.notes, s.tags,
               s.difficulty, s.topic, s.points_awarded, s.progress_pct
        FROM sessions s
        JOIN items i ON s.item_id = i.id
        ORDER BY s.date DESC, s.id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    con.close()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        # Updated header row
        w.writerow([
            "ID", "Date", "Type", "Work Item",
            "Status", "Hours", "Notes", "Tags",
            "Difficulty", "Topic", "Points", "Progress %"
        ])
        for r in rows:
            # Format progress_pct as a string with a percent sign
            row = list(r)
            row[-1] = f"{row[-1]:.1f}%" if row[-1] else ""
            w.writerow(row)
    print(f"Wrote {OUT} ({len(rows)} rows)")

if __name__ == "__main__":
    export()
