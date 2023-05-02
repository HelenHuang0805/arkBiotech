from flask import Flask
from .dashboard import dashboard_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    app.register_blueprint(dashboard_blueprint)
    return app
