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

    # Relationships
    events = db.relationship('Event', backref='creator', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    @property
    def full_name(self):
        return f"{self.firstname} {self.surname}"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    artist_name = db.Column(db.String(200), nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    tickets_available = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(400), nullable=True)
    status = db.Column(db.String(20), default='Open', nullable=False)
    category = db.Column(db.String(50), nullable=False)
    acknowledgement_type = db.Column(db.String(20), default='none', nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    orders = db.relationship('Order', backref='event', lazy=True)
    comments = db.relationship('Comment', backref='event', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_fee = db.Column(db.Float, default=1.50, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)