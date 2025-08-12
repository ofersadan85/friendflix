import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import Request
from psycopg.sql import SQL, Composed, Identifier
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel, EmailStr, HttpUrl, PostgresDsn, ValidationError, AnyUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("uvicorn")


class InitialAdminUser(BaseModel):
    username: str = "admin"
    email: EmailStr = "admin@example.com"
    password: str | None = None


class JWTSettings(BaseModel):
    secret_key: str
    expiry_minutes: int = 60


class AppSettings(BaseSettings):
    debug: bool = False
    db_address: PostgresDsn
    frontend_url: HttpUrl | None = None
    initial_admin: InitialAdminUser = InitialAdminUser()
    create_examples: bool = False
    jwt: JWTSettings
    smtp: AnyUrl | None = None

    model_config = SettingsConfigDict(
        env_prefix="friendflix_",
        env_file=".env",
        env_nested_delimiter="_",
        env_nested_max_split=1,
        # cli_parse_args=True, # This is buggy when using fastapi cli
    )

    @field_validator("smtp")
    @classmethod
    def validate_smtp(cls, v: AnyUrl | None) -> AnyUrl | None:
        if v is None:
            return None
        if not all([v.username, v.password, v.host, v.port]) or v.scheme != "smtp":
            logger.warning("SMTP URL must include username, password, host, and port: smtp://user:pass@host:port")
            logger.warning("SMTP Settings will be ignored")
        return v


try:
    app_settings = AppSettings()  # type: ignore
except ValidationError as e:
    logger.fatal(f"Some mandatory environment variables are missing or wrong, see example.env {e}")
    exit(69)


class SQLModel(BaseModel):
    @classmethod
    def sql_fields(cls) -> Composed:
        return SQL(", ").join(Identifier(field) for field in cls.model_fields.keys())


@lru_cache
def load_query(name: str) -> SQL | Composed:
    if not name.endswith(".sql"):
        name = name + ".sql"
    return SQL((Path("db") / name).read_text())  # type: ignore[unused-ignore]


async def pool_connect() -> AsyncConnectionPool[Any]:
    pool = AsyncConnectionPool(
        conninfo=str(app_settings.db_address),  # cSpell: disable-line
        open=False,
        timeout=10,
    )
    await pool.open()
    return pool


async def get_db(request: Request) -> AsyncConnectionPool:
    if hasattr(request.app.state, "db_pool"):
        pool: AsyncConnectionPool = request.app.state.db_pool
    else:
        pool = await pool_connect()
        request.app.state.db_pool = pool
    return pool
