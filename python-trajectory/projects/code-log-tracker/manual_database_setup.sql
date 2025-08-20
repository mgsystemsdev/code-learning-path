-- Manual Database Setup for Supabase
-- Copy and paste these into your Supabase SQL Editor: 
-- https://supabase.com/dashboard/project/ehpnpjsrghlyeqafzora/sql

-- 1. Create languages table
CREATE TABLE IF NOT EXISTS public.languages (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    color TEXT DEFAULT '#6c757d',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) DEFAULT NULL
);

-- 2. Create items table
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

-- 3. Create sessions table
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

-- 4. Create config table
CREATE TABLE IF NOT EXISTS public.config (
    id BIGSERIAL PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    value_json TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) DEFAULT NULL
);

-- 5. Enable Row Level Security
ALTER TABLE public.languages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.config ENABLE ROW LEVEL SECURITY;

-- 6. Create security policies
CREATE POLICY IF NOT EXISTS "languages_public_read" ON public.languages
FOR SELECT USING (true);

CREATE POLICY IF NOT EXISTS "languages_user_write" ON public.languages
FOR ALL USING (auth.uid() IS NOT NULL);

CREATE POLICY IF NOT EXISTS "items_user_access" ON public.items
FOR ALL USING (user_id = auth.uid());

CREATE POLICY IF NOT EXISTS "sessions_user_access" ON public.sessions
FOR ALL USING (user_id = auth.uid());

CREATE POLICY IF NOT EXISTS "config_public_read" ON public.config
FOR SELECT USING (user_id IS NULL OR user_id = auth.uid());

CREATE POLICY IF NOT EXISTS "config_user_write" ON public.config
FOR ALL USING (user_id = auth.uid() OR auth.uid() IS NOT NULL);

-- 7. Insert default languages
INSERT INTO public.languages (code, name, description, color) VALUES
('python', 'Python', 'General-purpose programming language', '#3776ab'),
('javascript', 'JavaScript', 'Dynamic programming language for web', '#f7df1e'),
('html', 'HTML/CSS', 'Markup and styling languages', '#e34f26'),
('sql', 'SQL', 'Database query language', '#336791'),
('git', 'Git/DevOps', 'Version control and deployment', '#f05032'),
('general', 'General/Theory', 'Programming concepts and theory', '#6c757d'),
('react', 'React', 'JavaScript library for UIs', '#61dafb'),
('typescript', 'TypeScript', 'Typed superset of JavaScript', '#3178c6')
ON CONFLICT (code) DO NOTHING;

-- 8. Insert default configuration
INSERT INTO public.config (key, value_json) VALUES
('difficulty_weights', '{"Beginner": 1.0, "Intermediate": 1.5, "Advanced": 2.0, "Expert": 2.5}'),
('status_multipliers', '{"Planned": 1.0, "In Progress": 1.1, "Completed": 1.2, "Blocked": 0.8}'),
('ui_limits', '{"max_hours_per_session": 24, "min_hours_per_session": 0.25}')
ON CONFLICT (key) DO NOTHING;

-- 9. Create performance indexes
CREATE INDEX IF NOT EXISTS idx_languages_active ON public.languages(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_items_user_language ON public.items(user_id, language_code);
CREATE INDEX IF NOT EXISTS idx_sessions_user_date ON public.sessions(user_id, date DESC);

-- Success message
SELECT 'Database setup completed successfully! ✅' as status;
