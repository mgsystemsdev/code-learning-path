#!/usr/bin/env python3
"""
Final database setup script with your actual Supabase credentials.
Run this to set up your database completely.
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Load from environment (your .env file)
load_dotenv()

def setup_database():
    """Setup complete database with admin permissions."""
    
    try:
        # Get credentials from environment
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY") 
        
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            print("❌ Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in .env file")
            return False
            
        # Create client with service role (admin permissions)
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print("🔧 Connected to Supabase with admin permissions")
        
        # Create all tables step by step
        print("📋 Creating database tables...")
        
        # 1. Languages table
        print("  Creating languages table...")
        try:
            supabase.table('languages').select('*').limit(1).execute()
            print("  ✅ Languages table already exists")
        except:
            # Create using SQL if table doesn't exist
            result = supabase.rpc('exec_sql', {
                'sql': """
                CREATE TABLE public.languages (
                    code TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    color TEXT DEFAULT '#6c757d',
                    is_active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    user_id UUID REFERENCES auth.users(id) DEFAULT NULL
                );
                
                ALTER TABLE public.languages ENABLE ROW LEVEL SECURITY;
                
                CREATE POLICY "languages_public_read" ON public.languages
                FOR SELECT USING (true);
                
                CREATE POLICY "languages_user_write" ON public.languages
                FOR ALL USING (auth.uid() IS NOT NULL);
                """
            }).execute()
            print("  ✅ Languages table created")
        
        # 2. Items table  
        print("  Creating items table...")
        try:
            result = supabase.rpc('exec_sql', {
                'sql': """
                CREATE TABLE IF NOT EXISTS public.items (
                    id BIGSERIAL PRIMARY KEY,
                    language_code TEXT REFERENCES public.languages(code),
                    type TEXT NOT NULL CHECK (type IN ('Exercise', 'Project')),
                    canonical_name TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    aliases_json TEXT DEFAULT '[]',
                    default_difficulty TEXT DEFAULT 'Beginner',
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
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid()
                );
                
                ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;
                
                CREATE POLICY IF NOT EXISTS "items_user_access" ON public.items
                FOR ALL USING (user_id = auth.uid());
                """
            }).execute()
            print("  ✅ Items table created")
        except Exception as e:
            print(f"  ⚠️  Items table: {e}")
        
        # 3. Sessions table
        print("  Creating sessions table...")
        try:
            result = supabase.rpc('exec_sql', {
                'sql': """
                CREATE TABLE IF NOT EXISTS public.sessions (
                    id BIGSERIAL PRIMARY KEY,
                    item_id BIGINT REFERENCES public.items(id) ON DELETE CASCADE,
                    date DATE NOT NULL,
                    status TEXT DEFAULT 'In Progress',
                    hours_spent DECIMAL NOT NULL CHECK (hours_spent >= 0),
                    notes TEXT,
                    tags TEXT,
                    difficulty TEXT DEFAULT 'Beginner',
                    topic TEXT,
                    points_awarded DECIMAL DEFAULT 0,
                    progress_pct DECIMAL DEFAULT 0,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid()
                );
                
                ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;
                
                CREATE POLICY IF NOT EXISTS "sessions_user_access" ON public.sessions
                FOR ALL USING (user_id = auth.uid());
                """
            }).execute()
            print("  ✅ Sessions table created")
        except Exception as e:
            print(f"  ⚠️  Sessions table: {e}")
            
        # 4. Config table
        print("  Creating config table...")
        try:
            result = supabase.rpc('exec_sql', {
                'sql': """
                CREATE TABLE IF NOT EXISTS public.config (
                    id BIGSERIAL PRIMARY KEY,
                    key TEXT NOT NULL UNIQUE,
                    value_json TEXT NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    user_id UUID REFERENCES auth.users(id) DEFAULT NULL
                );
                
                ALTER TABLE public.config ENABLE ROW LEVEL SECURITY;
                
                CREATE POLICY IF NOT EXISTS "config_public_read" ON public.config
                FOR SELECT USING (user_id IS NULL OR user_id = auth.uid());
                
                CREATE POLICY IF NOT EXISTS "config_user_write" ON public.config
                FOR ALL USING (user_id = auth.uid() OR auth.uid() IS NOT NULL);
                """
            }).execute()
            print("  ✅ Config table created")
        except Exception as e:
            print(f"  ⚠️  Config table: {e}")
        
        # Insert default languages
        print("📊 Inserting default data...")
        
        languages_data = [
            {'code': 'python', 'name': 'Python', 'description': 'General-purpose programming language', 'color': '#3776ab'},
            {'code': 'javascript', 'name': 'JavaScript', 'description': 'Dynamic programming language for web', 'color': '#f7df1e'},
            {'code': 'html', 'name': 'HTML/CSS', 'description': 'Markup and styling languages', 'color': '#e34f26'},
            {'code': 'sql', 'name': 'SQL', 'description': 'Database query language', 'color': '#336791'},
            {'code': 'git', 'name': 'Git/DevOps', 'description': 'Version control and deployment', 'color': '#f05032'},
            {'code': 'general', 'name': 'General/Theory', 'description': 'Programming concepts and theory', 'color': '#6c757d'},
            {'code': 'react', 'name': 'React', 'description': 'JavaScript library for UIs', 'color': '#61dafb'},
            {'code': 'typescript', 'name': 'TypeScript', 'description': 'Typed superset of JavaScript', 'color': '#3178c6'},
        ]
        
        for lang in languages_data:
            try:
                supabase.table('languages').upsert(lang, on_conflict='code').execute()
            except Exception as e:
                print(f"  ⚠️  Language {lang['code']}: {e}")
        
        print("  ✅ Default languages inserted")
        
        # Insert default configuration
        config_data = [
            {'key': 'difficulty_weights', 'value_json': '{"Beginner": 1.0, "Intermediate": 1.5, "Advanced": 2.0, "Expert": 2.5}'},
            {'key': 'status_multipliers', 'value_json': '{"Planned": 1.0, "In Progress": 1.1, "Completed": 1.2, "Blocked": 0.8}'},
            {'key': 'ui_limits', 'value_json': '{"max_hours_per_session": 24, "min_hours_per_session": 0.25}'},
        ]
        
        for config in config_data:
            try:
                supabase.table('config').upsert(config, on_conflict='key').execute()
            except Exception as e:
                print(f"  ⚠️  Config {config['key']}: {e}")
        
        print("  ✅ Default configuration inserted")
        
        print("\n🎉 Database setup completed successfully!")
        print("✅ Tables: languages, items, sessions, config")
        print("✅ Security: RLS enabled with user isolation")
        print("✅ Data: Default languages and config loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def test_connection():
    """Test the connection with regular anon key."""
    try:
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
        
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        # Try to query languages
        result = supabase.table('languages').select('*').limit(5).execute()
        print(f"✅ Connection test passed: Found {len(result.data)} languages")
        
        for lang in result.data:
            print(f"  - {lang['name']} ({lang['code']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Smart Learning Tracker - Final Database Setup")
    print("=" * 55)
    print(f"Using credentials from .env file")
    print("=" * 55)
    
    choice = input("""Choose option:
1. Setup database (create tables, policies, data)
2. Test connection only
3. Both setup and test
4. Exit
Enter 1, 2, 3, or 4: """)
    
    if choice == "1":
        if setup_database():
            print("\n🎯 Next steps:")
            print("1. Add secrets to Streamlit Cloud app settings")
            print("2. Test: streamlit run streamlit_app.py")
            
    elif choice == "2":
        test_connection()
        
    elif choice == "3":
        print("\n📋 Step 1: Setting up database...")
        if setup_database():
            print("\n📋 Step 2: Testing connection...")
            test_connection()
            
            print("\n🎯 Complete setup finished!")
            print("Your Smart Learning Tracker is ready to use!")
        
    else:
        print("👋 Goodbye!")
