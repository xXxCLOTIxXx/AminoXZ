"""
Author: Xsarz

Enjoy using!
"""


from os import system as s
from .client import Client
from .localClient import LocalClient
from .lib.util import generator, exceptions, headers
from colored import fore
from json import loads
from requests import get
from .socket import SocketHandler, Callbacks
__title__ = 'AminoXZ'
__author__ = 'Xsarz'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-2023 Xsarz'
__version__ = '1.1.8'

def init():
	__newest__ = loads(get("https://pypi.org/pypi/aminoxz/json").text)["info"]["version"]
	if __version__ != __newest__:
		s('cls || clear')
		print(fore.ORANGE_1, f'{__title__} made by {__author__}\nPlease update the library. Your version: {__version__}  A new version:{__newest__}', fore.WHITE)
init()