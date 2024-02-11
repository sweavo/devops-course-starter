import os
from pymongo import MongoClient


# Establish connection to MongoDB
class LazyMongoSession:
    """Extra complexity here, because we don't want to execute the connection code
    on a simple import, since test_view_model wants to play with the Card class
    below.  Card couples the business object to the persistence layer, making a
    bad smell.
    """

    def __init__(self, uri):
        self._uri = uri
        self._collection = None

    def collection(self):
        if not self._collection:
            database_client = MongoClient(os.getenv("MONGODB_URI"))
            db = database_client.get_database("todo_app")
            self._collection = db.get_collection("cards")
        return self._collection


assert "MONGODB_URI" in os.environ
mongosession = LazyMongoSession(os.getenv("MONGODB_URI"))

VALID_STATUSES = ["Not Started", "Done"]


class HTTP401Exception(RuntimeError):
    pass


class Card(object):
    """
    Sort-of POD for a todo card, but coupled to trello because of its
    conversion methods
    """

    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        if status not in VALID_STATUSES:
            raise ValueError(
                f'Attempt to create a card with status "{status}", which was not in {VALID_STATUSES}.'
            )
        self.status = status

    def to_dict(self):
        """Return dictionary representation of the card"""
        return {"_id": self.id, "title": self.title, "status": self.status}

    @classmethod
    def from_dict(cls, card_dict):
        """Factory to create Card from a dictionary"""
        return cls(card_dict["_id"], card_dict["title"], card_dict["status"])


def get_items():
    """
    Fetches all saved items from MongoDB

    Returns:
        list: The list of saved items.
    """
    results = []
    for card_data in mongosession.collection.find():
        results.append(Card.from_dict(card_data))
    return results


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    return mongosession.collection.find_one({"_id": id})


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    card_data = {"title": title, "status": "Not Started"}
    result = mongosession.collection.insert_one(card_data)
    card_data["_id"] = result.inserted_id
    return Card.from_dict(card_data)


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    card_data = item.to_dict()
    mongosession.collection.update_one({"_id": card_data["_id"]}, {"$set": card_data})
