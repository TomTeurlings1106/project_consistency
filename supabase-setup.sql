-- Personal Habit Tracker Database Schema
-- Run this in your Supabase SQL editor

-- Core habit tracking
CREATE TABLE habits (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    target_frequency INTEGER DEFAULT 1, -- times per day/week
    frequency_type VARCHAR(20) DEFAULT 'daily', -- daily, weekly, monthly
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE habit_logs (
    id BIGSERIAL PRIMARY KEY,
    habit_id BIGINT REFERENCES habits(id) ON DELETE CASCADE,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT,
    value DECIMAL, -- for quantifiable habits
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Garmin data integration
CREATE TABLE garmin_sleep (
    id BIGSERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    duration_minutes INTEGER, -- total sleep time
    deep_sleep_minutes INTEGER,
    light_sleep_minutes INTEGER,
    rem_sleep_minutes INTEGER,
    awake_minutes INTEGER,
    sleep_score INTEGER, -- 0-100 if available
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE garmin_activities (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    duration_minutes INTEGER,
    calories INTEGER,
    distance_meters DECIMAL,
    heart_rate_avg INTEGER,
    heart_rate_max INTEGER,
    activity_start TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE garmin_steps (
    id BIGSERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    steps INTEGER NOT NULL,
    goal INTEGER DEFAULT 10000,
    distance_meters DECIMAL,
    floors_climbed INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE garmin_heart_rate (
    id BIGSERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    resting_hr INTEGER,
    max_hr INTEGER,
    avg_hr INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Daily logging and reflection
CREATE TABLE daily_logs (
    id BIGSERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    mood INTEGER CHECK (mood >= 1 AND mood <= 10), -- 1-10 scale
    energy INTEGER CHECK (energy >= 1 AND energy <= 10), -- 1-10 scale
    notes TEXT,
    highlights TEXT, -- best parts of the day
    challenges TEXT, -- difficulties faced
    tomorrow_goals TEXT, -- what to focus on tomorrow
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agenda and task management
CREATE TABLE agenda_items (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date TIMESTAMP WITH TIME ZONE,
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, urgent
    category VARCHAR(100),
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE reminders (
    id BIGSERIAL PRIMARY KEY,
    agenda_item_id BIGINT REFERENCES agenda_items(id) ON DELETE CASCADE,
    reminder_time TIMESTAMP WITH TIME ZONE NOT NULL,
    message TEXT,
    sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better performance
CREATE INDEX idx_habit_logs_habit_id ON habit_logs(habit_id);
CREATE INDEX idx_habit_logs_completed_at ON habit_logs(completed_at);
CREATE INDEX idx_garmin_sleep_date ON garmin_sleep(date);
CREATE INDEX idx_garmin_activities_date ON garmin_activities(date);
CREATE INDEX idx_garmin_steps_date ON garmin_steps(date);
CREATE INDEX idx_garmin_heart_rate_date ON garmin_heart_rate(date);
CREATE INDEX idx_daily_logs_date ON daily_logs(date);
CREATE INDEX idx_agenda_items_due_date ON agenda_items(due_date);
CREATE INDEX idx_reminders_reminder_time ON reminders(reminder_time);

-- Enable Row Level Security (RLS) for all tables
ALTER TABLE habits ENABLE ROW LEVEL SECURITY;
ALTER TABLE habit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE garmin_sleep ENABLE ROW LEVEL SECURITY;
ALTER TABLE garmin_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE garmin_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE garmin_heart_rate ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agenda_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE reminders ENABLE ROW LEVEL SECURITY;

-- Since this is for personal use, create policies that allow all operations
-- In production, you'd want more restrictive policies based on user authentication
CREATE POLICY "Allow all operations" ON habits FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON habit_logs FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON garmin_sleep FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON garmin_activities FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON garmin_steps FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON garmin_heart_rate FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON daily_logs FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON agenda_items FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON reminders FOR ALL USING (true);