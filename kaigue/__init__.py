"""
    Kaigue - A Virtual Assistant for Windows
    For now, it only works on Windows and supports Spanish.

    NOTE
    This project a personal project, so it's not intended to be used by anyone else.
    If you want to use it, you can do it, but I won't provide support for it for now.
"""

__title__ = 'kaigue'
__author__ = 'Manuel Cabral'
__version__ = '0.0.1'
__license__ = 'GPLv3'
__description__ = 'A Virtual Assistant for Windows'

from kaigue.__main__ import Kaigue
from kaigue.weather import Weather
from kaigue.web import Web

__all__ = ['Kaigue', 'Weather', 'Web']