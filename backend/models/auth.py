from datetime import datetime

import bcrypt
from psycopg import AsyncConnection
from psycopg.rows import class_row, namedtuple_row
from psycopg.sql import SQL
from pydantic import BaseModel, Field


def check_password_hash(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


class LoginUser(BaseModel):
    username_or_email: str = Field(alias="username")
    password: str


class User(BaseModel):
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
    def sql_fields(cls) -> str:
        """Returns the class fields as a comma-space separated string as a helper for SQL"""
        return ", ".join(cls.model_fields.keys())

    @classmethod
    def get_by_id(cls, id: int, cursor: RealDictCursor) -> "User | None":
        query = f"SELECT {cls.sql_fields()} FROM users WHERE id = %s"
        cursor.execute(query, [id])
        row = cursor.fetchone()
        if row is None:
            return None
        return cls(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            created=row["created"],
            last_login=row["last_login"],
            role=row["role"],
        )

    @classmethod
    async def get_by_login(cls, username_or_email: str, password: str, conn: AsyncConnection) -> "User | None":
        query = SQL(f"SELECT {cls.sql_fields()}, password FROM users WHERE username = %s OR email = %s")  # type: ignore
        async with conn.cursor(row_factory=namedtuple_row) as cursor:
            await cursor.execute(query, [username_or_email, username_or_email])
            row = await cursor.fetchone()
            if row is None:
                return None
            if row.password and (password == row.password or check_password_hash(row.password, password)):
                now = datetime.now()
                query = SQL("UPDATE users SET last_login = %s WHERE id = %s")
                await cursor.execute(query, [now, row["id"]])
                return cls(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                    created=row["created"],
                    last_login=now,
                    role=row["role"],
                )


class NewUser(BaseModel):
    username: str
    password: str
    email: str
    role: str = "user"

    async def register(self, conn: AsyncConnection) -> User:
        hashed_password = hash_password(self.password)
        query = SQL(f"""INSERT INTO users
                (username, password, email, role)
                VALUES (%s, %s, %s, %s)
                RETURNING {User.sql_fields()}""")  # type: ignore
        async with conn.cursor(row_factory=class_row(User)) as cursor:
            await cursor.execute(query, [self.username, hashed_password, self.email, self.role])
            user = await cursor.fetchone()
            assert user is not None
            return user
