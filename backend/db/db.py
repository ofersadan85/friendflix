import os
import psycopg2
from psycopg2.extras import DictCursor
from pathlib import Path

from flask import g

CURRENT_FOLDER = Path(__file__).parent
DB_HOST=os.getenv("DB_HOST", "localhost")

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password",
            host=DB_HOST,
            port=5432,
            cursor_factory=DictCursor
        )
        g.db.autocommit = True
    return g.db


def close_db(_e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
