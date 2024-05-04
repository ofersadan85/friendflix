import sqlite3
from pathlib import Path

CURRENT_FOLDER = Path(__file__).parent
DB_PATH = CURRENT_FOLDER / "db.sqlite"

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
