import pytest
import mongomock

from dotenv import find_dotenv, load_dotenv

from words import DICTIONARY
import random


def randomish_text():
    # List of words

    # Generate a random number of words to select
    num_words = random.randint(1, 5)  # Change the range according to your preference

    # Select random words from the list
    random_words = [random.choice(DICTIONARY) for _ in range(num_words)]

    # Join the selected words into a string
    return " ".join(random_words)


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
    """GIVEN the app
    WHEN I post a new item
    THEN I can see the text of the new item on the page
    """
    text = randomish_text()
    client.post("/additem", data={"title": text, "submit": "Add"})

    response = client.get("/")

    assert 200 == response.status_code
    assert text in response.data.decode()
