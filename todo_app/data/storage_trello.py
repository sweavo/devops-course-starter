import os 

from flask import session

from .TrelloSession import TrelloSession
from .. import trello_config

import dotenv

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]

dotenv.load_dotenv()
trello = TrelloSession('https://api.trello.com', 
    os.getenv('TRELLO_API_KEY'), 
    os.getenv('TRELLO_TOKEN') )

def peep_data(data):
    if isinstance(data, dict):
        print(data.keys())
    else:
        for item in data:
            peep_data(item)

def get_items():
    """
    Fetches all saved items from trello

    Returns:
        list: The list of saved items.
    """

    results = []
    for list_id in trello_config.LISTS.values():
        url = trello.request_url(f'/1/lists/{list_id}/cards' )
        data = trello.retrieve_json(url)
        for card in data:
            results.append( { 'id': card['id'],
                              'status': card['idList'],
                              'title': card['name'] })
    return results


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1]['id'] + 1 if items else 0

    item = { 'id': id, 'title': title, 'status': 'Not Started' }

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item
