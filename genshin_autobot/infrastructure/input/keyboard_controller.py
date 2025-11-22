"""Контроллер управления клавиатурой.

Этот модуль содержит класс для управления клавиатурой с использованием pyautogui.
"""

from typing import List
import pyautogui as pgui


class KeyboardController:
    """Контроллер для управления клавиатурой."""
    
    def press_key(self, key: str) -> None:
        """Нажимает указанную клавишу.
        
        Args:
            key: Название клавиши (например, 'shift', 'e', 'w').
        """
        pgui.press(key)
    
    def press_keys(self, keys: List[str]) -> None:
        """Нажимает несколько клавиш последовательно.
        
        Args:
            keys: Список клавиш для нажатия.
        """
        for key in keys:
            self.press_key(key)
    
    def down_key(self, key: str) -> None:
        """Зажимает клавишу (удерживает нажатой).
        
        Args:
            key: Название клавиши.
        """
        pgui.keyDown(key)
    
    def up_key(self, key: str) -> None:
        """Отпускает клавишу.
        
        Args:
            key: Название клавиши.
        """
        pgui.keyUp(key)
