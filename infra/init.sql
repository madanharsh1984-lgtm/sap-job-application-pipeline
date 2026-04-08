-- JobAccelerator AI Database Initialization
-- This script runs on first database creation

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for performance
-- (Tables are created by Alembic migrations, this is for additional setup)

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE jobaccelerator TO postgres;
