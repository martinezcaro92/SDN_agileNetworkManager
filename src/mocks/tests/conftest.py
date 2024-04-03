import pytest, os
from starlette.testclient import TestClient
print(os.getcwd())
from sdn_controllers import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here