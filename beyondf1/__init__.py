import flask, flask_migrate
from beyondf1.models import db
from beyondf1.site_views import site
from beyondf1.admin_views import admin

def create_app(test_config=None):
    app = flask.Flask(__name__)

    #### config
    app.secret_key = b'HollaAmigos'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #### extensions and blueprints
    app.register_blueprint(site)
    app.register_blueprint(admin)
    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = flask_migrate.Migrate(app,db)