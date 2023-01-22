import os 

from flask import session
import dotenv
import requests

from .TrelloSession import TrelloSession
from .. import trello_config

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

VALID_STATUSES=trello_config.LISTS.keys()

class Card(object):
    """ Sort-of POD for a todo card, but coupled to trello because of its 
        conversion methods
    """
    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        if status not in VALID_STATUSES:
            raise ValueError(f'Attempt to create a card with status "{status}", which was not in {VALIDstatusES}.')
        self.status = status

    def to_trello(self):
        
        id_of_list = trello_config.LISTS[self.status]
        
        return { 'id': self.id,
                'idList': id_of_list,
                'name': self.title }

    @classmethod
    def from_trello(cls, trello_card):        
        # Look up the key of the dict given its value. Behavior is not defined if 
        # it's not present.
        for status in trello_config.LISTS.keys():
            if trello_config.LISTS[status] == trello_card['idList']:
                break

        return cls(trello_card['id'], trello_card['name'], status)


def get_items():
    """
    Fetches all saved items from trello

    Returns:
        list: The list of saved items.
    """
    results = []

    board_id = trello_config.BOARD_ID

    url = trello.request_url(f'/1/board/{board_id}/lists/', {'cards': 'open'} )
    data = trello.retrieve_json(url)
    for trello_list in data:
        results.extend(map(Card.from_trello, trello_list['cards']))
            
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
    return next((item for item in items if item.id == id), None)


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
    
    return Card.from_trello(response.json())


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    print('XXX save TODO untested')
    trello_card = item.to_trello()

    url = trello.request_url(f'/1/cards/{trello_card["id"]}', trello_card)

    response = requests.put(url)

    return Card.from_trello(response.json())
