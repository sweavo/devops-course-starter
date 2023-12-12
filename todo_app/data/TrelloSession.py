"""
    TrelloSession.py


"""
import urllib.parse as UP
import requests

# Handle Corporate IT wonk. TODO once I'm back in the office
PROXIES = {}
REQUESTS_VERIFY = True


class HTTP401Exception(RuntimeError):
    pass

class TrelloSession(object):
    """Class to handle the dialect of REST used by trello.

    In particular, it encapsulates how to pass authentication information to
    the server, and returns response body JSON.
    """

    def __init__(self, root_url, api_key, token):
        self._root_url = root_url
        self._api_key = api_key
        self._token = token

    def request_url(self, path, query_dict=None):
        """Trello's authentication goes in the querystring, so this function
        generates URLs with the authentication present.
        """
        if query_dict is None:
            query_dict = {}

        query_items = {"key": self._api_key, "token": self._token}

        # merge in the passed query_dict
        for k in query_dict:
            query_items[k] = query_dict[k]

        query_string = UP.urlencode(query_items, doseq=True)

        return f"{self._root_url}{path}?{query_string}"

    def retrieve_json(self, path_or_url):
        """REST API helper for calls returning volatile results (i.e. can
        change behind our back).
        """
        if not path_or_url.startswith("http"):
            path_or_url = self.request_url(path_or_url)

        response = requests.get(
            path_or_url,
            proxies=PROXIES,
            verify=REQUESTS_VERIFY,  # Lel, because of our security policies
        )

        if response.status_code != 200:
            # note: bail out before writing the cache :)
            if response.status_code == 401:
                raise HTTP401Exception
            else:
                raise RuntimeError(f"Server response code {response.status_code}")

        data = response.json()

        return data
