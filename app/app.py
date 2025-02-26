
import os
import selectors

if (os.environ.get('FLASK-ENV') != 'production'):
    selectors.DefaultSelector = selectors.SelectSelector

import eventlet
eventlet.monkey_patch()


from config import Config
from models import db,User
from api.auth_routes import auth_routes
from api.feed_routes import feed_routes

import flask_login
from flask import Flask,request,redirect,render_template
from flask_cors import CORS
from flask_wtf.csrf import generate_csrf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO,send


flask_app = Flask(__name__,)

flask_app.config.from_object(Config)
db.init_app(flask_app)
migrate = Migrate(flask_app,db)

# Flask login
login_manager = flask_login.LoginManager()
login_manager.init_app(flask_app)

# Python socket
sio = SocketIO(flask_app,async_mode = 'eventlet',cors_allowed_origins="*")

@sio.on('connect')
def connect(message):
    print('connected -----',message)
    send('message received')

@sio.on('message')
def message(message):
    print('message from client',message)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# application securities
CORS(flask_app)

# @app.route('/api')
# def index():
#     return render_template('index.html')
# registering app with blueprints
flask_app.register_blueprint(auth_routes,url_prefix='/api/auth')
flask_app.register_blueprint(feed_routes,url_prefix = '/api/feed')
# in production, forcing requests from http to https protocol by redirecting requests
@flask_app.before_request
def redirect_request():
    if os.environ.get('FLASK_ENV') == 'production':
        print('in production',request)
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://','https://',1)
            code = 301
            return redirect(url,code = code)

# injecting csurf token to cookies after every requests
@flask_app.after_request
def inject_csurf_tokens(response):
    response.set_cookie(
        'csrf_token',
        value=generate_csrf(),
        max_age = 12400,
        secure = True if os.environ.get('FLASK_ENV') == 'production' else False,
        samesite = 'Lax' if os.environ.get('FLASK_ENV') == 'production' else None,
        httponly = True
    )
    return response

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def react_root(path):
#     """
#     This route will direct to the public directory in our
#     react builds in the production environment for favicon
#     or index.html requests
#     """
#     if path == 'favicon.ico':
#         return app.send_from_directory('public', 'favicon.ico')
#     return app.send_static_file('index.html')


@flask_app.errorhandler(404)
def not_found(e):
    return flask_app.send_static_file('index.html')
