from psycopg2.errors import IntegrityError
from psycopg2.extras import DictCursor


def add_watched_status_to_movies(movies_data: dict, user_id: int, cursor: DictCursor) -> dict:
    cursor.execute("SELECT movie_id FROM user_actions WHERE user_id=%s AND action='play'", [user_id])
    watched_ids = [row[0] for row in cursor.fetchall()]
    single_movie = "results" not in movies_data.keys()
    if single_movie:
        movies_data["watched"] = movies_data["id"] in watched_ids
        return movies_data
    for movie in movies_data["results"]:
        movie["watched"] = movie["id"] in watched_ids
    return movies_data["results"][0] if single_movie else movies_data


def do_action(user_id: int, movie_id: int, action_type: str, cursor: DictCursor) -> None:
    params = [user_id, movie_id, action_type]
    try:
        cursor.execute("INSERT INTO user_actions (user_id, movie_id, action) VALUES (%s, %s ,%s)", params)
    except IntegrityError:
        cursor.execute("DELETE FROM user_actions WHERE user_id=%s AND movie_id=%s AND action=%s", params)


def get_user_movies(user_id: int, action: str, cursor: DictCursor) -> list[int]:
    cursor.execute("SELECT movie_id FROM user_actions WHERE user_id=%s AND action=%s", [user_id, action])
    return [row[0] for row in cursor.fetchall()]
