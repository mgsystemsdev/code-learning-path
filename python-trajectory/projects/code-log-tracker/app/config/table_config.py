# app/config/table_config.py
"""
Table Configuration - Centralized table structure definitions.

Defines:
- Column headers and keys
- Column widths and properties
- Editable columns
- Read-only columns
"""

from typing import List, Set, Dict


class TableConfig:
    """Configuration for the main data table."""
    
    # Column headers displayed in the table (exact order per requirements)
    HEADERS: List[str] = [
        "ID",              # 1. Unique identifier (read-only)
        "Date",            # 2. Date of work session  
        "Type",            # 3. Exercise or Project
        "Work Item Name",  # 4. Exercise/Project name
        "Notes",           # 5. Session details
        "Status",          # 6. Progress stage
        "Hours",           # 7. Time spent
        "Tags",            # 8. Keywords for grouping
        "Language",        # 9. Programming language
        "Difficulty",      # 10. Complexity rating
        "Topic",           # 11. Broad category
        "Points",          # 12. Computed score (read-only)
        "Progress %",      # 13. Completion percentage (read-only)
        "Target Time",     # 14. Planned total hours
    ]

    # Database field keys corresponding to headers
    KEYS: List[str] = [
        "id",                # 0 - ID
        "date",              # 1 - Date
        "type",              # 2 - Type
        "canonical_name",    # 3 - Work Item Name
        "notes",             # 4 - Notes
        "status",            # 5 - Status
        "hours_spent",       # 6 - Hours
        "tags",              # 7 - Tags
        "language_code",     # 8 - Language
        "difficulty",        # 9 - Difficulty
        "topic",             # 10 - Topic
        "points_awarded",    # 11 - Points
        "progress_pct",      # 12 - Progress %
        "target_hours",      # 13 - Target Time
    ]

    # Proportional column widths - all 14 columns always visible
    COLUMN_WIDTHS: Dict[str, int] = {
        "ID": 60,                 # Fixed narrow
        "Date": 100,             # Short field
        "Type": 80,              # Short field  
        "Work Item Name": -1,     # Flexible fill (largest)
        "Notes": -2,             # Flexible fill (second largest)
        "Status": 100,           # Short field
        "Hours": 80,             # Short field
        "Tags": 120,             # Medium field
        "Language": 100,         # Short field
        "Difficulty": 100,       # Short field
        "Topic": 100,            # Short field
        "Points": 80,            # Short field
        "Progress %": 100,       # Short field
        "Target Time": 120,      # Medium field
    }
    
    # Column widths as list (for backwards compatibility)
    COLUMN_WIDTHS_LIST: List[int] = [
        60,   # ID
        100,  # Date
        80,   # Type
        300,  # Work Item Name (will be flexible)
        250,  # Notes (will be flexible)
        100,  # Status
        80,   # Hours
        120,  # Tags
        100,  # Language
        100,  # Difficulty
        100,  # Topic
        80,   # Points
        100,  # Progress %
        120,  # Target Time
    ]

    # Columns that can be edited inline
    EDITABLE_COLS: Set[str] = {
        "Date",
        "Type", 
        "Work Item Name",
        "Notes",
        "Status",
        "Hours",
        "Tags",
        "Language",
        "Difficulty",
        "Topic",
        "Target Time",
    }

    # Columns that are read-only (computed or system fields)
    READONLY_COLUMNS: Set[int] = {0, 11, 12}  # ID, Points, Progress %

    @classmethod
    def get_column_index(cls, header: str) -> int:
        """Get the column index for a given header name."""
        try:
            return cls.HEADERS.index(header)
        except ValueError:
            raise ValueError(f"Header '{header}' not found in table configuration")

    @classmethod
    def get_key_for_header(cls, header: str) -> str:
        """Get the database key for a given header."""
        try:
            index = cls.HEADERS.index(header)
            return cls.KEYS[index]
        except (ValueError, IndexError):
            raise ValueError(f"No key found for header '{header}'")

    @classmethod
    def get_header_for_key(cls, key: str) -> str:
        """Get the header name for a given database key."""
        try:
            index = cls.KEYS.index(key)
            return cls.HEADERS[index]
        except (ValueError, IndexError):
            raise ValueError(f"No header found for key '{key}'")

    @classmethod
    def is_editable(cls, header: str) -> bool:
        """Check if a column is editable."""
        return header in cls.EDITABLE_COLS

    @classmethod
    def is_readonly(cls, header: str) -> bool:
        """Check if a column is read-only."""
        try:
            index = cls.get_column_index(header)
            return index in cls.READONLY_COLUMNS
        except ValueError:
            return False

    @classmethod
    def get_display_headers(cls) -> List[str]:
        """Get headers formatted for display."""
        return cls.HEADERS.copy()

    @classmethod
    def get_editable_headers(cls) -> List[str]:
        """Get list of editable column headers."""
        return list(cls.EDITABLE_COLS)

    @classmethod
    def get_readonly_headers(cls) -> List[str]:
        """Get list of read-only column headers."""
        return [cls.HEADERS[i] for i in cls.READONLY_COLUMNS]

    @classmethod
    def validate_configuration(cls) -> bool:
        """Validate that the configuration is consistent."""
        # Check that HEADERS and KEYS have the same length
        if len(cls.HEADERS) != len(cls.KEYS):
            raise ValueError("HEADERS and KEYS must have the same length")
        
        # Check that COLUMN_WIDTHS matches HEADERS length
        if len(cls.COLUMN_WIDTHS) != len(cls.HEADERS):
            raise ValueError("COLUMN_WIDTHS must match HEADERS length")
        
        # Check that all editable columns exist in HEADERS
        for col in cls.EDITABLE_COLS:
            if col not in cls.HEADERS:
                raise ValueError(f"Editable column '{col}' not found in HEADERS")
        
        # Check that all readonly column indices are valid
        for idx in cls.READONLY_COLUMNS:
            if idx >= len(cls.HEADERS):
                raise ValueError(f"Read-only column index {idx} is out of range")
        
        return True


# Validate configuration on import
TableConfig.validate_configuration()