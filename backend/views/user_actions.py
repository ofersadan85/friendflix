import sqlite3

from db.db import get_db
from db.user_actions import do_action as do_action_db
from flask import Blueprint, request

actions_bp = Blueprint("actions", __name__)


@actions_bp.route("/actions")
def do_action():
    user_id = 1  # ! TODO: User ID Should come from JWT
    movie_id = request.args["movie_id"]
    action_type = request.args["action"]
    db = get_db()
    cursor = db.cursor()
    do_action_db(user_id, movie_id, action_type, cursor)
    return "", 202
