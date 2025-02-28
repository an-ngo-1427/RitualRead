
from flask import Blueprint,request,redirect,render_template,url_for
from forms.user_forms import SignupForm,LoginForm
from models import User,db
from flask_login import current_user,login_user,logout_user,login_required
auth_routes = Blueprint('auth',__name__)

#loading a user

@auth_routes.route('/')
def get_user():
    if current_user.is_authenticated:
        # return current_user.to_dict()
        print('this is current user',current_user)
        return render_template('testing.html',current_user=current_user)
    return {'error':{'message':'Unauthorized'}}, 401

# Signing up a user
@auth_routes.route('/signup',methods=['GET','POST'])
def signup():
    form = SignupForm()
    if (request.method == 'GET'):
        return render_template('signUp.html',form=form),200

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
        return redirect(url_for('homePage')),201
    # return {'errors':{k:v[0] for k,v in form.errors.items()}}, 400
    return render_template('signUp.html',form=form),400

# logging out user
@auth_routes.route('/logout',methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homePage')),301

#logging in a user
@auth_routes.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.data['email']).first()
        login_user(user)
        return redirect(url_for('homePage')),301

    return render_template('login.html',form=form)

@auth_routes.route('/delete',methods = ['DELETE'])
def deleteAcc(user_id):
    user = User.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return 'Account deleted successfully'
    else:
        return 'User not found',401
