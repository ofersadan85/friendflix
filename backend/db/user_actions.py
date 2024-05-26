import sqlite3

def add_watched_status_to_movies(movies_data, user_id, cursor):
    cursor.execute("SELECT movie_id FROM user_actions WHERE user_id=? AND action_type='play'", [user_id])
    watched_ids = [row[0] for row in cursor.fetchall()]
    for movie in movies_data["results"]:
        movie["watched"] = movie["id"] in watched_ids
    return movies_data


def do_action(user_id, movie_id, action_type, cursor):
    params = [user_id, movie_id, action_type]
    try:
        cursor.execute("INSERT INTO user_actions (user_id, movie_id, action_type) VALUES (?, ? ,?)", params)
    except sqlite3.IntegrityError:
        cursor.execute("DELETE FROM user_actions WHERE user_id=? AND movie_id=? AND action_type=?", params)
    finally:
        cursor.connection.commit()
