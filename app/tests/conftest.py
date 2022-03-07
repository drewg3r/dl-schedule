import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db
from models import User, ApiToken


@pytest.fixture(scope='session')
def client():
    flask_app = create_app('config.TestConfig')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    test_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    with test_client:
        yield test_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='class')
def temp_db():
    # Create the database and the database table
    db.create_all()
    add_test_data(db)

    yield db  # this is where the testing happens!

    db.drop_all()


def add_test_data(db):
    hashed_password = generate_password_hash('1234')
    user = User(username='test_user', email='test_email', password=hashed_password)
    primary_api_token = ApiToken(name='Primary API key', is_primary=True, user=user)
    db.session.add(user, primary_api_token)
    db.session.commit()


@pytest.fixture(scope='class')
def test_user():
    return User.query.get(1)
