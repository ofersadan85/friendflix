from db import get_db
from flask import Blueprint, request
from flask_jwt_extended import get_jwt, jwt_required
from models.user import do_action as do_action_db
from models.user import get_user_movies

actions_bp = Blueprint("actions", __name__)


@actions_bp.route("/actions")
@jwt_required()
def do_action() -> tuple[str, int]:
    user = get_jwt()
    movie_id = int(request.args["movie_id"])
    action = request.args["action"]
    do_action_db(user["id"], movie_id, action, get_db().cursor())
    return "", 202


@actions_bp.route("/user/<int:user_id>/watchlist")
@jwt_required()
def get_user_watchlist(user_id: int) -> list[int]:
    return get_user_movies(user_id, "watchlist", get_db().cursor())
