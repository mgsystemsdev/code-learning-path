# app/services/ui_state_service.py
"""
UI State Service - Handles UI state management and formatting.

Handles:
- Status display formatting
- UI state persistence
- Display formatting utilities
"""

from __future__ import annotations
from typing import Dict, Any, List


class UIStateService:
    """Service for managing UI state and display formatting."""

    def format_item_status(self, item: Dict[str, Any]) -> List[str]:
        """Format item information for status display.
        
        Args:
            item: Dictionary containing item data
            
        Returns:
            List of formatted status strings
        """
        status_parts = []
        
        if item.get("name"):
            status_parts.append(f"Item: {item['name']}")
            
        if item.get("language"):
            status_parts.append(f"Language: {item['language']}")
            
        if item.get("topic"):
            status_parts.append(f"Topic: {item['topic']}")
            
        if item.get("difficulty"):
            status_parts.append(f"Difficulty: {item['difficulty']}")
            
        return status_parts
