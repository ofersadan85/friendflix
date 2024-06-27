from dataclasses import asdict, dataclass, fields
from datetime import datetime

from psycopg2.extras import DictCursor
from werkzeug.security import check_password_hash


@dataclass
class User:
    id: int
    username: str
    email: str
    created: str | datetime
    last_login: str | datetime
    role: str = "user"

    def __post_init__(self):
        if isinstance(self.created, str):
            self.created = datetime.fromisoformat(self.created)
        if isinstance(self.last_login, str):
            self.last_login = datetime.fromisoformat(self.last_login)

    def asdict(self) -> dict:
        return asdict(self)

    @classmethod
    def fields(cls, as_columns: bool = False) -> list[str] | str:
        all_fields = [field.name for field in fields(cls)]
        return ", ".join(all_fields) if as_columns else all_fields

    @classmethod
    def from_sql_row(cls, row) -> "User | None":
        return cls(**{key: row[key] for key in cls.fields()}) if row else None

    def __str__(self) -> str:
        return f"<{self.role.capitalize()} {self.username} ({self.id})>"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def get_by_id(cls, id: int, cursor: DictCursor) -> "User | None":
        query = f"SELECT {cls.fields(True)} FROM users WHERE id = %s"
        cursor.execute(query, [id])
        row = cursor.fetchone()
        return cls.from_sql_row(row)

    @classmethod
    def get_by_login(cls, username_or_email: str, password: str, cursor: DictCursor) -> "User | None":
        query = f"SELECT {cls.fields(True)}, password FROM users WHERE username = %s OR email = %s"
        cursor.execute(query, [username_or_email, username_or_email])
        row = cursor.fetchone()
        db_password = row["password"] if row else None
        if db_password and (password == db_password or check_password_hash(db_password, password)):
            return cls.from_sql_row(row)
        else:
            return None
