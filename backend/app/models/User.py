from .db import db,environment, SCHEMA
class User(db.Model):
    __tablename__ = 'users'
    if environment == 'production':
        __table_arg__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(80), nullable = False)
    last_name = db.Column(db.String(80),nullable = False)
    email = db.Column(db.String(150),nullable = False)

    def to_dict(self):
        return{
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email
        }
