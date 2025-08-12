import random
import string

import pytest
from fastapi.testclient import TestClient
from psycopg_pool import AsyncConnectionPool

from common import pool_connect
from main import app
from routes.auth import NewUser, User


def random_string(length: int) -> str:
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.yield_fixture(scope="session")
async def db():
    db = await pool_connect()
    yield db
    await db.close()


@pytest.mark.asyncio
async def test_register_login(client: TestClient, db: AsyncConnectionPool):
    username = "test_" + random_string(8)
    password = random_string(12)
    email = f"{username}@example.com"
    new_user = NewUser(username=username, password=password, email=email)

    # Login before registration
    response = client.post("/auth/login", json=new_user.model_dump(exclude={"email"}))
    assert response.status_code == 404
    assert response.cookies.get("auth_token") is None, "Auth token cookie should not be set"

    # Register the user
    response = client.post("/auth/register", json=new_user.model_dump())
    assert response.status_code == 200
    user = response.json()
    assert "id" in user
    assert user["id"] > 0
    assert "password" not in user, "Password should not be returned"
    user = User(**user)
    assert user.username == username
    assert user.email == email
    assert user.last_login is None
    assert user.role == "user"
    assert user.enabled
    assert not user.verified

    # Login after registration
    response = client.post("/auth/login", json=new_user.model_dump(exclude={"email"}))
    assert response.status_code == 200
    json_response = response.json()
    token = json_response.get("auth_token")
    assert token is not None, "Auth token should be returned"
    assert response.cookies.get("auth_token") is not None, "Auth token cookie should be set"
    returned_user = User(**json_response.get("user"))
    assert returned_user.model_dump(exclude={"last_login"}) == user.model_dump(exclude={"last_login"})

    # Login with wrong password
    response = client.post("/auth/login", json={"username": username, "password": "wrong"})
    assert response.status_code == 401
    assert response.cookies.get("auth_token") is None, "Auth token cookie should not be set"

    # Login with email
    response = client.post("/auth/login", json={"username": email, "password": password})
    assert response.status_code == 200
    json_response = response.json()
    token = json_response.get("auth_token")
    assert token is not None, "Auth token should be returned"
    assert response.cookies.get("auth_token") is not None, "Auth token cookie should be set"
    returned_user = User(**json_response.get("user"))
    assert returned_user.model_dump(exclude={"last_login"}) == user.model_dump(exclude={"last_login"})

    # Register with the same username
    response = client.post("/auth/register", json=new_user.model_dump())
    assert response.status_code == 409
    assert response.json().get("detail") == "Username or Email already exists"

    # Cleanup
    async with db.connection() as conn:
        await conn.execute("DELETE FROM users WHERE id = %s", (user.id,))
