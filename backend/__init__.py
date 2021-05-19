import flask 
from .api import api_v1, secret_key
from flask_cors import CORS

def create_app(test_config=None):
    app = flask.Flask(__name__)

    #### config
    app.secret_key = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #### extensions and blueprints
    app.register_blueprint(api_v1)
    register_extensions(app)

    return app


def register_extensions(app):
    CORS(app)