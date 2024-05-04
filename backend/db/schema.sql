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
    filetype TEXT NOT NULL CHECK (filetype IN ('movie', 'song', 'episode', 'picture')),
    fileSize INTEGER NOT NULL,
    createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expirationDate TIMESTAMP,
    description TEXT,  -- Corrected typo here
    owner INTEGER NOT NULL,
    FOREIGN KEY (owner) REFERENCES users(id)
);

