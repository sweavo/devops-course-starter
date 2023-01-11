""" Marvel Character Query tool 

The API contains extra wonk for authentication.  
    https://developer.marvel.com/documentation/authorization
"""

import hashlib
import json
import os
import requests
import urllib.parse as UP


PROXIES = { "http": "http://localhost:3128",
            "https": "http://localhost:3128"}

PUBLIC_KEY = '4e7701ebe8f8158383368664c6e029dc'
PRIVATE_KEY = 'c7dc815ef8c8eb1c53ce8f075da6d5210f0d1cde'

def convert_dict_to_querystring( dictionary ):
    """
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
        # TODO what if not success?
        data = response.json()
        with open(filename, 'w') as fp:
            json.dump(data,fp)

    return data

def retrieve_hero_by_name(name):
    """ Application level helper: retrieve, by any means, the json for a 
        named hero.
    """
    query = {
        'name': hero_name
    }

    url = session.request_url('/v1/public/characters', query)

    print(f'Debug: Requesting from {url}')

    body_data = retrieve_json(url)

    items = body_data['data']['results']

    if items:
        return items[0], body_data['attributionText']
    else:
        print('Error: Could not find "{hero_name}"')

if __name__ == "__main__":

    session = MarvelSession('https://gateway.marvel.com:443',PUBLIC_KEY,PRIVATE_KEY)

    hero_name = '3-D Man'
    hero_data, attribution = retrieve_hero_by_name(hero_name)
    description = hero_data['description']
    if len(description.strip()):
        print(f"Result: {description}")
    else:
        print(f'Info: "{hero_name}" did not have a description')

    print(attribution) # comply with Marvel ToS
