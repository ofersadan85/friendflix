import sqlite3

from db.db import get_db
from flask import Blueprint, request

actions_bp = Blueprint("actions", __name__)


@actions_bp.route("/actions")
def do_action():
    user_id = 1  # ! TODO: User ID Should come from JWT
    movie_id = request.args["movie_id"]
    action_type = request.args["action"]
    db = get_db()
    cursor = db.cursor()
    params = [user_id, movie_id, action_type]
    try:
        cursor.execute("INSERT INTO user_actions (user_id, movie_id, action_type) VALUES (?, ? ,?)", params)
    except sqlite3.IntegrityError:
        cursor.execute("DELETE FROM user_actions WHERE user_id=? AND movie_id=? AND action_type=?", params)
    finally:
        db.commit()
    return "", 202
