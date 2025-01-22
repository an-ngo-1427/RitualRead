from flask_wtf import FlaskForm
from wtforms import StringField,EmailField
from wtforms.validators import DataRequired,ValidationError,Email
from app.models import User
def emailExists(form,field):
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError('email is already in use')

def usernameExists(form,field):
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('username is already in use')



class SignupForm(FlaskForm):
    username = StringField('username',validators=[DataRequired('username required'),usernameExists])
    email = EmailField('email',validators=[DataRequired('email is required'),Email(),emailExists])
    password = StringField('password',validators=[DataRequired('password is required')])
    first_name = StringField('first_name',validators=[DataRequired('first name is required')])
    last_name = StringField('last_name',validators=[DataRequired('last name is required')])
