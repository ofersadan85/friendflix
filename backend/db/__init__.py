import os
from pathlib import Path

import psycopg2
from flask import Flask, g
from psycopg2.extras import DictConnection
from werkzeug.security import gen_salt

CURRENT_FOLDER = Path(__file__).parent


def get_db():
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "password")
    if "db" not in g:
        g.db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            connection_factory=DictConnection,
        )
        g.db.autocommit = True
    return g.db


def close_db(_e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app: Flask):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM users LIMIT 1")
    except psycopg2.errors.UndefinedTable:
        app.logger.info("Database not found, creating new one")
    else:
        app.logger.info("Database already exists, skipping creation")
        return

    with app.open_resource("db/schema.sql") as f:
        cursor.execute(f.read())

    initial_admin_username = app.config.get("INITIAL_ADMIN_USERNAME", "admin")
    initial_admin_email = app.config.get("INITIAL_ADMIN_EMAIL", "admin@example.com")
    random_password = gen_salt(16)
    initial_admin_password = app.config.get("INITIAL_ADMIN_PASSWORD", random_password)
    cursor.execute(
        "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
        [initial_admin_username, initial_admin_email, initial_admin_password, "admin"],
    )
    app.logger.info(
        f"""
            *********************************************************
            Created initial admin user `{initial_admin_username}` with password: {initial_admin_password}
            Don't forget to change the password on your first login!
            *********************************************************
            """
    )

    create_examples = app.config.get("CREATE_EXAMPLES", False)
    app.logger.info("Creating example data")
    if create_examples:
        with app.open_resource("db/examples.sql") as f:
            cursor.execute(f.read())
