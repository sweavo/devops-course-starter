""" Module to get the environment's proxy settings and format them for requests 
"""
import os


def derive_proxy_settings(environ):
    """read the environment for proxy variables and generate key-value pairs for a
        dict for requests module to use. This is a function so that I can avoid
        mutating PROXIES, which should be treated as a constant, in global scope.

    >>> dict(derive_proxy_settings({'http_proxy': 'hello, mum'}))
    {'http': 'hello, mum'}

    """
    if "http_proxy" in environ:
        yield "http", environ["http_proxy"]
    if "https_proxy" in environ:
        yield "https", environ["https_proxy"]


def from_env():
    return dict(derive_proxy_settings(os.environ))
