class Config(object):
    DEBUG = False
    TESTING = False
    API_VERSION = 0.1
    API_TITLE = 'user-service'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    CORS_ORIGINS = ["*"]
    JWT_SECRET_KEY = "super-secret"
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@127.0.0.1/users'
class DevelopmentConfig(Config):
    DEBUG = True
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'