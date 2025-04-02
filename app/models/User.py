from .db import db,environment, SCHEMA
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, LoginManager

login_manager = LoginManager()

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    if environment == 'production':
        __table_arg__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(80), nullable = False)
    last_name = db.Column(db.String(80),nullable = False)
    email = db.Column(db.String(150),nullable = False)
    hashed_password = db.Column(db.String(200),nullable = False)
    username = db.Column(db.String(50),nullable = False)
    room_id = db.Column(db.Integer,db.ForeignKey('rooms.id'),nullable = True)
    room = db.relationship('Room',back_populates='members')
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self,password):
        self.hashed_password = generate_password_hash(password)

    def checkPassword(self,password):
        return check_password_hash(self.hashed_password,password)

    def to_dict(self):
        return{
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'username':self.username
        }
