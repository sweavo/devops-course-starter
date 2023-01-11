""" Marvel Character Query tool 

The API contains extra wonk for authentication.  
    https://developer.marvel.com/documentation/authorization
"""

import hashlib
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


if __name__ == "__main__":

    session = MarvelSession('https://gateway.marvel.com:443',PUBLIC_KEY,PRIVATE_KEY)
    
    hero_name = '3-D Man'

    query = {
        'name': hero_name
    }

    url = session.request_url('/v1/public/characters', query)

    print(f'Debug: Requesting from {url}')

    response = requests.get(url,proxies=PROXIES)

    # TODO what if not success?

    body_data = response.json()

    items = body_data['data']['results']

    if items:
        description = items[0]['description']
        if len(description.strip()):
            print(f"Result: {description}")
        else:
            print(f'Info: "{hero_name}" did not have a description')
    else:
        print('Error: Could not find "{hero_name}"')

    print(body_data['attributionText']) # comply with Marvel ToS

