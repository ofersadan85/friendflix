from main import app
from dotenv import load_dotenv


def test_movies():
    client = app.test_client()
    response = client.get("/movies")
    data = response.json
    assert isinstance(data, dict)
    movies = data.get("results")
    assert isinstance(movies, list)
    assert len(movies) == 20
    for movie in movies:
        assert movie["watched"] is not None


def test_movie_with_id():
    client = app.test_client()
    response = client.get("/movies/299536")
    data = response.json
    assert isinstance(data, dict)
    assert data["title"] == "Avengers: Infinity War"



def test_actions():
    client = app.test_client()
    response = client.get("/actions", query_string={"movie_id": 299536, "action": "play"})
    assert response.status_code == 202
    assert response.text == ""
