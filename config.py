class Config(object):
    DEBUG = False
    TESTING = False
    API_VERSION = 0.1
    API_TITLE = 'user-service'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    URL_PREFIX = '/users/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    CORS_ORIGINS = "*"
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES = 1440
class ProductionConfig(Config):
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_USER = 'user'
    DB_PASSWORD = 'password'
    DB_NAME = 'users'
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
class DevelopmentConfig(Config):
    DEBUG = True
class TestConfig(Config):
    TESTING = True
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'