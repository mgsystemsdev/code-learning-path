# app/supabase_client.py
"""
Supabase client configuration and authentication management.
"""

import os
import streamlit as st
from typing import Dict, Any, Optional, List, Tuple
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables (for local development)
load_dotenv()

def _get_secret(name: str) -> str | None:
    """Get secret from Streamlit secrets or environment variables."""
    try:
        return st.secrets.get(name) or os.getenv(name)
    except:
        return os.getenv(name)

class SupabaseManager:
    """Manages Supabase client and authentication. Uses only anon key for security."""
    
    def __init__(self):
        # Get required configuration
        self.url = _get_secret("SUPABASE_URL")
        self.anon_key = _get_secret("SUPABASE_ANON_KEY")
        
        # Check for missing configuration
        missing = []
        if not self.url:
            missing.append("SUPABASE_URL")
        if not self.anon_key:
            missing.append("SUPABASE_ANON_KEY")
            
        if missing:
            raise ValueError(f"Missing Supabase configuration: {', '.join(missing)}.")
            
        # Create client with anon key only (respects RLS)
        self.client: Client = create_client(self.url, self.anon_key)
    
    # Authentication Methods
    def sign_up(self, email: str, password: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Sign up a new user."""
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": metadata} if metadata else None
            })
            return {"success": True, "data": response}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in user."""
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {"success": True, "data": response}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def sign_out(self) -> Dict[str, Any]:
        """Sign out current user."""
        try:
            self.client.auth.sign_out()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user(self) -> Optional[Dict[str, Any]]:
        """Get current user."""
        try:
            response = self.client.auth.get_user()
            return response.user.__dict__ if response.user else None
        except Exception as e:
            st.error(f"Error getting user: {e}")
            return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.get_user() is not None
    
    # Database Methods
    def create_tables(self) -> Dict[str, Any]:
        """Create database tables using SQL."""
        sql_statements = [
            # Languages table
            """
            CREATE TABLE IF NOT EXISTS languages (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                color TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid()
            );
            """,
            
            # Items table (exercises/projects)
            """
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                language_code TEXT REFERENCES languages(code),
                type TEXT NOT NULL CHECK (type IN ('Exercise', 'Project')),
                canonical_name TEXT NOT NULL,
                slug TEXT NOT NULL,
                aliases_json TEXT DEFAULT '[]',
                default_difficulty TEXT,
                default_topic TEXT,
                target_hours DECIMAL DEFAULT 0,
                total_logs INTEGER DEFAULT 0,
                total_hours DECIMAL DEFAULT 0,
                last_logged_at TIMESTAMP WITH TIME ZONE,
                current_streak_days INTEGER DEFAULT 0,
                longest_streak_days INTEGER DEFAULT 0,
                projected_finish_date DATE,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid(),
                UNIQUE(language_code, type, slug, user_id)
            );
            """,
            
            # Sessions table
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id SERIAL PRIMARY KEY,
                item_id INTEGER REFERENCES items(id),
                date DATE NOT NULL,
                status TEXT DEFAULT 'In Progress',
                hours_spent DECIMAL NOT NULL CHECK (hours_spent >= 0),
                notes TEXT,
                tags TEXT,
                difficulty TEXT,
                topic TEXT,
                points_awarded DECIMAL DEFAULT 0,
                progress_pct DECIMAL DEFAULT 0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid()
            );
            """,
            
            # Configuration table
            """
            CREATE TABLE IF NOT EXISTS config (
                key TEXT NOT NULL,
                value_json TEXT NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid(),
                PRIMARY KEY (key, user_id)
            );
            """
        ]
        
        try:
            for sql in sql_statements:
                self.client.rpc('exec_sql', {'sql': sql}).execute()
            return {"success": True, "message": "Tables created successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def setup_rls_policies(self) -> Dict[str, Any]:
        """Set up Row Level Security policies."""
        policies = [
            # Enable RLS on all tables
            "ALTER TABLE languages ENABLE ROW LEVEL SECURITY;",
            "ALTER TABLE items ENABLE ROW LEVEL SECURITY;", 
            "ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;",
            "ALTER TABLE config ENABLE ROW LEVEL SECURITY;",
            
            # Languages policies
            """
            CREATE POLICY "Users can view their own languages" ON languages
            FOR SELECT USING (user_id = auth.uid());
            """,
            """
            CREATE POLICY "Users can insert their own languages" ON languages
            FOR INSERT WITH CHECK (user_id = auth.uid());
            """,
            """
            CREATE POLICY "Users can update their own languages" ON languages
            FOR UPDATE USING (user_id = auth.uid());
            """,
            
            # Items policies  
            """
            CREATE POLICY "Users can view their own items" ON items
            FOR SELECT USING (user_id = auth.uid());
            """,
            """
            CREATE POLICY "Users can insert their own items" ON items
            FOR INSERT WITH CHECK (user_id = auth.uid());
            """,
            """
            CREATE POLICY "Users can update their own items" ON items
            FOR UPDATE USING (user_id = auth.uid());
            """,
            
            # Sessions policies
            """
            CREATE POLICY "Users can view their own sessions" ON sessions
            FOR SELECT USING (user_id = auth.uid());
            """,
            """
            CREATE POLICY "Users can insert their own sessions" ON sessions
            FOR INSERT WITH CHECK (user_id = auth.uid());
            """,
            """
            CREATE POLICY "Users can update their own sessions" ON sessions
            FOR UPDATE USING (user_id = auth.uid());
            """,
            """
            CREATE POLICY "Users can delete their own sessions" ON sessions
            FOR DELETE USING (user_id = auth.uid());
            """,
            
            # Config policies
            """
            CREATE POLICY "Users can view their own config" ON config
            FOR SELECT USING (user_id = auth.uid());
            """,
            """
            CREATE POLICY "Users can insert their own config" ON config
            FOR INSERT WITH CHECK (user_id = auth.uid());
            """,
            """
            CREATE POLICY "Users can update their own config" ON config
            FOR UPDATE USING (user_id = auth.uid());
            """
        ]
        
        try:
            for policy in policies:
                self.client.rpc('exec_sql', {'sql': policy}).execute()
            return {"success": True, "message": "RLS policies created successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # CRUD Operations
    def get_sessions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get user's sessions with related item data."""
        try:
            response = (
                self.client
                .table('sessions')
                .select('''
                    *,
                    items (
                        language_code,
                        type,
                        canonical_name,
                        target_hours
                    )
                ''')
                .order('date', desc=True)
                .order('created_at', desc=True)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            st.error(f"Error fetching sessions: {e}")
            return []
    
    def create_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new learning session."""
        try:
            # First, find or create the item
            item = self.find_or_create_item(
                session_data['language_code'],
                session_data['type'], 
                session_data['canonical_name']
            )
            
            if not item['success']:
                return item
                
            # Create session with item_id
            session_data['item_id'] = item['data']['id']
            
            # Calculate points
            points = self._calculate_points(
                session_data.get('hours_spent', 0),
                session_data.get('difficulty', 'Beginner'),
                session_data.get('status', 'In Progress')
            )
            session_data['points_awarded'] = points
            
            response = self.client.table('sessions').insert(session_data).execute()
            
            # Update item statistics
            self._update_item_stats(item['data']['id'])
            
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_session(self, session_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing session."""
        try:
            # Recalculate points if relevant fields changed
            if any(field in updates for field in ['hours_spent', 'difficulty', 'status']):
                # Get current session to merge data
                current = self.client.table('sessions').select('*').eq('id', session_id).execute()
                if current.data:
                    merged_data = {**current.data[0], **updates}
                    points = self._calculate_points(
                        merged_data.get('hours_spent', 0),
                        merged_data.get('difficulty', 'Beginner'),
                        merged_data.get('status', 'In Progress')
                    )
                    updates['points_awarded'] = points
            
            response = self.client.table('sessions').update(updates).eq('id', session_id).execute()
            return {"success": True, "data": response.data[0] if response.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_session(self, session_id: int) -> Dict[str, Any]:
        """Delete a session."""
        try:
            response = self.client.table('sessions').delete().eq('id', session_id).execute()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_or_create_item(self, language_code: str, item_type: str, name: str) -> Dict[str, Any]:
        """Find existing item or create new one."""
        try:
            # Generate slug
            slug = self._slugify(name)
            
            # Try to find existing item
            existing = (
                self.client.table('items')
                .select('*')
                .eq('language_code', language_code)
                .eq('type', item_type)
                .eq('slug', slug)
                .execute()
            )
            
            if existing.data:
                return {"success": True, "data": existing.data[0]}
            
            # Create new item
            item_data = {
                'language_code': language_code,
                'type': item_type,
                'canonical_name': name,
                'slug': slug,
                'target_hours': 0,
                'is_active': True
            }
            
            response = self.client.table('items').insert(item_data).execute()
            return {"success": True, "data": response.data[0]}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_languages(self) -> List[Dict[str, Any]]:
        """Get available programming languages."""
        try:
            response = self.client.table('languages').select('*').execute()
            return response.data
        except Exception as e:
            st.error(f"Error fetching languages: {e}")
            return []
    
    def _calculate_points(self, hours: float, difficulty: str, status: str) -> float:
        """Calculate points for a session."""
        difficulty_multipliers = {
            'Beginner': 1.0,
            'Intermediate': 1.5, 
            'Advanced': 2.0,
            'Expert': 2.5
        }
        
        status_multipliers = {
            'Planned': 1.0,
            'In Progress': 1.1,
            'Completed': 1.2,
            'Blocked': 0.8
        }
        
        return (hours * 
                difficulty_multipliers.get(difficulty, 1.0) * 
                status_multipliers.get(status, 1.0))
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
    
    def _update_item_stats(self, item_id: int):
        """Update item statistics after session changes."""
        # This would recalculate total hours, progress, etc.
        # Implementation depends on your specific requirements
        pass


# Global instance with proper error handling
@st.cache_resource(show_spinner=False)
def get_supabase_manager() -> SupabaseManager:
    """Get cached Supabase manager instance."""
    try:
        return SupabaseManager()
    except ValueError as e:
        st.error("Supabase configuration is incomplete.")
        st.error(str(e))
        st.stop()

# Alias for compatibility
SupabaseClient = SupabaseManager
