import logging
import random
import string
from pathlib import Path

import psycopg2
import psycopg2.errors
from fastapi import Request
from psycopg2.extras import RealDictConnection, RealDictCursor

from models.auth import NewUser
from settings import app_settings

logger = logging.getLogger("uvicorn")


def load_query(name: str) -> str:
    if not name.endswith(".sql"):
        name = name + ".sql"
    return (Path("db") / name).read_text()


def db_connect() -> RealDictConnection:
    return psycopg2.connect(dsn=str(app_settings.db_address), connection_factory=RealDictConnection)


def get_db(request: Request) -> RealDictCursor:
    if hasattr(request.app.state, "db"):
        db = request.app.state.db
    else:
        db = db_connect()
        db.autocommit = True
        request.app.state.db = db
    try:
        cursor = db.cursor()
    except psycopg2.InterfaceError:
        delattr(request.app.state, "db")
        raise
    return cursor


def init_db():
    db = db_connect()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM users LIMIT 1")
    except psycopg2.errors.UndefinedTable:
        logger.info("Database not found, creating new one")
        db.rollback()
    else:
        logger.info("Database already exists, skipping creation")
        return

    password = app_settings.initial_admin_password or "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(16)
    )
    cursor.execute(load_query("schema"))
    new_user = NewUser(
        username=app_settings.initial_admin_username,
        password=password,
        email=app_settings.initial_admin_email,
        role="admin",
    )
    new_user.register(cursor)
    logger.info(
        f"""
            *********************************************************
            Created initial admin user `{app_settings.initial_admin_username}` with password: {password}
            Don't forget to change the password on your first login!
            *********************************************************
            """
    )

    if app_settings.create_examples:
        logger.info("Creating example data")
        examples = Path("db/examples.sql").read_text()
        cursor.execute(examples)
    db.commit()
