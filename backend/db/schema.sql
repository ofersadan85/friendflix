DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created timestamp DEFAULT NOW(),
    edited timestamp DEFAULT NOW(),
    last_login timestamp,
    role TEXT NOT NULL DEFAULT 'user'
);

DROP TABLE IF EXISTS files CASCADE;
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (
        type IN ('movie', 'song', 'episode', 'image', 'clip', 'document', 'other')
    ),
    size INTEGER NOT NULL,
    created timestamp DEFAULT NOW(),
    expired timestamp,
    description TEXT,
    owner INTEGER NOT NULL,
    hash TEXT,
    FOREIGN KEY (owner) REFERENCES users(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS credits CASCADE;
CREATE TABLE IF NOT EXISTS credits (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    created timestamp NOT NULL DEFAULT NOW(),
    user_id INTEGER NOT NULL,
    amount INTEGER DEFAULT 0,
    reason TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS files_share CASCADE;
CREATE TABLE IF NOT EXISTS files_share (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    created timestamp DEFAULT NOW(),
    shared_by INTEGER NOT NULL,
    shared_with INTEGER NOT NULL,
    file_id INTEGER NOT NULL,
    FOREIGN KEY (shared_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (shared_with) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS user_actions CASCADE;
CREATE TABLE IF NOT EXISTS user_actions (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    action TEXT NOT NULL CHECK (
        action IN ('like', 'dislike', 'play', 'favorite', 'watchlist', 'comment', 'rate', 'share')
    ),
    action_timestamp timestamp DEFAULT NOW(),
    PRIMARY KEY (user_id, movie_id, action),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES files(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS discussions CASCADE;
CREATE TABLE IF NOT EXISTS discussions (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id INTEGER NOT NULL,
    file_id INTEGER,
    tmdb_movie_id INTEGER,
    comment TEXT NOT NULL,
    created timestamp DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
    CHECK ((file_id IS NOT NULL) OR (tmdb_movie_id IS NOT NULL)),
    CHECK ((file_id IS NULL) OR (tmdb_movie_id IS NULL))
);
