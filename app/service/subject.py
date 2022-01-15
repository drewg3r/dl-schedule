from sqlalchemy import func

from app import db
from exceptions import DuplicateSubjectNameException, SubjectNotFoundException, AccessDeniedException
from models import Subject, User


def get_subjects(user: User) -> list[Subject]:
    """
    Return all Subjects that belong to provided User. Subjects are
    sorted by name.
    :param user: instance of User model class
    :return: list of sorted Subjects
    """
    return sorted(user.subjects, key=lambda x: x.name)


def get_subject(subject_id: int) -> Subject:
    """
    Return Subject by its id or None if Subject was not found
    :param subject_id: requested Subject's id
    :return: Subject instance
    """
    return Subject.query.get(subject_id)


def get_subject_safe(user: User, subject_id: int) -> Subject:
    """
    Safe version of get_subject method. Check if provided User have access
    to Subject.
    Return Subject if it exists. Otherwise raise SubjectNotFoundException.
    Raise AccessDeniedException if provided User does not have access to Subject.
    :param user: instance of User model class
    :param subject_id: requested Subject's id
    :return: Subject
    """
    subject = get_subject(subject_id)

    if subject:
        if subject.user == user:
            return subject
        else:
            raise AccessDeniedException
    else:
        raise SubjectNotFoundException


def create_subject(name: str, abbr: str, lecturer: str,
                   link: str, user: User) -> Subject:
    """
    Create new Subject for specified user and return it.
    :param name: new Subject's name
    :param abbr: new Subject's abbreviation
    :param lecturer: new Subject's lecturer
    :param link: new Subject's lesson link
    :param user: instance of User model class
    :return: newly created Subject
    """
    if name in [subject.name for subject in user.subjects]:
        raise DuplicateSubjectNameException
    subject = Subject(name=name,
                      name_abbr=abbr,
                      lecturer=lecturer,
                      link=link,
                      user=user)
    db.session.add(user)
    db.session.commit()
    return subject


def delete_subject_safe(user: User, subject_id: int) -> None:
    """
    Delete Subject by provided Subject's id.
    Raise AccessDeniedException if provided User does not
    have access to the Subject.
    :param user: instance of User model class
    :param subject_id: Subject's id to delete
    :return: None
    """
    subject = get_subject_safe(user, subject_id)
    db.session.delete(subject)
    db.session.commit()


def update_subject_safe(user: User, subject_id: int, name: str = None,
                        abbr: str = None, lecturer: str = None,
                        link: str = None) -> Subject:
    """
    Update Subject by provided Subject's id.
    Raise AccessDeniedException if provided User does not
    have access to the Subject.
    Raise SubjectNotFoundException if Subject with provided
    id does not exist.
    """
    subject = get_subject_safe(user, subject_id)

    subject.name = name or subject.name
    subject.name_abbr = abbr or subject.name_abbr
    subject.lecturer = lecturer or subject.lecturer
    subject.link = link or subject.link
    db.session.commit()
    return subject


def search_subject(subject_name: str, user: User) -> tuple[Subject]:
    """
    Return provided User's subjects that contain provided str in name.
    Return None if nothing was found.
    :param subject_name: Subject's name to search for
    :param user: instance of User model class
    :return: found Subjects
    """
    return Subject.query.filter(
        func.lower(Subject.name).contains(func.lower(subject_name)),
        Subject.user == user)
