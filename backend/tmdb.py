import os
from functools import cache, lru_cache

import httpx
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"


@cache
def get_movie_list():
    print("Fetching movie list data from TMDB")
    url = f"{TMDB_BASE_URL}/discover/movie?&sort_by=revenue.desc&api_key={TMDB_API_KEY}"
    response = httpx.get(url)
    movies_data = response.json()
    return movies_data


@lru_cache(maxsize=128)
def get_full_movie(id):
    print(f"Fetching full movie data from TMDB ({id})")
    url = f"{TMDB_BASE_URL}/movie/{id}?append_to_response=credits&language=en-US&api_key={TMDB_API_KEY}"
    response = httpx.get(url)
    movie_data = response.json()
    return movie_data
