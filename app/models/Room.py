from app.models import db
import datetime
from app.models import SCHEMA, environment
class Room(db.Model):
    __tablename__ = 'rooms'
    if environment == 'production':
        __table_arg__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    members = db.relationship('User', back_populates='room')
    messages = db.Column(db.String(255), nullable=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Room %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'members': [member.to_dict() for member in self.members],
            'messages': self.messages
        }
