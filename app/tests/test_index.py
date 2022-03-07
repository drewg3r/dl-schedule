from models import User
from service.event import get_event


def test_index_page(client, temp_db):
    """Test index page accessibility"""
    response = client.get('/')
    assert response.status_code == 200


def test_index_page2(client, temp_db):
    response = client.get('/')
    assert b'schedule' in response.data


def test_login(client, temp_db):
    response = client.post('/login',
                           data={
                               'username': 'andrew',
                               'password': '1234'
                           },
                           follow_redirects=True)

    assert b'Invalid' in response.data


def test_signup(client, temp_db):
    response = client.post('/signup',
                           data={
                               'username': 'andrew',
                               'email': 'somemail',
                               'password': '1234',
                               'password2': '1234'
                           },
                           follow_redirects=True)

    assert 'Week' in response.data.decode('UTF-8')

    user = User.query.get(1)
    assert user is not None


def test_db(client, temp_db):
    event = get_event(1)
    assert event is None
