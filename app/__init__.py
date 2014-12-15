from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .xtu import xtu as xtu_blueprint
    if config_name == "development":
        app.register_blueprint(xtu_blueprint, url_prefix="/xtu.308")
    else:
        app.register_blueprint(xtu_blueprint, subdomain="xtu.308")

    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint)

    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # from .api_1_0 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix="/api/v1.0")

    return app
