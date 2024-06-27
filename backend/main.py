import psycopg2
from db import close_db, init_db
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from views import all_blueprints

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

with app.app_context():
    try:
        init_db(app)
    except psycopg2.errors.ConnectionFailure:
        app.logger.error("Failed to connect to the database, exiting")
        exit(1)
