from db.db import get_db
from flask import Blueprint, request
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, username, role FROM users WHERE username = ? AND password = ?", (data["username"], data["password"])
    )
    user = cursor.fetchone()
    if user is None:
        return "Invalid username or password", 401
    user_dict = {"id": user["id"], "username": user["username"], "role": user["role"]}
    data["token"] = create_access_token(identity=user["id"], additional_claims=user_dict)
    return data


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return data


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return "Logout"


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    return "Forgot password"


@auth_bp.route("/register/check")
def register_check():
    username = request.args.get("username")
    if username == "admin":
        # TODO: Check if username exists in the database
        return "Username already exists", 400
    return "", 200
