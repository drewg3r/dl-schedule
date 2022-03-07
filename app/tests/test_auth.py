import pytest

from models import User


class TestAuthentication:
    def test_sign_in_with_invalid_username(self, client, temp_db):
        response = client.post('/login',
                               data={
                                   'username': 'andrew',
                                   'password': '1234'
                               },
                               follow_redirects=True)
        assert response.status_code == 200
        assert 'Invalid username' in response.data.decode('UTF-8')

    def test_sign_in_with_invalid_password(self, client, temp_db):
        response = client.post('/login',
                               data={
                                   'username': 'test_user',
                                   'password': 'some_password'
                               },
                               follow_redirects=True)
        assert response.status_code == 200
        assert 'Invalid password' in response.data.decode('UTF-8')

    def test_sign_in_with_valid_credentials(self, client, temp_db):
        response = client.post('/login',
                               data={
                                   'username': 'test_user',
                                   'password': '1234'
                               },
                               follow_redirects=True)
        assert response.status_code == 200
        assert 'Today' in response.data.decode('UTF-8')

    def test_sign_up(self, client, temp_db):
        response = client.post('/signup',
                               data={
                                   'username': 'test_username',
                                   'email': 'some_email@server.com',
                                   'password': '1234',
                                   'password2': '1234'
        },
                               follow_redirects=True)
        assert response.status_code == 200
        assert 'test_username' in [user.username for user in User.query.all()]
