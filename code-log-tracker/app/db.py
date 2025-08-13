# app/db.py
import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

DB_PATH = Path(__file__).resolve().parent.parent / "learning_tracker.db"
RULES_PATH = Path(__file__).resolve().parent.parent / "rules"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug"""
    # Normalize: lowercase, basic synonyms
    text = text.lower().strip()
    synonyms = {
        'auth': 'authentication',
        'jwt': 'json-web-token',
        'api': 'application-programming-interface',
        'ui': 'user-interface',
        'db': 'database'
    }
    
    for short, full in synonyms.items():
        text = text.replace(short, full)
    
    # Remove special chars, convert spaces to hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def init_db():
    con = connect()
    cur = con.cursor()

    # Global configuration
    cur.execute("""CREATE TABLE IF NOT EXISTS config(
        key TEXT PRIMARY KEY,
        value_json TEXT NOT NULL,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    # Languages (programming languages/technologies)
    cur.execute("""CREATE TABLE IF NOT EXISTS languages(
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        color_hex TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    # Items (stable work items - exercises/projects)
    cur.execute("""CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language_code TEXT NOT NULL,
        type TEXT NOT NULL CHECK (type IN ('Exercise','Project')),
        canonical_name TEXT NOT NULL,
        slug TEXT NOT NULL,
        aliases_json TEXT DEFAULT '[]',
        default_difficulty TEXT,
        default_topic TEXT,
        target_hours REAL DEFAULT 0,
        total_logs INTEGER DEFAULT 0,
        total_hours REAL DEFAULT 0,
        last_logged_at TEXT,
        current_streak_days INTEGER DEFAULT 0,
        longest_streak_days INTEGER DEFAULT 0,
        projected_finish_date TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(language_code, type, slug),
        FOREIGN KEY(language_code) REFERENCES languages(code)
    )""")

    # Sessions (individual log entries)
    cur.execute("""CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT DEFAULT 'In Progress',
        hours_spent REAL NOT NULL CHECK (hours_spent >= 0),
        notes TEXT,
        tags TEXT,
        difficulty TEXT,
        topic TEXT,
        points_awarded REAL DEFAULT 0,
        progress_pct REAL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(item_id) REFERENCES items(id)
    )""")

    # Create indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_items_language_type ON items(language_code, type)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_items_slug ON items(slug)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sessions_item ON sessions(item_id)")

    # Seed initial data
    now = datetime.utcnow().isoformat()
    
    # Default configuration
    default_config = {
        'difficulty_weights': {
            'Beginner': 1.0,
            'Intermediate': 1.5,
            'Advanced': 2.0,
            'Expert': 2.5
        },
        'status_multipliers': {
            'Planned': 1.0,
            'In Progress': 1.1,
            'Completed': 1.2,
            'Blocked': 0.8
        },
        'ui_limits': {
            'max_hours_per_session': 24,
            'hours_increment': 0.25
        }
    }
    
    cur.execute("SELECT 1 FROM config WHERE key='global'")
    if not cur.fetchone():
        cur.execute("INSERT INTO config (key, value_json) VALUES (?, ?)", 
                   ('global', json.dumps(default_config)))

    # Default languages
    languages = [
        ('python', 'Python', '#3776ab'),
        ('javascript', 'JavaScript', '#f7df1e'),
        ('html', 'HTML/CSS', '#e34f26'),
        ('sql', 'SQL', '#336791'),
        ('git', 'Git/DevOps', '#f05032'),
        ('general', 'General/Theory', '#6c757d')
    ]
    
    for code, name, color in languages:
        cur.execute("SELECT 1 FROM languages WHERE code=?", (code,))
        if not cur.fetchone():
            cur.execute("INSERT INTO languages (code, name, color_hex) VALUES (?, ?, ?)",
                       (code, name, color))

    con.commit()
    con.close()

def get_config(key: str = 'global') -> Dict:
    """Get configuration from database"""
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT value_json FROM config WHERE key=?", (key,))
    row = cur.fetchone()
    con.close()
    
    if row:
        return json.loads(row[0])
    return {}

def load_language_pack(language_code: str) -> Dict:
    """Load language pack from JSON file"""
    pack_file = RULES_PATH / f"{language_code}.json"
    common_file = RULES_PATH / "_common.json"
    
    # Ensure rules directory exists
    RULES_PATH.mkdir(exist_ok=True)
    
    pack = {}
    
    # Load common rules first
    if common_file.exists():
        with open(common_file, 'r') as f:
            pack.update(json.load(f))
    
    # Load language-specific rules
    if pack_file.exists():
        with open(pack_file, 'r') as f:
            lang_pack = json.load(f)
            # Merge, with language-specific overriding common
            for key, value in lang_pack.items():
                if key in pack and isinstance(pack[key], dict) and isinstance(value, dict):
                    pack[key].update(value)
                else:
                    pack[key] = value
    else:
        # Create default language pack if it doesn't exist
        default_pack = {
            'topics': {
                'Basics': {'default_difficulty': 'Beginner', 'default_target_hours': 5},
                'Intermediate': {'default_difficulty': 'Intermediate', 'default_target_hours': 10},
                'Advanced': {'default_difficulty': 'Advanced', 'default_target_hours': 15}
            },
            'skills': {},
            'aliases': {}
        }
        
        with open(pack_file, 'w') as f:
            json.dump(default_pack, f, indent=2)
        pack.update(default_pack)
    
    return pack

def find_or_create_item(language_code: str, item_type: str, work_item_name: str) -> Tuple[int, bool, List[Dict]]:
    """
    Find existing item or create new one
    Returns: (item_id, is_new, suggestions)
    """
    con = connect()
    cur = con.cursor()
    
    # Normalize input
    slug = slugify(work_item_name)
    normalized_name = work_item_name.strip()
    
    # Try exact slug match first
    cur.execute("""
        SELECT id FROM items 
        WHERE language_code=? AND type=? AND slug=? AND is_active=1
    """, (language_code, item_type, slug))
    
    row = cur.fetchone()
    if row:
        con.close()
        return row[0], False, []
    
    # Try alias match
    cur.execute("""
        SELECT id, aliases_json FROM items 
        WHERE language_code=? AND type=? AND is_active=1
    """, (language_code, item_type))
    
    for item_id, aliases_json in cur.fetchall():
        aliases = json.loads(aliases_json or '[]')
        if slug in [slugify(alias) for alias in aliases]:
            con.close()
            return item_id, False, []
    
    # Generate suggestions for near matches
    suggestions = []
    cur.execute("""
        SELECT id, canonical_name, slug FROM items 
        WHERE language_code=? AND type=? AND is_active=1
    """, (language_code, item_type))
    
    for item_id, canonical_name, item_slug in cur.fetchall():
        # Simple similarity check
        if abs(len(slug) - len(item_slug)) <= 2:  # Length difference
            common_chars = set(slug) & set(item_slug)
            if len(common_chars) >= min(3, len(slug) // 2):  # Some common characters
                suggestions.append({
                    'id': item_id,
                    'name': canonical_name,
                    'similarity_hint': f"matched: {', '.join(sorted(common_chars)[:3])}"
                })
    
    # If we have close suggestions and the input is short, return them
    if suggestions and len(work_item_name.strip()) <= 20:
        con.close()
        return None, False, suggestions[:3]
    
    # Create new item
    pack = load_language_pack(language_code)
    
    # Auto-detect topic and difficulty from language pack
    default_topic = 'Basics'
    default_difficulty = 'Beginner'
    default_target = 5.0
    
    # Score against language pack keywords
    text_to_score = f"{normalized_name}".lower()
    best_score = 0
    
    for topic, topic_info in pack.get('topics', {}).items():
        score = 0
        # Simple keyword matching
        if topic.lower() in text_to_score:
            score += 10
        
        if score > best_score:
            best_score = score
            default_topic = topic
            default_difficulty = topic_info.get('default_difficulty', 'Beginner')
            default_target = topic_info.get('default_target_hours', 5.0)
    
    # Check skills for better matches
    for skill_name, skill_info in pack.get('skills', {}).items():
        score = 0
        keywords = skill_info.get('keywords', [])
        
        for keyword in keywords:
            if keyword.lower() in text_to_score:
                score += 5
        
        if skill_name.lower() in text_to_score:
            score += 15
            
        if score > best_score:
            best_score = score
            default_difficulty = skill_info.get('difficulty', default_difficulty)
            default_target = skill_info.get('default_target_hours', default_target)
    
    # Insert new item
    now = datetime.utcnow().isoformat()
    aliases = [normalized_name, slug]  # Start with input variants
    
    cur.execute("""
        INSERT INTO items (
            language_code, type, canonical_name, slug, aliases_json,
            default_difficulty, default_topic, target_hours, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (language_code, item_type, normalized_name, slug, json.dumps(aliases),
          default_difficulty, default_topic, default_target, now))
    
    item_id = cur.lastrowid
    con.commit()
    con.close()
    
    return item_id, True, []

def update_item_summaries(item_id: int):
    """Update computed fields for an item"""
    con = connect()
    cur = con.cursor()
    
    # Get all sessions for this item
    cur.execute("""
        SELECT date, hours_spent FROM sessions 
        WHERE item_id=? 
        ORDER BY date
    """, (item_id,))
    
    sessions = cur.fetchall()
    
    if not sessions:
        con.close()
        return
    
    # Calculate totals
    total_logs = len(sessions)
    total_hours = sum(float(row[1]) for row in sessions)
    last_logged_at = sessions[-1][0]
    
    # Calculate streaks
    dates = [datetime.fromisoformat(row[0]).date() for row in sessions]
    unique_dates = sorted(set(dates))
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 1
    
    if unique_dates:
        # Current streak (from most recent date backwards)
        today = datetime.now().date()
        for i, date in enumerate(reversed(unique_dates)):
            expected_date = today - timedelta(days=i)
            if date == expected_date:
                current_streak += 1
            else:
                break
        
        # Longest streak
        for i in range(1, len(unique_dates)):
            if (unique_dates[i] - unique_dates[i-1]).days == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
        longest_streak = max(longest_streak, temp_streak)
    
    # Calculate projected finish date
    cur.execute("SELECT target_hours FROM items WHERE id=?", (item_id,))
    target_row = cur.fetchone()
    target_hours = float(target_row[0]) if target_row and target_row[0] else 0
    
    projected_finish_date = None
    if target_hours > total_hours and len(unique_dates) >= 2:
        # Calculate average hours per active day (last 14 days of activity)
        recent_dates = [d for d in unique_dates if (datetime.now().date() - d).days <= 14]
        if recent_dates:
            recent_sessions = [s for s in sessions if datetime.fromisoformat(s[0]).date() in recent_dates]
            recent_hours = sum(float(s[1]) for s in recent_sessions)
            avg_hours_per_day = recent_hours / len(set(recent_dates))
            
            if avg_hours_per_day > 0:
                remaining_hours = target_hours - total_hours
                days_to_finish = remaining_hours / avg_hours_per_day
                projected_finish_date = (datetime.now() + timedelta(days=days_to_finish)).isoformat()
    
    # Update item
    cur.execute("""
        UPDATE items SET 
            total_logs=?, total_hours=?, last_logged_at=?,
            current_streak_days=?, longest_streak_days=?, projected_finish_date=?
        WHERE id=?
    """, (total_logs, total_hours, last_logged_at,
          current_streak, longest_streak, projected_finish_date, item_id))
    
    con.commit()
    con.close()

def insert_or_update_session(session_data: Dict) -> int:
    """Insert or update a session"""
    con = connect()
    cur = con.cursor()
    
    # Get global config for calculations
    config = get_config()
    diff_weights = config.get('difficulty_weights', {'Beginner': 1.0})
    status_multipliers = config.get('status_multipliers', {'In Progress': 1.0})
    
    # Calculate points
    hours = float(session_data.get('hours_spent', 0))
    difficulty = session_data.get('difficulty', 'Beginner')
    status = session_data.get('status', 'In Progress')
    
    points = hours * diff_weights.get(difficulty, 1.0) * status_multipliers.get(status, 1.0)
    
    # Calculate progress
    item_id = session_data['item_id']
    cur.execute("SELECT target_hours, total_hours FROM items WHERE id=?", (item_id,))
    item_row = cur.fetchone()
    
    target_hours = float(item_row[0]) if item_row and item_row[0] else 0
    current_total = float(item_row[1]) if item_row and item_row[1] else 0
    
    # For updates, subtract the old hours first
    if session_data.get('id'):
        cur.execute("SELECT hours_spent FROM sessions WHERE id=?", (session_data['id'],))
        old_hours_row = cur.fetchone()
        if old_hours_row:
            current_total -= float(old_hours_row[0])
    
    new_total = current_total + hours
    progress_pct = min(100.0, (new_total / target_hours) * 100.0) if target_hours > 0 else 0.0
    
    # Prepare session data
    cols = ['item_id', 'date', 'status', 'hours_spent', 'notes', 'tags', 
            'difficulty', 'topic', 'points_awarded', 'progress_pct']
    vals = [
        session_data['item_id'],
        session_data['date'],
        session_data.get('status', 'In Progress'),
        hours,
        session_data.get('notes', ''),
        session_data.get('tags', ''),
        session_data.get('difficulty', 'Beginner'),
        session_data.get('topic', ''),
        points,
        progress_pct
    ]
    
    if session_data.get('id'):
        # Update existing session
        sets = ",".join([f"{c}=?" for c in cols])
        cur.execute(f"UPDATE sessions SET {sets} WHERE id=?", (*vals, session_data['id']))
        session_id = session_data['id']
    else:
        # Insert new session
        placeholders = ",".join(["?"] * len(cols))
        cur.execute(f"INSERT INTO sessions({','.join(cols)}) VALUES({placeholders})", vals)
        session_id = cur.lastrowid
    
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
    
    # Update item summaries
    update_item_summaries(item_id)
    
    return session_id

def get_languages() -> List[Tuple[str, str, str]]:
    """Get all active languages"""
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT code, name, color_hex FROM languages WHERE is_active=1 ORDER BY name")
    result = cur.fetchall()
    con.close()
    return result

def search_items(language_code: str, item_type: str = None, query: str = None, limit: int = 50) -> List[Dict]:
    """Search items with optional filters"""
    con = connect()
    cur = con.cursor()
    
    sql = """
        SELECT id, canonical_name, type, target_hours, total_hours, 
               total_logs, current_streak_days, last_logged_at
        FROM items 
        WHERE language_code=? AND is_active=1
    """
    params = [language_code]
    
    if item_type:
        sql += " AND type=?"
        params.append(item_type)
    
    if query:
        sql += " AND (canonical_name LIKE ? OR slug LIKE ?)"
        query_pattern = f"%{query}%"
        params.extend([query_pattern, query_pattern])
    
    sql += " ORDER BY last_logged_at DESC, canonical_name LIMIT ?"
    params.append(limit)
    
    cur.execute(sql, params)
    rows = cur.fetchall()
    con.close()
    
    return [
        {
            'id': row[0], 'name': row[1], 'type': row[2],
            'target_hours': row[3], 'total_hours': row[4],
            'total_logs': row[5], 'current_streak': row[6],
            'last_logged_at': row[7]
        }
        for row in rows
    ]

def list_sessions(limit: int = 200) -> List[Tuple]:
    """Get recent sessions with item info"""
    con = connect()
    cur = con.cursor()
    
    cur.execute("""
        SELECT s.id, s.date, i.language_code, i.type, i.canonical_name, 
               s.status, s.hours_spent, s.notes, s.tags, s.difficulty, 
               s.topic, s.points_awarded, s.progress_pct, s.item_id
        FROM sessions s
        JOIN items i ON s.item_id = i.id
        ORDER BY s.date DESC, s.id DESC 
        LIMIT ?
    """, (limit,))
    
    result = cur.fetchall()
    con.close()
    return result

def get_item_by_id(item_id: int) -> Optional[Dict]:
    """Get item details by ID"""
    con = connect()
    cur = con.cursor()
    
    cur.execute("""
        SELECT id, language_code, type, canonical_name, slug, 
               default_difficulty, default_topic, target_hours,
               total_logs, total_hours, current_streak_days, projected_finish_date
        FROM items WHERE id=?
    """, (item_id,))
    
    row = cur.fetchone()
    con.close()
    
    if row:
        return {
            'id': row[0], 'language_code': row[1], 'type': row[2],
            'canonical_name': row[3], 'slug': row[4],
            'default_difficulty': row[5], 'default_topic': row[6],
            'target_hours': row[7], 'total_logs': row[8],
            'total_hours': row[9], 'current_streak_days': row[10],
            'projected_finish_date': row[11]
        }
    return None