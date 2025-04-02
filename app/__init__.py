
import os
import selectors
from .websocket import sio
if (os.environ.get('FLASK-ENV') != 'production'):
    selectors.DefaultSelector = selectors.SelectSelector


from .config import Config
from .models import db,User
from .api.auth_routes import auth_routes
from .api.feed_routes import feed_routes
from .api.room_routes import room_routes,rooms
from .api.lobby_routes import lobby_routes
import flask_login
from flask import Flask,request,redirect,render_template,session,send_from_directory
from flask_cors import CORS
from flask_wtf.csrf import generate_csrf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO,send,join_room,leave_room
from flask_login import current_user

app = Flask(__name__,static_folder='../react-vite/dist',static_url_path='/')

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)

# initiating socketio
sio.init_app(app)

# Flask logink
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# application securities
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


CORS(app)

# @app.route('/api')
# def index():
#     return render_template('index.html')
# registering app with blueprints
@app.route('/api')
def homePage():
    return render_template('index.html',current_user=current_user)

app.register_blueprint(auth_routes,url_prefix='/api/auth')
app.register_blueprint(feed_routes,url_prefix = '/api/feed')
app.register_blueprint(room_routes,url_prefix='/api/rooms')
app.register_blueprint(lobby_routes,url_prefix='/api/lobby')
# in production, forcing requests from http to https protocol by redirecting requests
@app.before_request
def before_request():
    print('current user----',current_user)
    print('user is authenticated----',current_user.is_authenticated)

@app.before_request
def redirect_request():
    if os.environ.get('FLASK_ENV') == 'production':
        print('in production',request)
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://','https://',1)
            code = 301
            return redirect(url,code = code)

# injecting csurf token to cookies after every requests
@app.after_request
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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    """
    This route will direct to the public directory in our
    react builds in the production environment for favicon
    or index.html requests
    """
    if path == 'favicon.ico':
        return send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    sio.run(app)
