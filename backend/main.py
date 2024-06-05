from db.db import DB_PATH, close_db, get_db
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from views import all_blueprints
from werkzeug.security import gen_salt

app = Flask(__name__)
app.config.from_prefixed_env()
app.teardown_appcontext(close_db)
for bp in all_blueprints:
    app.register_blueprint(bp)

FRONTEND_URL = app.config.get("FRONTEND_URL", "*")
cors = CORS(app, origins=FRONTEND_URL, methods=["GET", "POST", "DELETE"])
jwt = JWTManager(app)

if app.debug:
    app.logger.debug("Starting app with config:")
    for key, value in app.config.items():
        app.logger.debug(f"{key}={value}")

if not DB_PATH.is_file():
    app.logger.info("Database not found, creating new one")
    with app.app_context():
        db = get_db()
        with app.open_resource(DB_PATH.with_name("schema.sql")) as f:  # type: ignore
            db.executescript(f.read().decode("utf8"))
        initial_admin_username = app.config.get("INITIAL_ADMIN_USERNAME", "admin")
        initial_admin_email = app.config.get("INITIAL_ADMIN_EMAIL", "admin@example.com")
        random_password = gen_salt(16)
        initial_admin_password = app.config.get("INITIAL_ADMIN_PASSWORD", random_password)
        db.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
            [initial_admin_username, initial_admin_email, initial_admin_password, "admin"],
        )
        app.logger.info(
            f"""
                *********************************************************
                Created initial admin user `{initial_admin_username}` with password: {initial_admin_password}
                Don't forget to change the password on your first login!
                *********************************************************
                """
        )

        create_examples = app.config.get("CREATE_EXAMPLES", False)
        app.logger.info("Creating example data")
        if create_examples:
            with app.open_resource(DB_PATH.with_name("examples.sql")) as f:  # type: ignore
                db.executescript(f.read().decode("utf8"))
