import sqlite3
from pathlib import Path

from flask import g

CURRENT_FOLDER = Path(__file__).parent
DB_PATH = CURRENT_FOLDER / "db.sqlite"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    schema = CURRENT_FOLDER / "schema.sql"
    schema = schema.read_text()
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.executescript(schema)
    db.commit()
    db.close()


if __name__ == "__main__":
    init_db()
