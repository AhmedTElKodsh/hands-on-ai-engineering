-- Initialization script for PostgreSQL database
-- Runs on first container startup

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgvector extension (for Week 6+)
-- CREATE EXTENSION IF NOT EXISTS "vector";

-- Create enum types
CREATE TYPE conversation_status AS ENUM ('active', 'archived', 'deleted');
CREATE TYPE message_role AS ENUM ('user', 'assistant', 'system');

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'Database initialization complete';
    RAISE NOTICE 'Extensions: uuid-ossp enabled';
    RAISE NOTICE 'Types: conversation_status, message_role created';
END $$;
