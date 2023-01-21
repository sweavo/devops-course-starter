import urllib.parse as UP
import requests

PROXIES={}
REQUESTS_VERIFY=True

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


class TrelloSession(object):
    def __init__(self, root_url, api_key, token):
        self._root_url = root_url
        self._api_key = api_key
        self._token = token

    def request_url(self, path, query_dict=None):
        """ Encapsulate the wonk for the Marvel API authentication.
        query_dict contains the arguments for the query, which are merged
        into the needed auth query items. """

        if query_dict is None:
            query_dict={}

        query_items = {
            'key': self._api_key,
            'token': self._token
        }

        # merge in the passed query_dict
        for k in query_dict:
            query_items[k] = query_dict[k]

        query_string = convert_dict_to_querystring(query_items)

        return f'{self._root_url}{path}{query_string}'

    def retrieve_json(self, path_or_url):
        """ REST API helper for calls returning volatile results (i.e. can change behind our back).
        """
        if not path_or_url.startswith('http'):
            path_or_url = self.request_url(path_or_url)
        
        print(f'Requesting from: {path_or_url}')
        response = requests.get(path_or_url,
                                proxies=PROXIES,
                                verify=REQUESTS_VERIFY # Lel, because of our security policies
                                )

        if response.status_code != 200:
            # note: bail out before writing the cache :)
            raise RuntimeError(f"Server response code {response.status_code}")

        data = response.json()

        return data
