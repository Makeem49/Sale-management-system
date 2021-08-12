import os
from typing import Tuple 

basedir = os.path.abspath(os.path.dirname(__file__))
username = "makeem49"
password = "Olayinka1?"
developementdbname = "management"
testingdbname = 'testingmanagement'
productiondbname = 'productionmanagement'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_ADMIN = os.environ.get('FLASK_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class Development(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@localhost/{developementdbname}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@localhost/{testingdbname}"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@localhost/{productiondbname}"

config = {
    'developemnt' : Development,
    'testing' : TestingConfig,
    'production' : ProductionConfig,

    'default' : Development
}