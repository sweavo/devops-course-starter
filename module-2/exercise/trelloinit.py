""" Trello config initializer.

Given your API_KEY and TOKEN it will let you navigate to a board and give you some 
initializing information for your API app.

Interactive prompts are to stderr so that it can be used in a pipe. 
Run in the following way:

    python trelloinit.py | tee trello_config.py

"""
API_KEY='5f0957ceb14e45bc554b6677ba2a408b'
TOKEN='ATTA2f78d45f7119de92b67bdae7eef91ef0449fb13850675b81b88285c2b0f400af7C6C9D49'

import argparse
import hashlib
import json
import os
import requests
import sys

from TrelloSession import TrelloSession
import requests_proxy_config

PROXIES=requests_proxy_config.from_env()

REQUESTS_VERIFY=os.environ.get('USERDOMAIN')!='EMEA' # Because the corporate network certificate is broken, we have to turn off certificate verification to talk to anyone who has SOTA authentication.
if not REQUESTS_VERIFY:
    print('Warning: skipping certificated verfication b/c of corporate wonk', file=sys.stderr)

def retrieve_json(url):
    """ REST API helper for calls returning volatile results (i.e. can change behind our back).
    """

    response = requests.get(url,proxies=PROXIES,
                            verify=REQUESTS_VERIFY # Lel, because of our security policies
                            )

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
    
    print(f'''
API_KEY='{API_KEY}'
TOKEN='{TOKEN}'
''')
    print(f"BOARD_ID='{board_id}'")

    url = session.request_url(f'/1/boards/{board_id}/lists/' )
    data = retrieve_json(url)
    print('LISTS={')
    for trello_list in data:
        print(f'  "{trello_list["name"]}": "{trello_list["id"]}"')
    print('}')
