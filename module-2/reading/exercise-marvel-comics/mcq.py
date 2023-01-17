""" Marvel Character Query tool

Notes:
    * The API contains extra wonk for authentication, so the authentication is
      encapsulated in the MarvelSession class.  "Session" is a little misleading
      because the server is not aware of any session continuity; but class holds the
      authentication credentials, so to the user of the class it feels like a
      session. See https://developer.marvel.com/documentation/authorization

    * Having to re-get information from the API was slowing development, so I
      implemented local caching.  Since the data is immutable, I hash the url and
      querystring to make a filename, and throw the json in there.

TODO:
    Merge the list all characters with the list one character by using name
    What when the character provided on the CLI doesn't exist?

"""

import argparse
import hashlib
import json
import os
import requests
import urllib.parse as UP

def derive_proxy_settings(environ):
    """ read the environment for proxy variables and generate key-value pairs for a
        dict for requests module to use. This is a function so that I can avoid
        mutating PROXIES, which should be treated as a constant, in global scope.

    >>> dict(derive_proxy_settings({'http_proxy': 'hello, mum'}))
    {'http': 'hello, mum'}

    """
    if 'http_proxy' in environ:
        yield 'http', environ['http_proxy']
    if 'https_proxy' in environ:
        yield 'https', environ['https_proxy']


PROXIES = dict(derive_proxy_settings(os.environ))

PUBLIC_KEY = '4e7701ebe8f8158383368664c6e029dc'
PRIVATE_KEY = 'c7dc815ef8c8eb1c53ce8f075da6d5210f0d1cde'

def convert_dict_to_querystring( dictionary ):
    """
        This test is here because at first I hand-rolled the functionality, then
        later googled for a better way and refactored. The doctests are the contract
        for the function, and still stand.

        >>> convert_dict_to_querystring( {'a': 'b', 'c': 'd'} )
        '?a=b&c=d'
        >>> convert_dict_to_querystring( {'a': 'b', 'c': 'hello there'} )
        '?a=b&c=hello+there'
        >>> convert_dict_to_querystring( {'a': 'b', 'c': 'hello"there'} )
        '?a=b&c=hello%22there'
    """
    return '?' + UP.urlencode(dictionary,doseq=False)

class MarvelSession(object):
    def __init__(self, root_url, public_key, private_key):
        self._root_url = root_url
        self._public_key = public_key
        self._private_key = private_key
        self._sequence=0

    def request_url(self, path, query_dict):
        """ Encapsulate the wonk for the Marvel API authentication.
        query_dict contains the arguments for the query, which are merged
        into the needed auth query items. """

        self._sequence+=1
        ts=self._sequence

        hashable = str(ts) + self._private_key + self._public_key
        hash_string = hashlib.md5( hashable.encode('UTF-8')).hexdigest()

        query_items = {
            'ts': str(ts),
            'hash': hash_string,
            'apikey': self._public_key
        }

        # merge in the
        for k in query_dict:
            query_items[k] = query_dict[k]

        query_string = convert_dict_to_querystring(query_items)

        return f'{self._root_url}{path}{query_string}'

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
        response = requests.get(url,proxies=PROXIES)

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
    """ So that we can interact happily with the data, retrieve a list of valid names
    """

    characters=[]

    limit, offset = 100 ,0

    query_string={
        'nameStartsWith': name_stem,
        'limit': str(limit)
    }

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
    print(f'Retrieved {count} items...')

if __name__ == "__main__":

    arguments=configure_argument_parsing().parse_args()

    session = MarvelSession('https://gateway.marvel.com:443',PUBLIC_KEY,PRIVATE_KEY)

    characters, attribution = retrieve_characters_by_part_name(arguments.SEARCH_TERM, progress)

    for character in characters:
        print(f"{character['name']:30s} | {character['description'] or '(no description)'}")

    print(attribution)