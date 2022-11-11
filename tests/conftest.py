import pytest
from server import app


@pytest.fixture
def client():
    client = app.test_client()
    return client
