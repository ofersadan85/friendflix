from views.auth import auth_bp
from views.movies import movies_bp
from views.user_actions import actions_bp

all_blueprints = [auth_bp, actions_bp, movies_bp]
