from os import environ


class ProductionConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DLS_DATABASE_URI')
    DEMO_MODE = False
    SECRET_KEY = environ.get('DLS_SECRET_KEY')


class DemoConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///demo.db'
    DEMO_MODE = True
    SECRET_KEY = '1234'


class DevConfig:
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DLS_DATABASE_URI')
    DEMO_MODE = False
    SECRET_KEY = '1234'


class TestConfig:
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEMO_MODE = False
    SECRET_KEY = '1234'
