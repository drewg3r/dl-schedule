import datetime

from sqlalchemy import asc

from app import db
from exceptions import AccessDeniedException, EventNotFoundException
from models import User, Subject, Event


def create_event(subject: Subject, start_time: int,
                 end_time: int, weekday: int) -> Event:
    """
    Create new Event in database and return it.
    :param subject: instance of Subject model class
    :param start_time: event start time in minutes from the start of the day
    :param end_time: event end time in minutes from the start of the day
    :param weekday: number of weekday starting from 0(Monday)
    :return: created Event
    """
    event = Event(start_time=start_time,
                  end_time=end_time,
                  weekday=weekday,
                  subject=subject)

    db.session.add(event)
    db.session.commit()

    return event


def get_event(event_id: int) -> Event:
    """
    Return Event model class instance by it's id.
    """
    return Event.query.get(event_id)


def get_event_safe(user: User, event_id: int) -> Event:
    """
    Safe version of get_event method.
    Raise AccessDeniedException if provided user is not owner of event.
    Raise EventNotFoundException if no event found with provided id.
    :param user: instance of User model class
    :param event_id: requested Event id
    :return: instance of Event model class
    """
    event = get_event(event_id)
    if event:
        if event.subject.user == user:
            return event
        else:
            raise AccessDeniedException
    else:
        raise EventNotFoundException


def get_all_events(user: User) -> tuple[Event] | None:
    """
    Return all events that provided user have.
    :param user: instance of User model class
    :return: tuple of Events or None if no Events were found
    """
    return user.events


def delete_event(event_id: int) -> None:
    """
    Delete Event with provided id.
    Raise EventNotFoundException if no event found with provided id.
    :param event_id: requested Event id
    :return: None
    """
    event = get_event(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
    else:
        raise EventNotFoundException


def delete_event_safe(user: User, event_id: int) -> None:
    """
    Safe version of delete_event method.
    Raise AccessDeniedException if provided user is not owner of event.
    Raise EventNotFoundException if no event found with provided id.
    :param user: instance of User model class
    :param event_id: requested Event id
    :return: None
    """
    event = get_event_safe(user, event_id)
    db.session.delete(event)
    db.session.commit()


def get_events_by_weekday(user: User, weekday: int) -> tuple[Event]:
    """
    Return all events that belong to provided user and have provided weekday.
    Return None if no events were found.
    :param user: instance of User model class
    :param weekday: number of weekday starting from 0(Monday)
    :return: found Events
    """
    return Event.query \
        .join(Event.subject, aliased=True) \
        .filter(Subject.user == user, Event.weekday == weekday)


def get_today_events(user: User) -> tuple[Event]:
    """
    Get events that provided user has today.
    """
    return get_events_by_weekday(user, datetime.date.today().weekday())


def get_tomorrow_events(user: User) -> tuple[Event]:
    """
    Get events that provided user has tomorrow.
    """
    return get_events_by_weekday(
        user,
        (datetime.date.today()+datetime.timedelta(days=1)).weekday()
    )


def get_current_event(user: User) -> Event | None:
    """
    Get event that provided user has right now.
    """
    current_time = datetime.datetime.now().hour*60 + datetime.datetime.now().minute
    return Event.query \
        .join(Event.subject, aliased=True) \
        .filter(Subject.user == user,
                Event.weekday == datetime.date.today().weekday(),
                Event.start_time <= current_time,
                Event.end_time > current_time
                ) \
        .order_by(asc(Event.start_time)).first()


def get_next_event(user: User) -> Event | None:
    """
    Get event that provided user has next.
    """
    current_time = datetime.datetime.now().hour*60 + datetime.datetime.now().minute
    return Event.query \
        .join(Event.subject, aliased=True) \
        .filter(Subject.user == user,
                Event.weekday == datetime.date.today().weekday(),
                Event.start_time > current_time,
                ) \
        .order_by(asc(Event.start_time)).first()
