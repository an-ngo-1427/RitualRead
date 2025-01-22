
from flask import Blueprint,request,redirect
from app.forms.user_forms import SignupForm,LoginForm
from app.models import User,db
from flask_login import current_user,login_user,logout_user,login_required
auth_routes = Blueprint('auth',__name__)

#loading a user

@auth_routes.route('/')
def get_user():
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'error':{'message':'Unauthorized'}}, 401

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
            password = form.data['password']
        )

        db.session.add(newUser)
        db.session.commit()
        login_user(newUser)
        return newUser.to_dict(), 301
    return {'errors':{k:v[0] for k,v in form.errors.items()}}, 400

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
def deleteAcc(user_id):
    user = User.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return 'Account deleted successfully'
    else:
        return 'User not found',401
