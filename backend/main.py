# from flask_jwt_extended import JWTManager
import tmdb
from db.db import close_db, get_db
from db.user_actions import add_watched_status_to_movies
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from views.user_actions import actions_bp

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.register_blueprint(actions_bp)
load_dotenv()
app.config.from_prefixed_env()
FRONTEND_URL = app.config["FRONTEND_URL"]
cors = CORS(app, origins=FRONTEND_URL, methods=["GET", "POST", "DELETE"])
# jwt = JWTManager(app)


@app.route("/movies")
def get_movies():
    user_id = 1  # ! TODO: User ID Should come from JWT
    db = get_db()
    cursor = db.cursor()
    movies_data = tmdb.get_movie_list()
    movies_data = add_watched_status_to_movies(movies_data, user_id, cursor)
    return movies_data


@app.route("/movies/<id>")
def get_full_movie(id: int):
    movie_data = tmdb.get_full_movie(id)
    return movie_data
