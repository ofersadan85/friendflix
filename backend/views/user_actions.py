from db.db import get_db
from db.user_actions import do_action as do_action_db
from flask import Blueprint, request
from flask_jwt_extended import get_jwt, jwt_required

actions_bp = Blueprint("actions", __name__)


@actions_bp.route("/actions")
@jwt_required()
def do_action():
    user = get_jwt()
    movie_id = request.args["movie_id"]
    action_type = request.args["action"]
    db = get_db()
    cursor = db.cursor()
    do_action_db(user["id"], movie_id, action_type, cursor)
    return "", 202
