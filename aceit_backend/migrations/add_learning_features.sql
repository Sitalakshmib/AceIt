-- Database Migration Script for Learning Features
-- Run this script on Neon DB to add new tables and columns

-- 1. Create bookmarked_problems table
CREATE TABLE IF NOT EXISTS bookmarked_problems (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    problem_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, problem_id)
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_bookmarked_user_id ON bookmarked_problems(user_id);
CREATE INDEX IF NOT EXISTS idx_bookmarked_problem_id ON bookmarked_problems(problem_id);

-- 2. Add solution fields to coding_problems table
ALTER TABLE coding_problems 
ADD COLUMN IF NOT EXISTS solution_code TEXT,
ADD COLUMN IF NOT EXISTS solution_explanation TEXT,
ADD COLUMN IF NOT EXISTS approach_summary TEXT,
ADD COLUMN IF NOT EXISTS time_complexity VARCHAR(100),
ADD COLUMN IF NOT EXISTS space_complexity VARCHAR(100);

-- 3. Add test case descriptions field
ALTER TABLE coding_problems 
ADD COLUMN IF NOT EXISTS test_case_descriptions JSONB;

-- Verify tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('bookmarked_problems', 'coding_problems');
