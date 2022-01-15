import pytest

from app import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('config.TestConfig')
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
