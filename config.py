from datetime import timedelta

class Config(object):
    DEBUG = False
    TESTING = False
    API_VERSION = 0.1
    API_TITLE = 'user-service'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    URL_PREFIX = '/users/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    CORS_ORIGINS = ["*"]
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1024)
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@127.0.0.1/users'
class DevelopmentConfig(Config):
    DEBUG = True
class TestConfig(Config):
    TESTING = True
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'