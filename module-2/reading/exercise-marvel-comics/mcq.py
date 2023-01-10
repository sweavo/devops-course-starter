""" Marvel Character Query tool 
"""

import hashlib
import requests
import time
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
    return '?' + '&'.join(f'{k}={UP.quote_plus(dictionary[k])}' for k in dictionary)

if __name__ == "__main__":

    ts = int(time.time())

    hash_string = hashlib.md5( f'{ts}{PRIVATE_KEY}{PUBLIC_KEY}'.encode('UTF-8')).hexdigest()

    query_items = {
        'ts': str(ts),
        'hash': hash_string,
        'apikey': PUBLIC_KEY,
        'name': '3-D Man'
    }

    query_string = convert_dict_to_querystring(query_items)

    url = f'https://gateway.marvel.com:443/v1/public/characters{query_string}'

    print(f'Requesting from {url}')

    response = requests.get(url,proxies=PROXIES)

    print(f'Response: {response.status_code}: {response.text}')
