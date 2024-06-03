import tmdb
from db.db import get_db
from db.user_actions import add_watched_status_to_movies
from flask import Blueprint
from flask_jwt_extended import get_jwt, jwt_required

movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/movies/top")
@jwt_required(optional=True)
def get_movies():
    movies_data = tmdb.get_movie_list()
    user = get_jwt()
    if user:
        cursor = get_db().cursor()
        movies_data = add_watched_status_to_movies(movies_data, user["id"], cursor)
    return movies_data


@movies_bp.route("/movies/<id>")
@jwt_required(optional=True)
def get_full_movie(id: int):
    movie_data = tmdb.get_full_movie(id)
    user = get_jwt()
    if user:
        cursor = get_db().cursor()
        movie_data = add_watched_status_to_movies(movie_data, user["id"], cursor)
    return movie_data
