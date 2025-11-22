"""Genshin Impact Autobot package.

Пакет для автоматизации игры Genshin Impact.
"""

__version__ = '0.1.0'
__author__ = 'Team-DED'

from . import core
from . import infrastructure

__all__ = [
    'core',
    'infrastructure',
    '__version__',
]
