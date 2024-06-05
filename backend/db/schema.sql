DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    edited DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    role TEXT NOT NULL DEFAULT 'user'
);

DROP TABLE IF EXISTS files;
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (
        type IN ('movie', 'song', 'episode', 'image', 'clip', 'document', 'other')
    ),
    size INTEGER NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    expired DATETIME,
    description TEXT,
    owner INTEGER NOT NULL,
    hash TEXT,
    FOREIGN KEY (owner) REFERENCES users(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS credits;
CREATE TABLE IF NOT EXISTS credits (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    amount INTEGER DEFAULT 0,
    reason TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS files_share;
CREATE TABLE IF NOT EXISTS files_share (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    shared_by INTEGER NOT NULL,
    shared_with INTEGER NOT NULL,
    file_id INTEGER NOT NULL,
    FOREIGN KEY (shared_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (shared_with) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS user_actions;
CREATE TABLE IF NOT EXISTS user_actions (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    action TEXT NOT NULL CHECK (
        action IN ('like', 'dislike', 'play', 'favorite', 'watchlist', 'comment', 'rate', 'share')
    ),
    action_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, movie_id, action),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES files(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS discussions;
CREATE TABLE IF NOT EXISTS discussions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    file_id INTEGER,
    tmdb_movie_id INTEGER,
    comment TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
    CHECK ((file_id IS NOT NULL) OR (tmdb_movie_id IS NOT NULL)),
    CHECK ((file_id IS NULL) OR (tmdb_movie_id IS NULL))
);
