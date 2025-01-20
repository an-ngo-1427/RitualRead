
from flask import Blueprint,request
from forms.user_forms import SignupForm
from models import User,db
from flask_login import login_user,logout_user
auth_routes = Blueprint('auth',__name__)

# Signing up a user
@auth_routes.route('/signup',method=['POST'])
def signup():
    form = SignupForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        newUser = User(
            first_name = form.data['first_name'],
            last_name = form.data['last_name'],
            email = form.data['email'],
            username = form.data['username'],
            password = form.data['password'],
        )

        db.session.add(newUser)
        db.session.commit()
        login_user(newUser)
        return
