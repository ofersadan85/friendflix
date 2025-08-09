import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

import psycopg
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from psycopg_pool import AsyncConnectionPool

from common import app_settings, get_db
from db import init_db
from routes import all_routers

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    try:
        # Startup logic
        app.state.settings = app_settings
        app.debug = app.state.settings.debug
        mode = "DEBUG / DEVELOPMENT" if app.debug else "PRODUCTION"
        logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
        logger.info(f"Starting app in {mode} mode")
        logger.info(f"CORS: FRONTEND_URL is set to {app.state.settings.frontend_url}")
        await init_db()
        yield
    finally:
        # Shutdown logic
        logger.debug(app.middleware_stack)
        logger.info("Shutting down gracefully...")
        if hasattr(app.state, "db_pool"):
            db_pool: AsyncConnectionPool = app.state.db_pool
            await db_pool.close()
            logger.info("Closed database connection")


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
async def healthcheck(db: Annotated[AsyncConnectionPool, Depends(get_db)]) -> JSONResponse:
    app_datetime = datetime.now().isoformat()
    try:
        async with db.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT NOW()")
                db_datetime = await cursor.fetchone()
        assert db_datetime is not None
        db_datetime = db_datetime[0].isoformat() if isinstance(db_datetime[0], datetime) else db_datetime[0]
        content = {"health": "OK", "app_datetime": app_datetime, "db_datetime": db_datetime}
        status_code = 200
    except (psycopg.Error, AssertionError, KeyError):
        content = {"health": "Database Error", "app_datetime": app_datetime, "db_datetime": None}
        status_code = 500
    return JSONResponse(content=content, status_code=status_code)
