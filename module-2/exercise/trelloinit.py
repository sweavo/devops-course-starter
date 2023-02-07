""" Trello config initializer.

Given your API_KEY and TOKEN it will let you navigate to a board and give you some 
initializing information for your API app.

Interactive prompts are to stderr so that it can be used in a pipe. 
Run in the following way:

    python trelloinit.py | tee trello_config.py

"""
import argparse
import hashlib
import json
import os
import requests
import sys

import dotenv
from TrelloSession import TrelloSession
import requests_proxy_config


dotenv.load_dotenv()

API_KEY=os.getenv('TRELLO_API_KEY')
TOKEN=os.getenv('TRELLO_TOKEN')

PROXIES=requests_proxy_config.from_env()

def retrieve_json(url):
    """ REST API helper for calls returning volatile results (i.e. can change behind our back).
    """

    response = requests.get(url,proxies=PROXIES)

    if response.status_code != 200:
        # note: bail out before writing the cache :)
        raise RuntimeError(f"Server response code {response.status_code}")

    data = response.json()

    return data

def peep_data(data):
    if isinstance(data, dict):
        print(data.keys())
    else:
        for item in data:
            peep_data(item)

if __name__ == "__main__":

    session = TrelloSession('https://api.trello.com',API_KEY, TOKEN)

    url = session.request_url(f'/1/member/me/boards/')
    boards = retrieve_json(url)
    print('Connect OK.', file=sys.stderr)
    
    while True:
        for number, board in enumerate(boards):
            print(f'{number:#2d}: {board["name"]}', file=sys.stderr)
        print('Choose: ', file=sys.stderr, end='')
        choice=int(input())
        if choice < len(boards):
            break
    
    board_id = boards[choice]['id']
    
    print(f"BOARD_ID='{board_id}'")

    url = session.request_url(f'/1/boards/{board_id}/lists/' )
    data = retrieve_json(url)

    as_dict = { trello_list["name"]: trello_list["id"] for trello_list in data}
    print(f'LISTS={as_dict}')
