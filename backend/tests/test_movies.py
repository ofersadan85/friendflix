from datetime import datetime
from unittest import mock

import pytest
from flask_jwt_extended import create_access_token
from main import app
from models.auth import User
from tests.mock_tmdb import test_movies_data, test_one_movie_data

admin = User(1, "test_admin", "admin@example.com", datetime.now(), datetime.now(), "admin")
user = User(2, "test_user", "test@example.com", datetime.now(), datetime.now(), "user")


@pytest.fixture
def logged_in_admin():
    with app.app_context():
        return {"token": create_access_token(identity=admin.id, additional_claims=admin.asdict())}


@pytest.fixture
def logged_in_user():
    with app.app_context():
        return {"token": create_access_token(identity=user.id, additional_claims=user.asdict())}


def test_top_movies_cached():
    with mock.patch("httpx.get") as mock_get:
        mock_get.return_value.response_code = 200
        mock_get.return_value.json.return_value = test_movies_data
        client = app.test_client()
        for _ in range(5):
            client.get("/movies/top")
        mock_get.assert_called_once()


def test_top_movies_watched(logged_in_user):
    with mock.patch("httpx.get") as mock_get:
        mock_get.return_value.response_code = 200
        mock_get.return_value.json.return_value = test_movies_data

        # Not logged in
        client = app.test_client()
        response = client.get("/movies/top")
        assert isinstance(response.json, dict)
        movies = response.json["results"]
        for movie in movies:
            assert "watched" not in movie.keys(), "watched key added to non-user"

        # Logged in user
        client = app.test_client()
        token = logged_in_user["token"]
        response = client.get("/movies/top", headers={"Authorization": f"Bearer {token}"})
        assert isinstance(response.json, dict)
        movies = response.json["results"]
        for movie in movies:
            assert "watched" in movie.keys() and movie["watched"] is not None, "watched key not added to user"


def test_movie_with_id(logged_in_user):
    with mock.patch("httpx.get") as mock_get:
        mock_get.return_value.response_code = 200
        mock_get.return_value.json.return_value = test_one_movie_data

        # Not logged in
        client = app.test_client()
        response = client.get("/movies/299536")
        movie = response.json
        assert isinstance(movie, dict)
        assert movie["title"] == test_one_movie_data["title"]
        assert "watched" not in movie.keys(), "watched key added to non-user"

        # Logged in user
        client = app.test_client()
        token = logged_in_user["token"]
        response = client.get("/movies/299536", headers={"Authorization": f"Bearer {token}"})
        movie = response.json
        assert isinstance(movie, dict)
        assert movie["title"] == test_one_movie_data["title"]
        assert "watched" in movie.keys() and movie["watched"] is not None, "watched key not added to user"


def test_actions(logged_in_user):
    client = app.test_client()
    token = logged_in_user["token"]
    response = client.get(
        "/actions",
        query_string={"movie_id": 299536, "action": "play"},
    )
    assert response.status_code == 401
    assert "Missing Authorization Header" in response.text

    client = app.test_client()
    response = client.get(
        "/actions",
        query_string={"movie_id": 299536, "action": "play"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 202
    assert response.text == ""
