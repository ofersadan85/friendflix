import sqlite3

from db.user_actions import do_action

from db.db import DB_PATH


def test_do_action():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    params = [1, 2, "like"]
    cursor.execute("DELETE FROM user_actions WHERE user_id=? AND movie_id=? AND action_type=?", params)
    assert cursor.rowcount == 0
    db.commit()  # We commit here to fix later tests if this row exists

    do_action(*params, cursor=cursor)  # First action - adds the row
    cursor.execute("SELECT * FROM user_actions WHERE user_id=? AND movie_id=? AND action_type=?", params)
    rows = cursor.fetchall()
    assert len(rows) == 1

    do_action(*params, cursor=cursor)  # Second action - deletes the row
    cursor.execute("SELECT * FROM user_actions WHERE user_id=? AND movie_id=? AND action_type=?", params)
    rows = cursor.fetchall()
    assert len(rows) == 0

    db.close()
