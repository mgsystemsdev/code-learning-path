# app/db.py
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "learning_tracker.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    con = connect()
    cur = con.cursor()

    # Lookups
    cur.execute("""CREATE TABLE IF NOT EXISTS difficulty(
        name TEXT PRIMARY KEY,
        weight REAL NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS lifecycle(
        name TEXT PRIMARY KEY,
        multiplier REAL NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS domain(
        name TEXT PRIMARY KEY,
        parent_domain TEXT,
        color_hex TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS projects(
        name TEXT PRIMARY KEY,
        target_hours REAL NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS exercises(
        name TEXT PRIMARY KEY,
        default_difficulty TEXT,
        default_domain TEXT,
        keywords_json TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS activities(
        name TEXT PRIMARY KEY,
        default_difficulty TEXT,
        default_domain TEXT,
        keywords_json TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    # Sessions (MVP)
    cur.execute("""CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        type TEXT NOT NULL CHECK (type IN ('Exercise','Project')),
        exercise_name TEXT,
        project_name TEXT,
        activity_name TEXT,
        description TEXT,
        lifecycle TEXT,
        hours_spent REAL NOT NULL CHECK (hours_spent >= 0),
        tags TEXT,
        difficulty TEXT,
        domain TEXT,
        points_awarded REAL,
        project_progress_pct REAL
    )""")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sessions_type ON sessions(type)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project_name)")

    # Seeder (idempotent)
    def seed(table, rows, key="name"):
        for r in rows:
            cur.execute(f"SELECT 1 FROM {table} WHERE {key}=?", (r[0],))
            if cur.fetchone() is None:
                placeholders = ",".join("?"*len(r))
                cur.execute(f"INSERT INTO {table} VALUES({placeholders})", r)

    now = datetime.utcnow().isoformat()
    seed("difficulty", [
        ("Beginner", 1.0, 1, now),
        ("Intermediate", 2.0, 1, now),
        ("Advanced", 3.0, 1, now),
    ])
    seed("lifecycle", [
        ("Planned", 0.0, 1, now),
        ("In Progress", 0.8, 1, now),
        ("Blocked", 0.25, 1, now),
        ("Done", 1.0, 1, now),
        ("Reviewed", 1.1, 1, now),
    ])
    seed("domain", [
        ("Python Basics", None, "#4e79a7", 1, now),
        ("APIs", None, "#f28e2b", 1, now),
        ("Data", None, "#e15759", 1, now),
        ("ML", None, "#76b7b2", 1, now),
        ("DevOps", None, "#59a14f", 1, now),
        ("Security", None, "#edc948", 1, now),
        ("Cloud", None, "#b07aa1", 1, now),
        ("DB/SQL", None, "#ff9da7", 1, now),
        ("Frontend", None, "#9c755f", 1, now),
    ])
    seed("projects", [
        ("Web Scraper + Dashboard", 55.0, 1, now),
        ("API Backend with Authentication", 55.0, 1, now),
        ("Data Analysis with Visual Insights", 55.0, 1, now),
        ("AI-Driven Compliance & Audit Automation Platform", 55.0, 1, now),
        ("Cross-Department Predictive Resource Optimization System", 55.0, 1, now),
        ("Decentralized, AI-Enhanced Supply Chain Visibility Network", 55.0, 1, now),
    ])
    seed("exercises", [
        ("Python Variables", "Beginner", "Python Basics", None, 1, now),
        ("API Basics", "Intermediate", "APIs", None, 1, now),
        ("JWT Auth", "Advanced", "Security", None, 1, now),
        ("Pandas Joins", "Intermediate", "Data", None, 1, now),
        ("Docker Basics", "Intermediate", "DevOps", None, 1, now),
    ])
    seed("activities", [
        ("Refactor", "Intermediate", "DevOps", None, 1, now),
        ("Fix API", "Advanced", "APIs", None, 1, now),
        ("Write Tests", "Intermediate", "DevOps", None, 1, now),
        ("Add Auth", "Advanced", "Security", None, 1, now),
        ("ETL Step", "Intermediate", "Data", None, 1, now),
        ("Deploy", "Advanced", "DevOps", None, 1, now),
        ("Dashboard View", "Intermediate", "Frontend", None, 1, now),
    ])

    con.commit()
    con.close()

def fetch_lookup(table):
    con = connect()
    cur = con.cursor()
    cur.execute(f"SELECT name FROM {table} WHERE is_active=1 ORDER BY name")
    items = [r[0] for r in cur.fetchall()]
    con.close()
    return items

def get_weights():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT name, weight FROM difficulty")
    diff = dict(cur.fetchall())
    cur.execute("SELECT name, multiplier FROM lifecycle")
    life = dict(cur.fetchall())
    con.close()
    return diff, life

def project_target_hours(project_name):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT target_hours FROM projects WHERE name=?", (project_name,))
    row = cur.fetchone()
    con.close()
    return float(row[0]) if row else 0.0

def project_logged_hours(project_name):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT IFNULL(SUM(hours_spent),0) FROM sessions WHERE project_name=?", (project_name,))
    row = cur.fetchone()
    con.close()
    return float(row[0] or 0.0)

def insert_or_update_session(row):
    """
    row keys:
    date,type,exercise_name,project_name,activity_name,description,lifecycle,
    hours_spent,tags,difficulty,domain,points_awarded,project_progress_pct
    + optional id for update
    """
    con = connect()
    cur = con.cursor()
    cols = ["date","type","exercise_name","project_name","activity_name","description","lifecycle",
            "hours_spent","tags","difficulty","domain","points_awarded","project_progress_pct"]
    vals = [row.get(c) for c in cols]
    if row.get("id"):
        sets = ",".join([f"{c}=?" for c in cols])
        cur.execute(f"UPDATE sessions SET {sets} WHERE id=?", (*vals, row["id"]))
        sid = row["id"]
    else:
        placeholders = ",".join(["?"]*len(cols))
        cur.execute(f"INSERT INTO sessions({','.join(cols)}) VALUES({placeholders})", vals)
        sid = cur.lastrowid
    con.commit()

    # Recompute and store project progress if a project name is provided
    project_name = row.get("project_name")
    if project_name:
        cur.execute("SELECT target_hours FROM projects WHERE name=?", (project_name,))
        tgt_row = cur.fetchone()
        target = float(tgt_row[0]) if tgt_row else 0.0

        cur.execute(
            "SELECT IFNULL(SUM(hours_spent),0) FROM sessions WHERE project_name=?",
            (project_name,),
        )
        logged_row = cur.fetchone()
        logged = float(logged_row[0] or 0.0)

        progress = min(100.0, (logged / target) * 100.0) if target > 0 else 0.0
        cur.execute(
            "UPDATE sessions SET project_progress_pct=? WHERE id=?",
            (progress, sid),
        )
        con.commit()

    con.close()
    return sid

def list_sessions(limit=200):
    con = connect()
    cur = con.cursor()
    cur.execute("""SELECT id,date,type,exercise_name,project_name,activity_name,description,lifecycle,
                   hours_spent,tags,difficulty,domain,points_awarded,project_progress_pct
                   FROM sessions ORDER BY date DESC, id DESC LIMIT ?""", (limit,))
    rows = cur.fetchall()
    con.close()
    return rows
