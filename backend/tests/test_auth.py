import pytest
from db.db import get_db
from flask_jwt_extended import decode_token
from main import app
from werkzeug.security import generate_password_hash

user1 = ["test_user1", "test@example.com", "test_password"]
user2 = ["test_user2", "test2@another.com", generate_password_hash("test_password")]


@pytest.fixture
def db():
    with app.app_context():
        db = get_db()
        db.execute("DELETE FROM users WHERE username LIKE 'test_%'")
        yield db
        db.execute("DELETE FROM users WHERE username LIKE 'test_%'")


def test_login(db):
    client = app.test_client()
    for user in [user1, user2]:
        db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", user)

    # Test plain password
    response = client.post("/login", json={"username": user1[0], "password": user1[2]})
    assert response.status_code == 200, "Valid login failed (plain password)"
    assert isinstance(response.json, dict)
    assert "token" in response.json.keys(), "Token not in response for valid login (plain password)"

    # Test hashed password
    response = client.post("/login", json={"username": user2[0], "password": user2[2]})
    assert response.status_code == 200, "Valid login failed (hashed password)"
    assert isinstance(response.json, dict)
    assert "token" in response.json.keys(), "Token not in response for valid login (hashed password)"

    # Test email login
    response = client.post("/login", json={"username": user1[1], "password": user1[2]})
    assert response.status_code == 200, "Valid login failed (email)"
    assert isinstance(response.json, dict)
    assert "token" in response.json.keys(), "Token not in response for valid login (email)"

    # Test invalid password
    response = client.post("/login", json={"username": "test_user1", "password": "wrong_password"})
    assert response.status_code == 401, "Invalid password not detected"
    assert "invalid" in response.text.lower(), "Invalid password not detected"

    # Test invalid username
    response = client.post("/login", json={"username": "wrong_user", "password": "test_password"})
    assert response.status_code == 401, "Invalid username not detected"
    assert "invalid" in response.text.lower(), "Invalid username not detected"


def test_register(db):
    client = app.test_client()

    # Test registration, new user
    response = client.post("/register", json={"username": user1[0], "email": user1[1], "password": user1[2]})
    assert response.status_code == 200, "Registration failed"
    assert isinstance(response.json, dict)
    assert "token" in response.json.keys(), "Token not in response for valid registration"
    user = decode_token(response.json["token"])
    assert user["username"] == user1[0], "Username mismatch"
    assert user["email"] == user1[1], "Email mismatch"
    assert user["role"] == "user", "Role mismatch"
    assert "created" in user.keys(), "Created timestamp missing"
    assert "last_login" in user.keys(), "Last login timestamp missing"
    assert "id" in user.keys(), "ID missing"
    assert "password" not in user.keys(), "Password returned in response"

    # Test registration, existing user
    response = client.post("/register", json={"username": user1[0], "email": user1[1], "password": user1[2]})
    assert response.status_code == 409, "Duplicate username not detected"
    assert "exists" in response.text.lower(), "Duplicate username not detected"

    # Test registration, existing email
    response = client.post("/register", json={"username": "test_new", "email": user1[1], "password": user1[2]})
    assert response.status_code == 409, "Duplicate email not detected"
    assert "exists" in response.text.lower(), "Duplicate email not detected"


def test_logout():
    client = app.test_client()
    response = client.post("/register", json={"username": user1[0], "email": user1[1], "password": user1[2]})
    assert isinstance(response.json, dict)
    register_token = response.json["token"]
    response = client.post("/login", json={"username": user1[0], "password": user1[2]})
    assert isinstance(response.json, dict)
    login_token = response.json["token"]
    assert register_token != login_token, "Tokens should not match"
    response = client.get("/logout", headers={"Authorization": f"Bearer {login_token}"})
    assert response.status_code == 200, "Logout failed"
    assert response.text == "", "Logout failed"
    response = client.get("/logout")
    assert response.status_code == 401, "Logout succeeded without token"
