from app import APP
import pytest

@pytest.fixture
def app():
    return APP