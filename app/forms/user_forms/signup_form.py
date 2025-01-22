from flask_wtf import FlaskForm
from wtforms import StringField,EmailField
from wtforms.validators import DataRequired,ValidationError
from app.models import User
def emailExists(form,field):
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        return ValidationError('email is already in use')

def usernameExists(form,field):
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        return ValidationError('username is already in use')



class SignupForm(FlaskForm):
    username = StringField('username',validators=[DataRequired('username required'),usernameExists])
    email = EmailField('email',validators=[DataRequired(),emailExists])
    password = StringField('password',validators=[DataRequired()])
    first_name = StringField('first_name',validators=[DataRequired()])
    last_name = StringField('last_name',validators=[DataRequired()])
