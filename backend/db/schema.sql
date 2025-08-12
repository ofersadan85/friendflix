DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created timestamp DEFAULT NOW(),
    edited timestamp DEFAULT NOW(),
    last_login timestamp,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    enabled BOOLEAN DEFAULT TRUE,
    verified BOOLEAN DEFAULT FALSE
);
