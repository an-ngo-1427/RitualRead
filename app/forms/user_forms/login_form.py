from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired,ValidationError,StopValidation
from models import User

user = None
def verifyEmail(form,field):
    global user
    user = User.query.filter(User.email == field.data).first()
    if not user:
        raise StopValidation('incorrect credentials')

def verifyPassword(form,field):
    if user and not user.checkPassword(field.data):
        raise ValidationError('incorrect credentials')

class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired('email required'),verifyEmail])
    password = StringField('password',validators=[DataRequired('password required'),verifyPassword])
