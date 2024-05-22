import sqlite3


def do_action(user_id, movie_id, action_type, cursor):
    params = [user_id, movie_id, action_type]
    try:
        cursor.execute("INSERT INTO user_actions (user_id, movie_id, action_type) VALUES (?, ? ,?)", params)
    except sqlite3.IntegrityError:
        cursor.execute("DELETE FROM user_actions WHERE user_id=? AND movie_id=? AND action_type=?", params)
    finally:
        cursor.connection.commit()
