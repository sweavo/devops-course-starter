import os 

from flask import session
import dotenv
import requests

from .TrelloSession import TrelloSession
from .. import trello_config


_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]

dotenv.load_dotenv()
trello = TrelloSession('https://api.trello.com', 
    os.getenv('TRELLO_API_KEY'), 
    os.getenv('TRELLO_TOKEN') )

def peep_data(data):
    """ Handy debug tool to see the structure of a response """
    if isinstance(data, dict):
        print(data.keys())
    else:
        for item in data:
            peep_data(item)

   
def trello_to_card(trello_card):
    return { 'id': trello_card['id'],
            'status': trello_card['idList'],
            'title': trello_card['name'] }


def card_to_trello(card):
    """ Assumption: we only receive a todo card that has all of id, status,
        title, and that the status is the name of a trello list that existed 
        when the process started
    """
    id_of_list = trello_config.LISTS[card['status']]
    
    return { 'id': card['id'],
            'idList': id_of_list,
            'name': card['title'] }


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
            results.append( trello_to_card( card ) )
            
    return results


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    print('XXX get TODO untested') 
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
    not_started_list = trello_config.LISTS['Not Started']

    url = trello.request_url('/1/cards',{'name': title, 'idList': not_started_list})

    response = requests.post(url)
    
    return trello_to_card(response.json())


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    print('XXX save TODO untested')
    trello_card = card_to_trello(item)

    url = trello.request_url(f'/1/cards/{trello_card["id"]}', trello_card)

    response = requests.put(url)

    return trello_to_card(response.json())
