import os
import pprint
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    pprint.pprint(dict(os.environ),width=1)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL').replace('prosgres://','postgresql://')
    SQLALCHEMY_ECHO = True
