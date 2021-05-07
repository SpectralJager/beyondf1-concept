import flask, flask_migrate
from beyondf1.extensions import db
from beyondf1.views import bp

def create_app(test_config=None):
    app = flask.Flask(__name__)

    #### config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #### extensions and blueprints
    app.register_blueprint(bp)
    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = flask_migrate.Migrate(app,db)