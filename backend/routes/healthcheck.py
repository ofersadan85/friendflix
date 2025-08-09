from datetime import datetime
from typing import Annotated

import psycopg
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel

from common import get_db

router = APIRouter(tags=["Health Check"])


class HealthCheckResponse(BaseModel):
    health: str
    app_datetime: str
    db_datetime: datetime | str | None


@router.get("/healthcheck")
async def healthcheck(db: Annotated[AsyncConnectionPool, Depends(get_db)]) -> JSONResponse:
    app_datetime = datetime.now().isoformat()
    try:
        async with db.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT NOW()")
                db_datetime = await cursor.fetchone()
        assert db_datetime is not None
        content = HealthCheckResponse(health="OK", app_datetime=app_datetime, db_datetime=db_datetime[0])
        status_code = 200
    except (psycopg.Error, AssertionError, KeyError):
        content = HealthCheckResponse(health="Database Error", app_datetime=app_datetime, db_datetime=None)
        status_code = 500
    return JSONResponse(content=content.model_dump(mode="json"), status_code=status_code)
