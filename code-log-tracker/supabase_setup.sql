-- supabase_setup.sql
-- Complete database setup for Learning Tracker with Supabase

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom function for SQL execution (for setup scripts)
CREATE OR REPLACE FUNCTION exec_sql(sql text)
RETURNS text
LANGUAGE plpgsql
SECURITY definer
AS $$
BEGIN
  EXECUTE sql;
  RETURN 'OK';
END;
$$;

-- Languages table
CREATE TABLE IF NOT EXISTS languages (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    color TEXT DEFAULT '#60a5fa',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid()
);

-- Items table (exercises/projects)
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    language_code TEXT REFERENCES languages(code),
    type TEXT NOT NULL CHECK (type IN ('Exercise', 'Project')),
    canonical_name TEXT NOT NULL,
    slug TEXT NOT NULL,
    aliases_json TEXT DEFAULT '[]',
    default_difficulty TEXT,
    default_topic TEXT,
    target_hours DECIMAL(10,2) DEFAULT 0,
    total_logs INTEGER DEFAULT 0,
    total_hours DECIMAL(10,2) DEFAULT 0,
    last_logged_at TIMESTAMP WITH TIME ZONE,
    current_streak_days INTEGER DEFAULT 0,
    longest_streak_days INTEGER DEFAULT 0,
    projected_finish_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid(),
    UNIQUE(language_code, type, slug, user_id)
);

-- Sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    status TEXT DEFAULT 'In Progress' CHECK (status IN ('Planned', 'In Progress', 'Completed', 'Blocked')),
    hours_spent DECIMAL(10,2) NOT NULL CHECK (hours_spent >= 0),
    notes TEXT,
    tags TEXT,
    difficulty TEXT DEFAULT 'Beginner' CHECK (difficulty IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),
    topic TEXT,
    points_awarded DECIMAL(10,2) DEFAULT 0,
    progress_pct DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid()
);

-- Configuration table
CREATE TABLE IF NOT EXISTS config (
    key TEXT NOT NULL,
    value_json TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) DEFAULT auth.uid(),
    PRIMARY KEY (key, user_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sessions_user_date ON sessions(user_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_item ON sessions(item_id);
CREATE INDEX IF NOT EXISTS idx_items_user_active ON items(user_id, is_active);
CREATE INDEX IF NOT EXISTS idx_items_language_type ON items(language_code, type);

-- Enable Row Level Security
ALTER TABLE languages ENABLE ROW LEVEL SECURITY;
ALTER TABLE items ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE config ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own languages" ON languages;
DROP POLICY IF EXISTS "Users can insert their own languages" ON languages;
DROP POLICY IF EXISTS "Users can update their own languages" ON languages;
DROP POLICY IF EXISTS "Users can delete their own languages" ON languages;

DROP POLICY IF EXISTS "Users can view their own items" ON items;
DROP POLICY IF EXISTS "Users can insert their own items" ON items;
DROP POLICY IF EXISTS "Users can update their own items" ON items;
DROP POLICY IF EXISTS "Users can delete their own items" ON items;

DROP POLICY IF EXISTS "Users can view their own sessions" ON sessions;
DROP POLICY IF EXISTS "Users can insert their own sessions" ON sessions;
DROP POLICY IF EXISTS "Users can update their own sessions" ON sessions;
DROP POLICY IF EXISTS "Users can delete their own sessions" ON sessions;

DROP POLICY IF EXISTS "Users can view their own config" ON config;
DROP POLICY IF EXISTS "Users can insert their own config" ON config;
DROP POLICY IF EXISTS "Users can update their own config" ON config;
DROP POLICY IF EXISTS "Users can delete their own config" ON config;

-- Languages RLS policies
CREATE POLICY "Users can view their own languages" ON languages
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can insert their own languages" ON languages
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own languages" ON languages
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete their own languages" ON languages
    FOR DELETE USING (user_id = auth.uid());

-- Items RLS policies
CREATE POLICY "Users can view their own items" ON items
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can insert their own items" ON items
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own items" ON items
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete their own items" ON items
    FOR DELETE USING (user_id = auth.uid());

-- Sessions RLS policies
CREATE POLICY "Users can view their own sessions" ON sessions
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can insert their own sessions" ON sessions
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own sessions" ON sessions
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete their own sessions" ON sessions
    FOR DELETE USING (user_id = auth.uid());

-- Config RLS policies
CREATE POLICY "Users can view their own config" ON config
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can insert their own config" ON config
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own config" ON config
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete their own config" ON config
    FOR DELETE USING (user_id = auth.uid());

-- Create trigger for updating updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions;
CREATE TRIGGER update_sessions_updated_at 
    BEFORE UPDATE ON sessions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert default languages
INSERT INTO languages (code, name, description, color) VALUES
    ('python', 'Python', 'High-level programming language', '#3776ab'),
    ('javascript', 'JavaScript', 'Dynamic programming language for web', '#f7df1e'),
    ('html', 'HTML/CSS', 'Markup and styling for web pages', '#e34f26'),
    ('react', 'React', 'JavaScript library for building UIs', '#61dafb'),
    ('nodejs', 'Node.js', 'JavaScript runtime environment', '#339933'),
    ('sql', 'SQL', 'Database query language', '#336791'),
    ('git', 'Git', 'Version control system', '#f05032'),
    ('django', 'Django', 'Python web framework', '#092e20'),
    ('flask', 'Flask', 'Lightweight Python web framework', '#000000'),
    ('vue', 'Vue.js', 'Progressive JavaScript framework', '#4fc08d')
ON CONFLICT (code) DO NOTHING;

-- Insert default configuration
INSERT INTO config (key, value_json) VALUES
    ('difficulty_weights', '{"Beginner": 1.0, "Intermediate": 1.5, "Advanced": 2.0, "Expert": 2.5}'),
    ('status_multipliers', '{"Planned": 1.0, "In Progress": 1.1, "Completed": 1.2, "Blocked": 0.8}'),
    ('ui_limits', '{"max_hours_per_session": 24, "min_hours_per_session": 0.25}')
ON CONFLICT (key, user_id) DO NOTHING;

-- Create view for session details with item information
CREATE OR REPLACE VIEW session_details AS
SELECT 
    s.*,
    i.language_code,
    i.type as item_type,
    i.canonical_name as item_name,
    i.target_hours,
    l.name as language_name,
    l.color as language_color
FROM sessions s
JOIN items i ON s.item_id = i.id
JOIN languages l ON i.language_code = l.code
WHERE s.user_id = auth.uid();

-- Function to calculate session points
CREATE OR REPLACE FUNCTION calculate_session_points(
    hours_spent DECIMAL,
    difficulty TEXT DEFAULT 'Beginner',
    status TEXT DEFAULT 'In Progress'
)
RETURNS DECIMAL
LANGUAGE plpgsql
AS $$
DECLARE
    difficulty_weight DECIMAL := 1.0;
    status_multiplier DECIMAL := 1.0;
BEGIN
    -- Get difficulty weight
    CASE difficulty
        WHEN 'Beginner' THEN difficulty_weight := 1.0;
        WHEN 'Intermediate' THEN difficulty_weight := 1.5;
        WHEN 'Advanced' THEN difficulty_weight := 2.0;
        WHEN 'Expert' THEN difficulty_weight := 2.5;
        ELSE difficulty_weight := 1.0;
    END CASE;
    
    -- Get status multiplier
    CASE status
        WHEN 'Planned' THEN status_multiplier := 1.0;
        WHEN 'In Progress' THEN status_multiplier := 1.1;
        WHEN 'Completed' THEN status_multiplier := 1.2;
        WHEN 'Blocked' THEN status_multiplier := 0.8;
        ELSE status_multiplier := 1.0;
    END CASE;
    
    RETURN hours_spent * difficulty_weight * status_multiplier;
END;
$$;

-- Trigger to automatically calculate points on insert/update
CREATE OR REPLACE FUNCTION calculate_points_trigger()
RETURNS TRIGGER AS $$
BEGIN
    NEW.points_awarded = calculate_session_points(
        NEW.hours_spent,
        NEW.difficulty,
        NEW.status
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS sessions_calculate_points ON sessions;
CREATE TRIGGER sessions_calculate_points
    BEFORE INSERT OR UPDATE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION calculate_points_trigger();

-- Function to update item statistics
CREATE OR REPLACE FUNCTION update_item_stats(item_id INTEGER)
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    total_hours DECIMAL;
    total_sessions INTEGER;
    latest_session DATE;
BEGIN
    -- Calculate totals
    SELECT 
        COALESCE(SUM(hours_spent), 0),
        COUNT(*),
        MAX(date)
    INTO total_hours, total_sessions, latest_session
    FROM sessions 
    WHERE item_id = update_item_stats.item_id AND user_id = auth.uid();
    
    -- Update item
    UPDATE items 
    SET 
        total_hours = total_hours,
        total_logs = total_sessions,
        last_logged_at = latest_session,
        updated_at = NOW()
    WHERE id = update_item_stats.item_id AND user_id = auth.uid();
END;
$$;

-- Trigger to update item stats when sessions change
CREATE OR REPLACE FUNCTION update_item_stats_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        PERFORM update_item_stats(NEW.item_id);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        PERFORM update_item_stats(OLD.item_id);
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS sessions_update_item_stats ON sessions;
CREATE TRIGGER sessions_update_item_stats
    AFTER INSERT OR UPDATE OR DELETE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_item_stats_trigger();
