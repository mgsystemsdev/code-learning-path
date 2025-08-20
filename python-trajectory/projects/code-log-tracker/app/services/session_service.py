# app/services/session_service.py
"""
Session Service - Business logic for managing learning sessions.

Handles:
- Session CRUD operations
- Item management and suggestions
- Points calculation
- Data export
"""

from __future__ import annotations
import csv
from typing import Dict, Any, List, Tuple, Optional

from app.db import (
    get_config,
    find_or_create_item,
    insert_or_update_session,
    list_sessions,
    search_items,
    get_item_by_id,
    connect,
    update_item_summaries,
)
from app.config.table_config import TableConfig


class SessionService:
    """Service for managing learning sessions and related data."""

    def __init__(self):
        self.config = get_config() or {}

    def get_sessions(self, limit: int = 1000) -> List[tuple]:
        """Get list of sessions for display."""
        try:
            return list_sessions(limit) or []
        except Exception as e:
            raise Exception(f"Failed to retrieve sessions: {e}")

    def save_session(self, session_data: Dict[str, Any], editing_session_id: Optional[int] = None):
        """Save a new or updated session with points calculation."""
        try:
            # Calculate points
            points = self._calculate_points(
                session_data.get("hours_spent", 0),
                session_data.get("difficulty", "Beginner"),
                session_data.get("status", "In Progress")
            )
            
            # Prepare full session data
            full_data = {
                **session_data,
                "points_awarded": points,
            }
            
            if editing_session_id:
                full_data["id"] = editing_session_id
            
            insert_or_update_session(full_data)
            
        except Exception as e:
            raise Exception(f"Failed to save session: {e}")

    def delete_session(self, session_id: int):
        """Delete a session and update related summaries."""
        try:
            with connect() as con:
                cur = con.cursor()
                
                # Get item_id before deletion for summary update
                cur.execute("SELECT item_id FROM sessions WHERE id=?", (session_id,))
                row = cur.fetchone()
                item_id = row[0] if row else None
                
                # Delete the session
                cur.execute("DELETE FROM sessions WHERE id=?", (session_id,))
                con.commit()
                
                # Update item summaries if needed
                if item_id is not None:
                    update_item_summaries(item_id)
                    
        except Exception as e:
            raise Exception(f"Failed to delete session: {e}")

    def update_session_inline(self, row_data: Dict[str, Any]) -> float:
        """Update a session from inline table editing and return new points."""
        try:
            # Calculate new points
            points = self._calculate_points(
                row_data.get("hours_spent", 0),
                row_data.get("difficulty", "Beginner"),
                row_data.get("status", "In Progress")
            )
            
            # Add points to data
            full_data = {**row_data, "points_awarded": points}
            
            # Save updates
            insert_or_update_session(full_data)
            
            return points
            
        except Exception as e:
            raise Exception(f"Failed to update session: {e}")

    def find_or_create_item(self, language_code: str, item_type: str, work_item: str) -> Tuple[int, List[Dict[str, Any]]]:
        """Find or create an item, returning item_id and any suggestions."""
        try:
            item_id, is_new, suggestions = find_or_create_item(language_code, item_type, work_item)
            return item_id, suggestions or []
        except Exception as e:
            raise Exception(f"Failed to find or create item: {e}")

    def search_items(self, language_code: str, item_type: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for existing items by language and type."""
        try:
            return search_items(language_code, item_type, limit) or []
        except Exception as e:
            raise Exception(f"Failed to search items: {e}")

    def get_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get item details by ID."""
        try:
            return get_item_by_id(item_id)
        except Exception as e:
            raise Exception(f"Failed to get item: {e}")

    def export_to_csv(self, file_path: str) -> int:
        """Export sessions to CSV file and return count of exported sessions."""
        try:
            sessions = self.get_sessions(100000)  # Get all sessions
            
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(TableConfig.HEADERS)
                
                for session in sessions:
                    row = self._format_session_for_export(session)
                    writer.writerow(row)
            
            return len(sessions)
            
        except Exception as e:
            raise Exception(f"Failed to export CSV: {e}")

    def _calculate_points(self, hours: float, difficulty: str, status: str) -> float:
        """Calculate points based on hours, difficulty, and status."""
        try:
            difficulty_weight = (self.config.get("difficulty_weights") or {}).get(difficulty, 1.0)
            status_multiplier = (self.config.get("status_multipliers") or {}).get(status, 1.0)
            
            return float(hours) * float(difficulty_weight) * float(status_multiplier)
            
        except Exception as e:
            # Fallback to simple calculation
            return float(hours)

    def _format_session_for_export(self, session: tuple) -> List[str]:
        """Format a session tuple for CSV export."""
        return [
            session[0],           # ID
            session[1],           # Date
            session[2],           # Language
            session[3],           # Type
            session[4],           # Work Item Name
            "",                   # Target Time (separate query if needed)
            session[5],           # Status
            session[6],           # Hours
            session[7],           # Notes
            session[8],           # Tags
            session[9],           # Difficulty
            session[10],          # Topic
            session[11],          # Points
            session[12],          # Progress %
        ]