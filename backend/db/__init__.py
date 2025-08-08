import logging
import random
import string
from pathlib import Path

import psycopg
from psycopg.sql import SQL

from common import app_settings, load_query, pool_connect
from routes.auth import NewUser

logger = logging.getLogger("uvicorn")


async def init_db():
    pool = await pool_connect()
    async with pool.connection() as conn:
        try:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT id FROM users LIMIT 1")
                _ = await cursor.fetchone()
        except psycopg.Error:
            logger.info("Database not found, creating new one")
            await conn.rollback()
        else:
            logger.info("Database already exists, skipping creation")
            return

        password = app_settings.initial_admin_password or "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(16)
        )
        async with conn.cursor() as cursor:
            schema = SQL(load_query("schema"))  # type: ignore
            await cursor.execute(schema)
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
                examples = SQL(Path("db/examples.sql").read_text())  # type: ignore
                await cursor.execute(examples)
