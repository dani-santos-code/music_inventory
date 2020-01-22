import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '\xf6\xbc\xe3\xfeD\xb5\xf8=\xd1\x80?\x13Hl\x81\x11'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///instruments.db')
    ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
    AUTHORIZATION_URL = 'https://accounts.google.com/o/' \
                        'oauth2/v2/auth?access_type=offline&prompt=consent'
    AUTHORIZATION_SCOPE = 'openid email profile'
    AUTH_REDIRECT_URI = 'http://localhost:8000/gCallback'
    BASE_URI = 'http://localhost:8000'
    CLIENT_ID = '359568122134-niii8bh1f3l32b466s6qna4867lbq45p.' \
                'apps.googleusercontent.com'
    CLIENT_SECRET = 'T1iIGSdpiw9Tj-gPCnKQdyNy'

    # Session credentials
    AUTH_TOKEN_KEY = 'auth_token'
    USER_INFO_KEY = 'user_info'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
