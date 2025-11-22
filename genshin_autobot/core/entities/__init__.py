"""Core entities package.

Этот пакет содержит классы бизнес-логики и сущностей.
"""

from .base import Entity
from .character import CharacterHealth, CharacterStateChecker

__all__ = ['Entity', 'CharacterHealth', 'CharacterStateChecker']
