from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin

from app import login
from app import db

GRAVATER_URL = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'


class User(UserMixin, db.Model):
    """User model(use for make migrate), inherit login mixin"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # field no write db (use for model relation)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def avatar(self, size):
        digit = md5(self.email.lower().encode('utf-8')).hexdigest()
        return GRAVATER_URL.format(digit, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Representation method"""
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id: str):
    """Helper for load user with storage"""
    return User.query.get(int(id))


class Post(db.Model):
    """Post model(use for make migrate)"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Representation method"""
        return '<Post {}>'.format(self.body)
