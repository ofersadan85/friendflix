import logging
import random
import string

import psycopg

from common import app_settings, load_query, pool_connect
from routes.auth import NewUser

logger = logging.getLogger("uvicorn")


async def init_db() -> None:
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

        password = app_settings.initial_admin.password or "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(16)
        )
        async with conn.cursor() as cursor:
            await cursor.execute(query=load_query("schema"))
            new_user = NewUser(
                username=app_settings.initial_admin.username,
                password=password,
                email=app_settings.initial_admin.email,
                role="admin",
            )
            await new_user.register(conn)
            logger.info(f"""
                    *********************************************************
                    Created initial admin user `{app_settings.initial_admin.username}` with password: {password}
                    Don't forget to change the password on your first login!
                    *********************************************************
                    """)
            if app_settings.create_examples:
                logger.info("Creating example data")
                example_users = [
                    NewUser(username="alice123", password="password123", email="alice@example.com"),
                    NewUser(username="bob456", password="password456", email="bob@example.com"),
                    NewUser(username="charlie789", password="password789", email="charlie@example.com", role="admin"),
                    NewUser(username="diana101", password="password101", email="diana@example.com"),
                    NewUser(username="eve202", password="password202", email="eve@example.com"),
                ]
                for user in example_users:
                    await user.register(conn)
