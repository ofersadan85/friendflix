import logging

from pydantic import EmailStr, HttpUrl, PostgresDsn, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("uvicorn")


class AppSettings(BaseSettings):
    debug: bool = False
    db_address: PostgresDsn
    frontend_url: HttpUrl | None = None
    initial_admin_username: str = "admin"
    initial_admin_password: str | None = None
    initial_admin_email: EmailStr = "admin@example.com"
    create_examples: bool = False

    model_config = SettingsConfigDict(
        env_prefix="friendflix_",
        env_file=".env",
        # cli_parse_args=True, # This is buggy when using fastapi cli
    )


app_settings = None
try:
    app_settings = AppSettings()
except ValidationError:
    logger.fatal("Some mandatory environment variables are missing or wrong, see example.env")
    exit(69)
assert app_settings is not None
