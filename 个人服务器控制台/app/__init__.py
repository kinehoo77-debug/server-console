from flask import Flask

from app.config import Config
from app.routes.auth import auth_bp
from app.routes.main import main_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["MAX_CONTENT_LENGTH"] = app.config["MAX_UPLOAD_MB"] * 1024 * 1024

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    return app
