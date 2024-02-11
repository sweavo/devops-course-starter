"""
    A happy-path smoke-test that the app can serve its root page, getting data
    like in board_result.json.  In the event that the trello API breaks, this
    file would need to be repopulated via a trello API get.
"""
import pytest
import mongomock

from dotenv import find_dotenv, load_dotenv


@pytest.fixture
def client():
    """Fixture to connect networklessly to the todo app"""

    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    from todo_app import app

    with mongomock.patch(servers=(("fakemongo.com", 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client


def test_index_page_trello(client):
    """GIVEN a trello board containing an item called "second item"
    WHEN we get the root URL of our app
     THEN we can find the text "second item" on the page
    """

    response = client.get("/")

    assert 200 == response.status_code
    assert "second item" in response.data.decode()
