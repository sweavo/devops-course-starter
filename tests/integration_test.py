import pytest

import dotenv
from todo_app import app


@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client
