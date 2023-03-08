import re
import pytest
import requests

from dotenv import find_dotenv, load_dotenv
from todo_app import app

RE_API = re.compile('^https://api.trello.com/1/boards?/[a-z0-9]+/lists')


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')

    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)

    response = client.get('/')

    assert 'hello' in response.data


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
        self.status_code = 200

    def json(self):
        return self.fake_response_data


def stub(url, params={}, proxies=None, verify=None):
    m = RE_API.match(url)
    if m:
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card'}]
        }]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')
