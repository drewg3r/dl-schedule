import uuid
from datetime import date

import flask_login
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID

from app import db


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

class User(db.Model, flask_login.UserMixin):
    """
    Model for all users.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    subjects = db.relationship('Subject', back_populates='user')
    tokens = db.relationship('ApiToken', back_populates='user')

    @property
    def events(self):
        events = []
        for subject in self.subjects:
            for event in subject.events:
                events.append(event)

        return events


class Subject(db.Model):
    """
    Representation for subjects at the university.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    name_abbr = db.Column(db.String(10), nullable=True)
    lecturer = db.Column(db.String(255), nullable=True)
    link = db.Column(db.String(1024), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='subjects')

    events = db.relationship('Event', back_populates='subject')

    @property
    def serialize(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'abbr': self.name_abbr,
            'lecturer': self.lecturer,
            'link': self.link
        }


class Event(db.Model):
    """
    Representation for single lesson in schedule.
    """
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    weekday = db.Column(db.Integer, nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', back_populates='events')

    @property
    def serialize(self) -> dict:
        return {
            'id': self.id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'start_time_str': self.start_time_str,
            'end_time_str': self.end_time_str,
            'weekday': self.weekday,
            'subject': self.subject.serialize
        }

    @property
    def user(self) -> User:
        return self.subject.user

    @property
    def start_time_str(self):
        return '{:02}:{:02}'.format(int(self.start_time//60), int(self.start_time % 60))

    @property
    def end_time_str(self):
        return '{:02}:{:02}'.format(int(self.end_time//60), int(self.end_time % 60))


class ApiToken(db.Model):
    """
    API tokens for users. Single user can has multiple API tokens.
    Used for authorization via REST API.
    """
    token = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    date_created = db.Column(db.Date, nullable=False, default=date.today())
    name = db.Column(db.String(255), nullable=True)
    is_primary = db.Column(db.Boolean, nullable=False, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='tokens')
