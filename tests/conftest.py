import pytest

from tests import client


@pytest.fixture
def no_board():
    client.delete('/api/v1/boards/0')


@pytest.fixture
def init_board():
    client.delete('/api/v1/boards/0')
    client.post('/api/v1/boards/')
