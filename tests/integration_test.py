import json
import pytest
import re
import requests

from dotenv import find_dotenv, load_dotenv
from todo_app import app

# How to recognize an incoming request for the boards, regardless of the authentication given
RE_API = re.compile("^https://api.trello.com/1/boards?/[a-z0-9]+/lists")


class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
        self.status_code = 200

    def json(self):
        return self.fake_response_data


def stub_requests_get(url, params={}, proxies=None, verify=None):
    m = RE_API.match(url)
    if m:
        with open("tests/test_data/board_result.json", "r") as fp:
            board_json = json.load(fp)
        return StubResponse(board_json)

    raise Exception(f'Integration test did not expect URL "{url}"')


@pytest.fixture
def client():
    """Fixture to connect networklessly to the app"""

    file_path = find_dotenv(".env.test")

    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, "get", stub_requests_get)
    response = client.get("/")

    assert 200 == response.status_code
    assert "second item" in response.data.decode()
