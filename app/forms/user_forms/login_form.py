from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired,ValidationError
from app.models import User
def verifyEmail(form,field):
    user = User.query.filter(User.email == field.data)
    if not user:
        return ValidationError('incorrect credentials')

def verifyPassword(form,field):
    user = User.query.filter(User.email == field.data)
    if not user.check_password(field.data):
        return ValidationError('incorrect credentials')

class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired('email required'),verifyEmail])
    password = StringField('password',validators=[DataRequired('password required'),verifyEmail,verifyPassword])
