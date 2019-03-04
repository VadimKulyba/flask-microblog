from datetime import datetime
from app import db


class User(db.Model):
    """User model(use for make migrate)"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        """Representation method"""
        return '<User {}>'.format(self.username)


class Post(db.Model):
    """Post model(use for make migrate)"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Representation method"""
        return '<Post {}>'.format(self.body)
