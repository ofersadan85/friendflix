import sqlite3

from db.db import DB_PATH
from db.user_actions import do_action


def test_do_action():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    params = [1, 2, "like"]
    cursor.execute("DELETE FROM user_actions WHERE user_id=? AND movie_id=? AND action=?", params)
    assert cursor.rowcount == 0

    do_action(*params, cursor=cursor)  # First action - adds the row
    cursor.execute("SELECT * FROM user_actions WHERE user_id=? AND movie_id=? AND action=?", params)
    rows = cursor.fetchall()
    assert len(rows) == 1

    do_action(*params, cursor=cursor)  # Second action - deletes the row
    cursor.execute("SELECT * FROM user_actions WHERE user_id=? AND movie_id=? AND action=?", params)
    rows = cursor.fetchall()
    assert len(rows) == 0

    db.close()
