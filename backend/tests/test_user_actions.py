from db import get_db
from main import app
from models.user import do_action


def test_do_action():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        params = [1, 2, "like"]
        cursor.execute("DELETE FROM user_actions WHERE user_id=%s AND movie_id=%s AND action=%s", params)
        assert cursor.rowcount == 0

        do_action(*params, cursor=cursor)  # First action - adds the row
        cursor.execute("SELECT * FROM user_actions WHERE user_id=%s AND movie_id=%s AND action=%s", params)
        rows = cursor.fetchall()
        assert len(rows) == 1

        do_action(*params, cursor=cursor)  # Second action - deletes the row
        cursor.execute("SELECT * FROM user_actions WHERE user_id=%s AND movie_id=%s AND action=%s", params)
        rows = cursor.fetchall()
        assert len(rows) == 0
