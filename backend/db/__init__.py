import logging
import random
import string
from pathlib import Path

import psycopg
from fastapi import Request
from psycopg_pool import AsyncConnectionPool

from models.auth import NewUser
from settings import app_settings

logger = logging.getLogger("uvicorn")


def load_query(name: str) -> str:
    if not name.endswith(".sql"):
        name = name + ".sql"
    return (Path("db") / name).read_text()


async def pool_connect():
    pool = AsyncConnectionPool(conninfo=str(app_settings.db_address), open=False)
    await pool.open()
    return pool


async def get_db(request: Request) -> AsyncConnectionPool:
    if hasattr(request.app.state, "db_pool"):
        pool = request.app.state.db_pool
    else:
        pool = await pool_connect()
        request.app.state.db_pool = pool
    return pool  # type: ignore


async def init_db():
    pool = await pool_connect()
    async with pool.connection() as conn:
        try:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT id FROM users LIMIT 1")
                _ = await cursor.fetchone()
        except psycopg.Error:
            logger.info("Database not found, creating new one")
        else:
            logger.info("Database already exists, skipping creation")
            return

        password = app_settings.initial_admin_password or "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(16)
        )
        async with conn.cursor() as cursor:
            schema = SQL(load)
            await cursor.execute(load_query("schema"))
            new_user = NewUser(
                username=app_settings.initial_admin_username,
                password=password,
                email=app_settings.initial_admin_email,
                role="admin",
            )
            await new_user.register(conn)
            logger.info(f"""
                    *********************************************************
                    Created initial admin user `{app_settings.initial_admin_username}` with password: {password}
                    Don't forget to change the password on your first login!
                    *********************************************************
                    """)
            if app_settings.create_examples:
                logger.info("Creating example data")
                examples = Path("db/examples.sql").read_text()
                await cursor.execute(examples)
