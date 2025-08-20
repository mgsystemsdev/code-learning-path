# simple_db.py
"""
Simplified database for clean UI - stores learning sessions in local SQLite.
Focuses on basic save/load without complex rules or language packs.
"""

from __future__ import annotations
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Database path
DB_PATH = Path(__file__).resolve().parent / "clean_learning_tracker.db"

def connect():
    """Connect to SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_simple_db():
    """Initialize simple database with minimal tables."""
    con = connect()
    cur = con.cursor()
    
    # Simple sessions table
    cur.execute("""CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        language TEXT NOT NULL,
        type TEXT NOT NULL,
        work_item TEXT NOT NULL,
        topic TEXT,
        difficulty TEXT,
        status TEXT,
        tags TEXT,
        hours REAL NOT NULL,
        target_time REAL DEFAULT 0,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Simple languages table
    cur.execute("""CREATE TABLE IF NOT EXISTS languages(
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )""")
    
    # Insert default languages
    languages = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('html', 'HTML/CSS'),
        ('sql', 'SQL'),
        ('git', 'Git/DevOps'),
        ('general', 'General Theory')
    ]
    
    for code, name in languages:
        cur.execute("INSERT OR IGNORE INTO languages (code, name) VALUES (?, ?)", (code, name))
    
    con.commit()
    con.close()

class SimpleSessionService:
    """Simplified session service for clean UI."""
    
    def get_sessions(self, limit: int = 1000) -> List[tuple]:
        """Get all sessions."""
        con = connect()
        cur = con.cursor()
        
        cur.execute("""
            SELECT id, date, language, type, work_item, topic, difficulty, 
                   status, tags, hours, target_time, 0 as points, 0 as progress, notes
            FROM sessions 
            ORDER BY date DESC, id DESC 
            LIMIT ?
        """, (limit,))
        
        result = cur.fetchall()
        con.close()
        return result
    
    def save_session(self, session_data: Dict, editing_session_id: Optional[int] = None) -> int:
        """Save or update a session."""
        con = connect()
        cur = con.cursor()
        
        if editing_session_id:
            # Update existing session
            cur.execute("""
                UPDATE sessions SET 
                    date=?, language=?, type=?, work_item=?, topic=?, 
                    difficulty=?, status=?, tags=?, hours=?, target_time=?, notes=?
                WHERE id=?
            """, (
                session_data.get('date'),
                session_data.get('language_code'),
                session_data.get('type'),
                session_data.get('canonical_name'),
                session_data.get('topic'),
                session_data.get('difficulty'),
                session_data.get('status'),
                session_data.get('tags'),
                session_data.get('hours_spent'),
                session_data.get('target_hours'),
                session_data.get('notes'),
                editing_session_id
            ))
            session_id = editing_session_id
        else:
            # Insert new session
            cur.execute("""
                INSERT INTO sessions 
                    (date, language, type, work_item, topic, difficulty, status, tags, hours, target_time, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_data.get('date'),
                session_data.get('language_code'),
                session_data.get('type'),
                session_data.get('canonical_name'),
                session_data.get('topic'),
                session_data.get('difficulty'),
                session_data.get('status'),
                session_data.get('tags'),
                session_data.get('hours_spent'),
                session_data.get('target_hours'),
                session_data.get('notes')
            ))
            session_id = cur.lastrowid
        
        con.commit()
        con.close()
        return session_id
    
    def delete_session(self, session_id: int):
        """Delete a session."""
        con = connect()
        cur = con.cursor()
        cur.execute("DELETE FROM sessions WHERE id=?", (session_id,))
        con.commit()
        con.close()
    
    def find_or_create_item(self, language_code: str, item_type: str, work_item: str) -> Tuple[int, List]:
        """Simple version - just return dummy item_id and no suggestions."""
        return 1, []

class SimpleLanguageService:
    """Simplified language service for clean UI."""
    
    def get_languages(self) -> List[Tuple[str, str, str]]:
        """Get all languages."""
        con = connect()
        cur = con.cursor()
        cur.execute("SELECT code, name, '#666666' FROM languages ORDER BY name")
        result = cur.fetchall()
        con.close()
        return result
