INSERT INTO users (username, email, password, role) VALUES
('alice123', 'alice@example.com', 'password123', 'user'),
('bob456', 'bob@example.com', 'password456', 'user'),
('charlie789', 'charlie@example.com', 'password789', 'admin'),
('diana101', 'diana@example.com', 'password101', 'user'),
('eve202', 'eve@example.com', 'password202', 'user');

INSERT INTO files (name, type, size, description, owner, hash) VALUES
('Inception', 'movie', 1500000, 'A mind-bending thriller', 1, 'abc123'),
('Bohemian Rhapsody', 'song', 5000, 'Iconic song by Queen', 2, 'def456'),
('Breaking Bad S1E1', 'episode', 600000, 'Pilot episode', 3, 'ghi789'),
('Sunset Picture', 'image', 2000, 'Beautiful sunset', 4, 'jkl012'),
('Document.pdf', 'document', 300, 'Important document', 5, 'mno345');

INSERT INTO credits (user_id, amount, reason) VALUES
(2, 100, 'Initial bonus'),
(3, 50, 'Monthly reward'),
(4, 200, 'Admin privileges'),
(5, 75, 'Content contribution'),
(6, 150, 'Moderator activities');

INSERT INTO files_share (shared_by, shared_with, file_id) VALUES
(2, 2, 1),
(3, 3, 2),
(4, 4, 3),
(5, 5, 4),
(6, 1, 5);

INSERT INTO user_actions (user_id, movie_id, action) VALUES
(2, 1, 'like'),
(3, 2, 'favorite'),
(4, 3, 'watchlist'),
(5, 4, 'comment'),
(6, 5, 'rate');

INSERT INTO discussions (user_id, file_id, comment, tmdb_movie_id) VALUES
(2, 1, 'Amazing movie! The plot twists are incredible.', NULL),
(3, 2, 'This song never gets old.', NULL),
(4, 3, 'Breaking Bad is a masterpiece.', NULL),
(5, 4, 'I love the colors in this picture.', NULL),
(6, NULL, 'Excited for the new Marvel movie!', 12345),
(2, NULL, 'Has anyone watched the latest Star Wars?', 67890);

INSERT INTO discussions (user_id, tmdb_movie_id, comment) VALUES
(2, 550, 'Fight Club is a classic.'),
(3, 680, 'Pulp Fiction has such great dialogue.'),
(4, 27205, 'Inception always blows my mind.'),
(5, 299536, 'Avengers: Infinity War was epic.'),
(1, 155, 'The Dark Knight is my favorite Batman movie.');
