from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from psycopg import AsyncConnection
from psycopg import Error as SQLError
from psycopg.rows import class_row, dict_row
from psycopg.sql import SQL
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel, Field

from common import SQLModel, app_settings, get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


def check_password_hash(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


class User(SQLModel):
    id: int
    username: str
    email: str
    created: str | datetime
    last_login: str | datetime | None
    role: str = "user"

    def __post_init__(self):
        if isinstance(self.created, str):
            self.created = datetime.fromisoformat(self.created)
        if isinstance(self.last_login, str):
            self.last_login = datetime.fromisoformat(self.last_login)

    @classmethod
    async def get_by_id(cls, id: int, conn: AsyncConnection) -> "User | None":
        query = SQL("SELECT {fields} FROM users WHERE id = %s").format(fields=cls.sql_fields())
        async with conn.cursor(row_factory=class_row(User)) as cursor:
            await cursor.execute(query, [id])
            user = await cursor.fetchone()
            return user


class LoginUser(BaseModel):
    username_or_email: str = Field(alias="username")
    password: str

    async def get_user(self, conn: AsyncConnection) -> User:
        query = SQL("SELECT id, password FROM users WHERE username = %s OR email = %s")
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(query, [self.username_or_email, self.username_or_email])
            row = await cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=401, detail="User not found")
        if self.password != row["password"] and not check_password_hash(row["password"], self.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user_id = row["id"]
        now = datetime.now()
        async with conn.cursor(row_factory=class_row(User)) as cursor:
            query = SQL("UPDATE users SET last_login = %s WHERE id = %s RETURNING {fields}").format(
                fields=User.sql_fields()
            )
            await cursor.execute(query, [now, user_id])
            user = await cursor.fetchone()
            assert user is not None, "User should not be None after checking password"
            return user


class NewUser(BaseModel):
    username: str
    password: str
    email: str
    role: str = "user"

    async def register(self, conn: AsyncConnection) -> User:
        hashed_password = hash_password(self.password)
        query = SQL("""INSERT INTO users (username, password, email, role)
                VALUES (%s, %s, %s, %s)
                RETURNING {fields}""").format(fields=User.sql_fields())
        async with conn.cursor(row_factory=class_row(User)) as cursor:
            try:
                await cursor.execute(query, [self.username, hashed_password, self.email, self.role])
            except SQLError as e:
                # This will catch any sql error but will raise HTTPException
                # Internally this will still log the error appropriately
                # But the user will only see status 500 and the detail
                raise HTTPException(status_code=500, detail="User registration failed") from e
            user = await cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=500, detail="User registration failed")
            return user


@router.post("/register")
async def register(new_user: NewUser, db: AsyncConnectionPool = Depends(get_db)) -> User:
    async with db.connection() as conn:
        return await new_user.register(conn)


def create_auth_token(user: User) -> str:
    now = datetime.now(tz=timezone.utc)
    jwt_payload = {
        "sub": user.id,
        "exp": (now + timedelta(minutes=app_settings.jwt_expiry_minutes)).timestamp(),
        "iat": now.timestamp(),
        "user":user.model_dump(mode="json"),
    }
    return jwt.encode(jwt_payload, app_settings.jwt_secret_key, algorithm="HS256")


@router.post("/login")
async def login(login_user: LoginUser, db: AsyncConnectionPool = Depends(get_db)) -> JSONResponse:
    async with db.connection() as conn:
        user = await login_user.get_user(conn)
    auth_token = create_auth_token(user)
    response = JSONResponse(content={"user": user.model_dump(mode="json"), "auth_token": auth_token})
    response.set_cookie("auth_token", auth_token)
    return response


@router.get("/logout")
async def logout() -> JSONResponse:
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie("auth_token")
    return response
