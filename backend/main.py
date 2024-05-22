
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import httpx

app = Flask(__name__)
load_dotenv()
app.config.from_prefixed_env()
FRONTEND_URL = app.config["FRONTEND_URL"]
cors = CORS(app, origins=FRONTEND_URL, methods=["GET", "POST", "DELETE"])
# jwt = JWTManager(app)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

@app.route("/movies")
def get_movies():
    url = f"{TMDB_BASE_URL}/discover/movie?&sort_by=revenue.desc&api_key={TMDB_API_KEY}"
    response = httpx.get(url)
    movies_data = response.json()
    return movies_data


@app.route("/movies/<id>")
def get_full_movie(id: int):
    url = f"{TMDB_BASE_URL}/movie/{id}?append_to_response=credits&language=en-US&api_key={TMDB_API_KEY}"
    response = httpx.get(url)
    movie_data = response.json()
    return movie_data
