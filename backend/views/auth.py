from sqlite3 import IntegrityError

from db.db import get_db
from flask import Blueprint, current_app, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from models.auth import User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    cursor = get_db().cursor()
    user = User.get_by_login(username, password, cursor)
    if user is None:
        current_app.logger.info(f"Login attempt for {username} failed")
        return "Invalid username or password", 401
    current_app.logger.info(f"Login successful for {user}")
    return {"token": create_access_token(identity=user.id, additional_claims=user.asdict())}


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    secure_password = generate_password_hash(password)
    cursor = get_db().cursor()
    columns = User.fields(as_columns=True)
    try:
        cursor.execute(
            f"INSERT INTO users (username, email, password) VALUES (?, ?, ?) RETURNING {columns}",
            [username, email, secure_password],
        )
    except IntegrityError:
        return "Username or email already exists", 409
    new_user = User.from_sql_row(cursor.fetchone())
    if new_user:
        current_app.logger.info(f"New user registered: {new_user}")
        return {"token": create_access_token(identity=new_user.id, additional_claims=new_user.asdict())}
    else:
        return "Registration failed", 500


@auth_bp.route("/logout")
@jwt_required()
def logout():
    user = get_jwt()
    cursor = get_db().cursor()
    cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", [user["id"]])
    return ""


@auth_bp.route("/register/check")
def register_check():
    username = request.args.get("username")
    cursor = get_db().cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", [username])
    response_code = 200 if cursor.fetchone() is None else 409
    return "", response_code


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    return "Forgot password", 501
