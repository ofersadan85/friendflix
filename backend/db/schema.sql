DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type TEXT NOT NULL DEFAULT 'user'
);
DROP TABLE IF EXISTS files;
CREATE TABLE IF NOT EXISTS files(
    id INTEGER PRIMARY KEY NOT NULL,
    filename TEXT NOT NULL,
    filetype TEXT NOT NULL CHECK (
        filetype IN ('movie', 'song', 'episode', 'picture')
    ),
    filesize INTEGER NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expired TIMESTAMP,
    description TEXT,
    owner INTEGER NOT NULL,
    FOREIGN KEY (owner) REFERENCES users(id)
);
DROP TABLE IF EXISTS credits;
CREATE TABLE IF NOT EXISTS credits (
    id INTEGER PRIMARY KEY NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT NOT NULL UNIQUE,
    amount INTEGER DEFAULT 0,
    reason TEXT
);
DROP TABLE IF EXISTS files_share;
CREATE TABLE IF NOT EXISTS files_share (
    id INTEGER PRIMARY KEY NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shared_by TEXT NOT NULL UNIQUE,
    shared_with TEXT NOT NULL,
    file_id TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS user_actions;
CREATE TABLE IF NOT EXISTS user_actions (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    action_type TEXT NOT NULL,
    PRIMARY KEY (user_id, movie_id, action_type),
    FOREIGN KEY (user_id) REFERENCES users(id)
);