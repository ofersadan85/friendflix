from db.db import close_db
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
    print("Starting app with config:")
    for key, value in app.config.items():
        print(f"{key}={value}")
