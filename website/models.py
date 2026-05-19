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
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(300), nullable=True)
    headliner = db.Column(db.String(200), nullable=False)
    support_acts = db.Column(db.String(300), nullable=True)
    venue = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=True)
    capacity = db.Column(db.Integer, nullable=False)
    tickets_available = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    acknowledgement_type = db.Column(db.String(20), nullable=False, default='none')
    status = db.Column(db.String(20), nullable=False, default='Open')
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    creator = db.relationship('User', backref='events')
    comments = db.relationship('Comment', backref='event', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='event', cascade='all, delete-orphan')

    @property
    def date(self):
        # Format event_date like "Sat 19 Apr 2026"
        return self.event_date.strftime('%a %d %b %Y')

    @property
    def time(self):
        # Format start/end like "8:00 PM — 11:30 PM"
        # Strip leading zero from %I on platforms that don't support %-I
        start = self.start_time.strftime('%I:%M %p').lstrip('0')
        if self.end_time is None:
            return start
        end = self.end_time.strftime('%I:%M %p').lstrip('0')
        return f"{start} \u2014 {end}"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    user = db.relationship('User', backref='comments')

    @property
    def author(self):
        return self.user.full_name

    @property
    def date(self):
        return self.created_at.strftime('%d %b %Y')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    user = db.relationship('User', backref='orders')
