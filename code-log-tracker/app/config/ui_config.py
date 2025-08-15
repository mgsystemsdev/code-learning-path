# app/config/ui_config.py
"""
UI Configuration - Modern responsive design settings.
"""

from typing import Dict, List, Tuple
from PySide6.QtCore import QSize

class UIConfig:
    """Modern UI configuration with responsive design."""
    
    # Dark Theme Color Palette
    COLORS = {
        'primary': '#3b82f6',
        'primary_light': '#1e40af', 
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'background': '#0f172a',     # Dark slate
        'surface': '#1e293b',        # Dark gray
        'surface_light': '#334155',  # Lighter gray
        'border': '#475569',         # Gray border
        'text_primary': '#ffffff',   # Pure white text for high contrast
        'text_secondary': '#e2e8f0', # Very light secondary text
        'input_bg': '#334155',       # Input background
        'hover': '#475569',          # Hover state
    }
    
    # Window Settings
    WINDOW_SIZE = QSize(1200, 800)
    MIN_WINDOW_SIZE = QSize(800, 600)
    
    # Table Configuration
    TABLE_MIN_WIDTH = 800
    COLUMN_PRIORITIES = {
        'essential': ['Date', 'Work Item Name', 'Hours', 'Status', 'Type'],
        'important': ['Notes', 'Language', 'Progress %', 'Difficulty'],
        'optional': ['Topic', 'Tags', 'Points', 'Target Time'],
        'hidden': ['ID']
    }
    
    # Responsive Breakpoints
    BREAKPOINTS = {
        'xs': 600,   # Hide optional columns
        'sm': 800,   # Show important columns  
        'md': 1000,  # Show most columns
        'lg': 1200,  # Show all columns
        'xl': 1400   # Optimal layout
    }
    
    # Dark Theme Styles
    MAIN_STYLE = """
        QMainWindow {
            background-color: #0f172a;
            color: #ffffff;
        }
        
        QGroupBox {
            font-weight: 600;
            font-size: 14px;
            color: #ffffff;
            border: 2px solid #475569;
            border-radius: 10px;
            margin: 8px 4px;
            padding: 18px;
            background-color: #1e293b;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 4px 12px;
            background-color: #1e293b;
            color: #60a5fa;
            font-weight: 700;
            font-size: 14px;
        }
        
        QTableWidget {
            alternate-background-color: #334155;
            background-color: #1e293b;
            gridline-color: #475569;
            border: 1px solid #475569;
            border-radius: 8px;
            selection-background-color: #1e40af;
            selection-color: #f8fafc;
            color: #ffffff;
        }
        
        QTableWidget::item {
            padding: 10px;
            border-bottom: 1px solid #334155;
        }
        
        QTableWidget::item:selected {
            background-color: #1e40af;
            color: #ffffff;
        }
        
        QHeaderView::section {
            background-color: #334155;
            padding: 12px;
            border: 1px solid #475569;
            border-left: none;
            font-weight: 600;
            color: #cbd5e1;
        }
        
        QHeaderView::section:first {
            border-left: 1px solid #475569;
        }
        
        QPushButton {
            background-color: #334155;
            border: 2px solid #475569;
            border-radius: 8px;
            padding: 12px 20px;
            font-weight: 600;
            color: #ffffff;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #475569;
            border-color: #60a5fa;
            color: #ffffff;
        }
        
        QPushButton:pressed {
            background-color: #1e40af;
        }
        
        QPushButton:disabled {
            background-color: #1e293b;
            color: #64748b;
            border-color: #334155;
        }
        
        /* Primary Button Variant */
        QPushButton[variant="primary"] {
            background-color: #3b82f6;
            color: #ffffff;
            border-color: #3b82f6;
        }
        
        QPushButton[variant="primary"]:hover {
            background-color: #2563eb;
        }
        
        QPushButton[variant="danger"] {
            background-color: #ef4444;
            color: #ffffff;
            border-color: #ef4444;
        }
        
        QPushButton[variant="danger"]:hover {
            background-color: #dc2626;
        }
        
        QComboBox, QLineEdit, QDoubleSpinBox, QDateEdit {
            border: 2px solid #475569;
            border-radius: 6px;
            padding: 8px 12px;
            background-color: #334155;
            color: #f1f5f9;
            font-size: 13px;
            font-weight: 500;
            selection-background-color: #1e40af;
            selection-color: #ffffff;
        }
        
        QComboBox:focus, QLineEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus {
            border-color: #60a5fa;
            outline: none;
            background-color: #475569;
            color: #ffffff;
        }
        
        QComboBox::drop-down {
            border: none;
            border-left: 1px solid #475569;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            background-color: #475569;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 6px solid #cbd5e1;
            width: 0;
            height: 0;
        }
        
        QComboBox QAbstractItemView {
            border: 1px solid #475569;
            background-color: #334155;
            color: #ffffff;
            selection-background-color: #1e40af;
        }
        
        QLabel {
            color: #ffffff;
            font-weight: 500;
        }
        
        QStatusBar {
            background-color: #1e293b;
            border-top: 1px solid #475569;
            color: #cbd5e1;
        }
        
        QMenuBar {
            background-color: #1e293b;
            color: #ffffff;
            border-bottom: 1px solid #475569;
        }
        
        QMenuBar::item:selected {
            background-color: #334155;
        }
        
        QMenu {
            background-color: #1e293b;
            color: #ffffff;
            border: 1px solid #475569;
        }
        
        QMenu::item:selected {
            background-color: #334155;
        }
        
        QFrame {
            background-color: #1e293b;
            border: 1px solid #475569;
            border-radius: 8px;
        }
        
        QSplitter::handle {
            background-color: #475569;
        }
        
        QSplitter::handle:horizontal {
            height: 2px;
        }
        
        QSplitter::handle:vertical {
            width: 2px;
        }
        
        /* Scrollbars */
        QScrollBar:vertical {
            background: #1e293b;
            width: 14px;
            border-radius: 7px;
            border: 1px solid #475569;
        }
        
        QScrollBar::handle:vertical {
            background: #475569;
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #60a5fa;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        
        QScrollBar:horizontal {
            background: #1e293b;
            height: 14px;
            border-radius: 7px;
            border: 1px solid #475569;
        }
        
        QScrollBar::handle:horizontal {
            background: #475569;
            border-radius: 6px;
            min-width: 20px;
            margin: 2px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #60a5fa;
        }
    """
    
    # Status-based colors for table rows
    STATUS_COLORS = {
        'Completed': '#10b981',    # Green
        'In Progress': '#3b82f6',  # Blue  
        'Planned': '#6b7280',      # Gray
        'Blocked': '#ef4444',      # Red
    }
    
    # Difficulty colors
    DIFFICULTY_COLORS = {
        'Beginner': '#10b981',     # Green
        'Intermediate': '#f59e0b', # Yellow
        'Advanced': '#ef4444',     # Red
        'Expert': '#8b5cf6',       # Purple
    }
