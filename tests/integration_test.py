"""
    A happy-path smoke-test that the app can serve its root page, getting data
    like in board_result.json.  In the event that the trello API breaks, this
    file would need to be repopulated via a trello API get.
"""
import json
import pytest
import re
import requests

from dotenv import find_dotenv, load_dotenv
from todo_app import app

# How to recognize an incoming request for the trello boards, regardless of the authentication given
RE_API = re.compile("^https://api.trello.com/1/boards?/[a-z0-9]+/lists")


class StubResponseTrello:
    """Fake Response object from our stubbed requests module"""

    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
        self.status_code = 200

    def json(self):
        return self.fake_response_data


def stub_requests_get_trello(url, params={}, proxies=None, verify=None):
    """Stub requests.get so that the app under test gets our injected data"""
    m = RE_API.match(url)
    if m:
        with open("tests/test_data/board_result.json", "r") as fp:
            board_json = json.load(fp)
        return StubResponseTrello(board_json)

    raise Exception(f'Integration test did not expect URL "{url}"')


@pytest.fixture
def client():
    """Fixture to connect networklessly to the todo app"""

    file_path = find_dotenv(".env.test")

    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    """GIVEN a trello board containing an item called "second item"
    WHEN we get the root URL of our app
     THEN we can find the text "second item" on the page
    """
    monkeypatch.setattr(requests, "get", stub_requests_get_trello)
    response = client.get("/")

    assert 200 == response.status_code
    assert "second item" in response.data.decode()
