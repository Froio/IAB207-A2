from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    surname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @property
    def full_name(self):
        return f"{self.firstname} {self.surname}"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)