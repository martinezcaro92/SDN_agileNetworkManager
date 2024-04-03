import pytest
import pdb
from starlette.testclient import TestClient

from main import app

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here


# def main():
#     # Crear una instancia de APIHandler
#     print (os.getcwd())

    
#     print(path.parent.absolute())
# if __name__ == '__main__':
#     main()
