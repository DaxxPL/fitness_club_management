import pytest
from fitness_club_manager import main


@pytest.fixture()
def app():
    main.app.testing = True
    yield main.app.test_client()


def test_working_web(app):
    resp = app.get('/').status_code
    assert resp == 200
