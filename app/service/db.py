from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Subject, Event, ApiToken
from service.subject import create_subject
from service.event import create_event


def create_demo_db(db):
    '''
    Fill database with demo data if DEMO_MODE is turned on.
    '''

    # Exit if db is not empty
    if User.query.all():
        return

    hashed_password = generate_password_hash('1234')
    user = User(username='demo', email='demo@email.com', password=hashed_password)
    primary_api_token = ApiToken(name='Primary API key', is_primary=True, user=user)

    db.session.add(user, primary_api_token)
    db.session.commit()

    anth = create_subject('Anthropology', 'ANTH', 'Dr. Christina Getrich', 'https://example.com', user)
    baac = create_subject('Business Administration and Accounting', 'BAAC', 'Jeffery Klauda', 'https://example.com', user)
    cnee = create_subject('Civil and Environmental Engineering', 'CNEE', 'Jeffery Klauda', 'https://example.com', user)
    cse = create_subject('Cybersecurity Engineering', 'CSE', 'Caitlin Gover', 'https://example.com', user)
    ehs = create_subject('Environmental Health Sciences', 'EHS', 'Paul C. Turner', 'https://example.com', user)
    hihp = create_subject('History and Historic Preservation', 'HIHP', 'Jeremy Wells', 'https://example.com', user)
    math = create_subject('Mathematics', 'MATH', 'Cristina Garcia', 'https://example.com', user)

    create_event(ehs, 510, 605, 0)
    create_event(baac, 625, 720, 0)
    create_event(anth, 740, 835, 0)
    create_event(math, 855, 950, 0)

    create_event(cse, 510, 605, 1)
    create_event(math, 625, 720, 1)

    create_event(hihp, 510, 605, 2)
    create_event(math, 625, 720, 2)
    create_event(anth, 740, 835, 2)

    create_event(ehs, 510, 605, 3)
    create_event(baac, 625, 720, 3)
    create_event(math, 740, 835, 3)

    create_event(cse, 510, 605, 4)
    create_event(cnee, 625, 720, 4)
    create_event(ehs, 740, 835, 4)
    create_event(anth, 855, 950, 4)
