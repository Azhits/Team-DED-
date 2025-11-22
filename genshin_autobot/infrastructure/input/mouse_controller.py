"""Контроллер управления мышью.

Этот модуль содержит класс для управления мышью с использованием pyautogui.
"""

from typing import Tuple
import pyautogui as pgui


class MouseController:
    """Контроллер для управления мышью.
    
    Attributes:
        _screen_width: Ширина экрана в пикселях.
        _screen_height: Высота экрана в пикселях.
    """
    
    def __init__(self) -> None:
        """Инициализация контроллера мыши."""
        self._screen_width, self._screen_height = pgui.size()
    
    def move_cursor_to_coords(
        self,
        coords: Tuple[int, int],
        duration: float = 0.1
    ) -> None:
        """Перемещает курсор в указанные координаты.
        
        Args:
            coords: Кортеж (x, y) с координатами экрана.
            duration: Длительность перемещения в секундах.
            
        Raises:
            ValueError: Если координаты выходят за пределы экрана.
        """
        x, y = coords
        
        if not self._is_valid_coords(x, y):
            raise ValueError(
                f"Координаты ({x}, {y}) выходят за пределы экрана "
                f"({self._screen_width}x{self._screen_height})"
            )
        
        pgui.moveTo(x=x, y=y, duration=duration)
    
    def click(self, coords: Tuple[int, int]) -> None:
        """Выполняет клик мышью в указанных координатах.
        
        Args:
            coords: Кортеж (x, y) с координатами для клика.
            
        Raises:
            ValueError: Если координаты невалидны.
        """
        self.move_cursor_to_coords(coords, duration=0.1)
        pgui.click()
    
    def _is_valid_coords(self, x: int, y: int) -> bool:
        """Проверяет валидность координат.
        
        Args:
            x: Координата X.
            y: Координата Y.
            
        Returns:
            True если координаты в пределах экрана, False иначе.
        """
        return 0 <= x <= self._screen_width and 0 <= y <= self._screen_height
