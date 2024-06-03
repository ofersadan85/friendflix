import json
from pathlib import Path

test_movies_data = json.loads(Path("tests/data/movies_by_revenue.json").read_text("utf-8"))
test_one_movie_data = test_movies_data["results"][0]
