from os import environ


class DevConfig:
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DLS_DATABASE_URI')
    SECRET_KEY = environ.get('DLS_SECRET_KEY')


class TestConfig:
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = '1234'
