import flask_login

from app import db


class User(db.Model, flask_login.UserMixin):
    """
    Just user model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    subjects = db.relationship('Subject', back_populates='user')

    def __str__(self):
        return f'<User {self.username}>'


class Subject(db.Model):
    """
    Model for university subjects
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    name_abbr = db.Column(db.String(10), nullable=True)
    lecturer = db.Column(db.String(255), nullable=True)
    link = db.Column(db.String(1024), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='subjects')

    events = db.relationship('Event', back_populates='subject')

    def __str__(self):
        return f'<Subject {self.name}'


class Event(db.Model):
    """
    Event in schedule. Places subject to specified time
    """
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    weekday = db.Column(db.Integer, nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', back_populates='events')
