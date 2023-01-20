""" Trello query tool


"""

import argparse
import hashlib
import json
import os
import requests
import sys


from TrelloSession import TrelloSession
import requests_proxy_config

PROXIES=requests_proxy_config.from_env()

API_KEY='5f0957ceb14e45bc554b6677ba2a408b'
TOKEN='ATTA2f78d45f7119de92b67bdae7eef91ef0449fb13850675b81b88285c2b0f400af7C6C9D49'

REQUESTS_VERIFY=os.environ.get('USERDOMAIN')=='EMEA' # Because the corporate network certificate is broken, we have to turn off certificate verification to talk to anyone who has SOTA authentication.

def retrieve_json(url):
    """ REST API helper for calls returning const results.

        Since the work network is slow, cache the results of unique requests.

        Cache does not expire, so don't use it on mutable data!
    """

    filename=".cache." + hashlib.md5(url.encode('utf-8')).hexdigest()

    if os.path.exists(filename):
        with open(filename,'r') as fp:
            data = json.load(fp)

    else:
        response = requests.get(url,proxies=PROXIES,
                                verify=REQUESTS_VERIFY # Lel, because of our security policies
                                )

        if response.status_code != 200:
            # note: bail out before writing the cache :)
            raise RuntimeError(f"Server response code {response.status_code}")

        data = response.json()
        with open(filename, 'w') as fp:
            json.dump(data,fp)

    return data

def retrieve_character_by_name(character_name):
    """ Application level helper: retrieve, by any means, the json for a
        named character.
    """
    query = {
        'name': character_name
    }

    url = session.request_url('/v1/public/characters', query)

    print(f'Debug: Requesting from {url}')

    body_data = retrieve_json(url)

    items = body_data['data']['results']

    if items:
        return items[0], body_data['attributionText']
    else:
        print('Error: Could not find "{character_name}"')

def configure_argument_parsing():
    ap = argparse.ArgumentParser('mcq')
    ap.add_argument('SEARCH_TERM', default='', nargs='?', help='The first part of the name of a character. If omitted, all characters will be listed.')
    return ap

def retrieve_characters_by_part_name(name_stem, progress_callback):
    """ Get the names returned by using the nameStartsWith argument of the Marvel
        API.  Since it doesn't allow nameStartsWith "" then we have to omit the
        argument if it is empty, in order to get the same effect.

        The function handles pagination of results, and returns the attributionText
        from the top of the response body structure as well as a list of all the
        characters received across all pages of body.data.results
    """

    characters=[]

    limit, offset = 100 ,0

    query_string={
        'limit': str(limit)
    }

    if name_stem:
        query_string['nameStartsWith'] = name_stem

    while True: # do while result_count==limit

        query_string['offset'] = str(offset)
        url = session.request_url('/v1/public/characters',query_string)

        body_data = retrieve_json(url)

        result_count = int(body_data['data']['count'])
        offset += result_count

        characters.extend( body_data['data']['results'] )

        progress_callback(offset)

        if result_count<limit:
            break

    return characters, body_data['attributionText']

def progress(count):
    print(f'Retrieved {count} items...', file=sys.stderr)

if __name__ == "__main__":

    arguments=configure_argument_parsing().parse_args()

    session = TrelloSession('https://api.trello.com',API_KEY, TOKEN)

    url = session.request_url('/1/members/me/boards')

    data = retrieve_json(url)
    
    print(data[0].keys())
