import logging
from contextlib import asynccontextmanager
from datetime import datetime

import psycopg2
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor
from pydantic import HttpUrl, PostgresDsn, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from db import get_db, init_db
from routes import all_routers

logger = logging.getLogger("uvicorn")


class AppSettings(BaseSettings):
    debug: bool = False
    db_address: PostgresDsn
    frontend_url: HttpUrl | None = None
    model_config = SettingsConfigDict(
        env_prefix="friendflix_",
        env_file=".env",
        # cli_parse_args=True, # This is buggy when using fastapi cli
    )


try:
    app_settings = AppSettings()
except ValidationError:
    logger.fatal("Some mandatory environment variables are missing or wrong, see example.env")
    exit(69)


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    try:
        # Startup logic
        app.state.settings = app_settings
        app.debug = app.state.settings.debug
        mode = "DEBUG / DEVELOPMENT" if app.debug else "PRODUCTION"
        logger.info(f"Starting app in {mode} mode")
        logger.info(f"CORS: FRONTEND_URL is set to {app.state.settings.frontend_url}")
        init_db()
        yield
    finally:
        # Shutdown logic
        logger.debug(app.middleware_stack)
        logger.info("Shutting down gracefully...")
        if hasattr(app.state, "db"):
            app.state.db.close()
            logger.info("Closed databse connection")


app = FastAPI(lifespan=lifespan_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(app_settings.frontend_url) or "*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
for router in all_routers:
    app.include_router(router)


@app.get("/healthcheck")
async def root(db: RealDictCursor = Depends(get_db)) -> JSONResponse:
    app_datetime = datetime.now().isoformat()
    try:
        db.execute("SELECT NOW() AS db_datetime")
        db_datetime = db.fetchone()
        assert db_datetime is not None
        db_datetime = db_datetime["db_datetime"]
        content = {"health": "OK", "app_datetime": app_datetime, "db_datetime": db_datetime.isoformat()}
        status_code = 200
    except (psycopg2.Error, AssertionError, KeyError):
        content = {"health": "Database Error", "app_datetime": app_datetime, "db_datetime": None}
        status_code = 500
    return JSONResponse(content=content, status_code=status_code)
