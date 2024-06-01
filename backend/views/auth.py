from flask import Blueprint, request

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
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
