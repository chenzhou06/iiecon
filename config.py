import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "chenzhou999"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    #MAIL_SERVER = ""
    #MAIL_PORT = 
    # MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    IIECON_MAIL_SUBJECT_PREFIX = "[IIECON]"
    IIECON_MAIL_SENDER = "IIECON <admin@iiecon.com>"
    IIECON_ADMIN = os.environ.get("XTU_ADMIN") or "czwork@outlook.com"
    IIECON_POSTS_PER_PAGE = 20
    IIECON_FOLLOWERS_PER_PAGE = 50
    IIECON_COMMENTS_PER_PAGE = 30
    IIECON_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = "127.0.0.1:5000"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
            "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = "iiecon.cz"
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
             "sqlite://" + os.path.join(basedir, "data-test.sqlite")
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SERVER_NAME = "iiecon.cz"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
             "sqlite://" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
