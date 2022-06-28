from os import system as s
from .client import Client
from .lib.util import generator, helpers, exceptions
from colored import fore
__title__ = 'AminoXZ'
__author__ = 'Xsarz'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022 Xsarz'
__version__ = '1.1'
__status__ = '(BETA)'

def init():
	__newest__ = '1.1'
	s('cls')
	if __version__ != __newest__:
		return print(fore.ORANGE_1, f'{__title__} made by {__author__}\nPlease update the library. Your version: {__version__}  A new version:{__newest__}', fore.WHITE)
	else:
		return print(fore.BLUE, f'{__title__} {__version__} {__status__} made by {__author__}\n', fore.WHITE)

init()