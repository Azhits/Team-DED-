"""Input controllers package.

Этот пакет содержит контроллеры для управления устройствами ввода.
"""

from .keyboard_controller import KeyboardController
from .mouse_controller import MouseController

__all__ = [
    'KeyboardController',
    'MouseController',
]
