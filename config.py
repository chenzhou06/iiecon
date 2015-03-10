import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "chenzhou999"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    # MAIL_SERVER = "smtp.qq.com"
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    # MAIL_USERNAME = "714264297"
    # MAIL_PASSWORD = "a650520"
    MAIL_SERVER = "hwsmtp.exmail.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "admin@iiecon.cz"
    MAIL_PASSWORD = "cz650520"
    IIECON_MAIL_SUBJECT_PREFIX = "[IIECON]"
    IIECON_MAIL_SENDER = "IIECON Admin <admin@iiecon.cz>"
    IIECON_ADMIN = os.environ.get("IIECON_ADMIN") or "iiecon@163.com"
    IIECON_POSTS_PER_PAGE = 20
    IIECON_FOLLOWERS_PER_PAGE = 50
    IIECON_COMMENTS_PER_PAGE = 30
    IIECON_SLOW_DB_QUERY_TIME = 0.5
    WTF_CSRF_ENABLED = True
    FLATPAGES_ROOT = os.path.join(basedir, "app", "blog", "pages")
    FLATPAGES_AUTO_RELOAD = True
    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_ENCODING = 'utf-8'
    FLATPAGES_MIMA = "cz650520"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = "127.0.0.1:5000"
    # WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = "iiecon.cz"
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "data-test.sqlite")
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SERVER_NAME = "iiecon.cz"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
