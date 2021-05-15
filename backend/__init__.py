import flask, flask_migrate
from .models import db
from .site_views import site
from .admin_views import admin
from .api import api_v1
from flask_cors import CORS

def create_app(test_config=None):
    app = flask.Flask(__name__)

    #### config
    app.secret_key = b'HollaAmigos'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #### extensions and blueprints
    app.register_blueprint(site)
    app.register_blueprint(admin)
    app.register_blueprint(api_v1)
    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = flask_migrate.Migrate(app,db)
    CORS(app)