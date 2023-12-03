from flask import Flask, current_app
from flask_cors import CORS
import config as cng
import os
from whisper import _download, _MODELS


def init_app() -> Flask:
    app = Flask(__name__)
    download_root = os.path.join(os.path.expanduser("~"), ".cache", "whisper")
    _download(_MODELS["base"], download_root, False)
    CORS(app)
    with app.app_context():
        register_blueprints(app)
        app.config.from_object(cng.Config)
        print(app.config)

    return app


def register_blueprints(app: Flask) -> None:
    """Registering blueprint"""
    from app.routes import get_translation_api
    from app.routes import home
    from app.routes import get_progression_api
    from app.routes import get_subtitles_api

    app.register_blueprint(home)
    app.register_blueprint(get_translation_api)
    app.register_blueprint(get_progression_api)
    app.register_blueprint(get_subtitles_api)
