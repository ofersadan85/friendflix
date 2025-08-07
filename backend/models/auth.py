from datetime import datetime

from psycopg2.extras import RealDictCursor
from pydantic import BaseModel


def check_password_hash(hashed_password: str, password: str) -> bool:
    return True  # TODO: implement


def hash_password(password: str) -> str:
    return password  # TODO: implement


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

    def __str__(self) -> str:
        return f"<{self.role.capitalize()} {self.username} ({self.id})>"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def sql_fields(cls) -> str:
        """Returns the class fields as a comma-space separated string as a helper for SQL"""
        return ", ".join(cls.model_fields.keys())

    @classmethod
    def get_by_id(cls, id: int, cursor: RealDictCursor) -> "User | None":
        query = f"SELECT {cls.sql_fields()} FROM users WHERE id = %s"
        cursor.execute(query, [id])
        row = cursor.fetchone()
        return cls.from_sql_row(row)

    @classmethod
    def get_by_login(cls, username_or_email: str, password: str, cursor: RealDictCursor) -> "User | None":
        query = f"SELECT {cls.sql_fields()}, password FROM users WHERE username = %s OR email = %s"
        cursor.execute(query, [username_or_email, username_or_email])
        row = cursor.fetchone()
        db_password = row["password"] if row else None
        if db_password and (password == db_password or check_password_hash(db_password, password)):
            return cls.from_sql_row(row)
        else:
            return None


class NewUser(BaseModel):
    username: str
    password: str
    email: str
    role: str = "user"

    def register(self, cursor: RealDictCursor) -> User:
        hashed_password = hash_password(self.password)
        query = f"""INSERT INTO users
                (username, password, email, role)
                VALUES (%s, %s, %s, %s)
                RETURNING {User.sql_fields()}"""
        cursor.execute(query, [self.username, hashed_password, self.email, self.role])
        row = cursor.fetchone()
        return User(**row)
