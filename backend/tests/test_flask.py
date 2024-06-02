from main import app
from dotenv import load_dotenv
from unittest import mock

fake_movies_data = {
  "page": 1,
  "results": [
    {
      "adult": False,
      "backdrop_path": "/vL5LR6WdxWPjLPFRLe133jXWsh5.jpg",
      "genre_ids": [28, 12, 14, 878],
      "id": 19995,
      "original_language": "en",
      "original_title": "Avatar",
      "overview": "In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.",
      "popularity": 135.342,
      "poster_path": "/kyeqWdyUXW608qlYkRqosgbbJyK.jpg",
      "release_date": "2009-12-15",
      "title": "Avatar",
      "video": False,
      "vote_average": 7.581,
      "vote_count": 30898
    },
    {
      "adult": False,
      "backdrop_path": "/7RyHsO4yDXtBv1zUU3mTpHeQ0d5.jpg",
      "genre_ids": [12, 878, 28],
      "id": 299534,
      "original_language": "en",
      "original_title": "Avengers: Endgame",
      "overview": "After the devastating events of Avengers: Infinity War, the universe is in ruins due to the efforts of the Mad Titan, Thanos. With the help of remaining allies, the Avengers must assemble once more in order to undo Thanos' actions and restore order to the universe once and for all, no matter what consequences may be in store.",
      "popularity": 240.198,
      "poster_path": "/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
      "release_date": "2019-04-24",
      "title": "Avengers: Endgame",
      "video": False,
      "vote_average": 8.253,
      "vote_count": 24931
    }
  ]
}

def test_movies():
    with mock.patch("httpx.get") as mock_get:
        mock_get.return_value.reponse_code = 200
        mock_get.return_value.json.return_value = fake_movies_data

        client = app.test_client()
        response = client.get("/movies")
        data = response.json
        assert isinstance(data, dict)
        movies = data.get("results")
        assert isinstance(movies, list)
        assert len(movies) == 2
        for movie in movies:
            assert movie["watched"] is not None

        movie_id = fake_movies_data["results"][0]["id"]
        client.get(f"/actions?movie_id={movie_id}&action=play")
        response2 = client.get("/movies")
        data2 = response2.json
        assert data != data2
        mock_get.assert_called_once()


def test_movie_with_id():
    with mock.patch("httpx.get") as mock_get:
        mock_get.return_value.reponse_code = 200
        mock_get.return_value.json.return_value = fake_movies_data["results"][0]

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
