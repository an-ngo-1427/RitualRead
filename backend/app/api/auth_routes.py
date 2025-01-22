
from flask import Blueprint,request,redirect
from app.forms.user_forms import SignupForm,LoginForm
from app.models import User,db
from flask_login import current_user,login_user,logout_user,login_required,LoginManager
auth_routes = Blueprint('auth',__name__)
login_manager = LoginManager()
#loading a user
@auth_routes.route('/')
def get_user():
    print('---------getting user',current_user.is_authenticated)
    return

# Signing up a user
@auth_routes.route('/signup',methods=['POST'])
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
        return newUser.to_dict(), 301

# logging out user
@auth_routes.route('/logout',methods = ['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

#logging in a user
@auth_routes.route('/login',methods = ['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.data['email'])
        login_user(user)
        return user.to_dict(), 201

    return form.errors, 401

@auth_routes.route('/delete',methods = ['DELETE'])
@login_manager.user_loader
def deleteAcc(user_id):
    user = User.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return 'Account deleted successfully'
    else:
        return 'User not found',401
