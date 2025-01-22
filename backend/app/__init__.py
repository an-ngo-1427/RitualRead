import os
from .config import Config
from flask import Flask,request,redirect
from flask_cors import CORS
from flask_wtf.csrf import generate_csrf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db
import flask_login
from .api.auth_routes import auth_routes
app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
# application securities
CORS(app)
# registering app with blueprints
app.register_blueprint(auth_routes,url_prefix='/api/auth')
# in production, forcing requests from http to https protocol by redirecting requests
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
        return app.send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
