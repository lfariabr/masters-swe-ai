-- transcripts table
CREATE TABLE transcripts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  transcript_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- curricula table  
CREATE TABLE curriculums (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  curriculum_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- sessions table
CREATE TABLE student_records (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  student_name TEXT DEFAULT 'Unknown Student',
  credit_points INTEGER DEFAULT 0,
  results_data JSONB,
  summary_data JSONB,
  electives_data JSONB,
  progress_data JSONB,
  created_at TIMESTAMP DEFAULT NOW()
  course_name TEXT,
  student_id TEXT,
);

-- Add NEW columns to student_records table
ALTER TABLE student_records 
ADD COLUMN course_name TEXT,
ADD COLUMN student_id TEXT;
