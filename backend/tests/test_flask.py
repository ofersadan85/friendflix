from unittest import mock

from main import app
from tests.mock_tmdb import test_movies_data, test_one_movie_data


def test_movies():
    with mock.patch("httpx.get") as mock_get:
        mock_get.return_value.response_code = 200
        mock_get.return_value.json.return_value = test_movies_data

        client = app.test_client()
        response = client.get("/movies")
        data = response.json
        assert isinstance(data, dict)
        movies = data.get("results")
        assert isinstance(movies, list)
        assert len(movies) == 20
        for movie in movies:
            assert movie["watched"] is not None

        movie_id = test_movies_data["results"][0]["id"]
        client.get(f"/actions?movie_id={movie_id}&action=play")
        response2 = client.get("/movies")
        data2 = response2.json
        assert data != data2
        mock_get.assert_called_once()


def test_movie_with_id():
    with mock.patch("httpx.get") as mock_get:
        mock_get.return_value.response_code = 200
        mock_get.return_value.json.return_value = test_one_movie_data

        client = app.test_client()
        response = client.get("/movies/299536")
        data = response.json
        assert isinstance(data, dict)
        assert data["title"] == "Avatar"


def test_actions():
    client = app.test_client()
    response = client.get("/actions", query_string={"movie_id": 299536, "action": "play"})
    assert response.status_code == 202
    assert response.text == ""
