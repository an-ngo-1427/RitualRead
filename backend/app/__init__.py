import os
from .config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)

@app.route('/')
def helloWorld():
    return 'hello  world'
