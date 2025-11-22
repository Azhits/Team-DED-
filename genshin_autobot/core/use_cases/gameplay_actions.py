"""Модуль игровых действий.
Gameplay actions module.

Этот модуль содержит классы для управления игровыми действиями:
управление камерой, атаки, перемещение и другие.
This module contains classes for managing gameplay actions:
camera control, attacks, movement, and others.
"""

import time
from typing import Optional, Tuple

from genshin_autobot.infrastructure.input.mouse_controller import (
    MouseController
)
from genshin_autobot.infrastructure.input.keyboard_controller import (
    KeyboardController
)


class CameraMover:
    """Управление движением камеры.
    
    Camera movement controller.
    Manages camera position by moving cursor.
    """
    
    def __init__(
        self,
        mouse_controller: Optional[MouseController] = None
    ) -> None:
        """Инициализация контроллера камеры.
        
        Initialize camera controller.
        
        Args:
            mouse_controller: Mouse controller instance
        """
        self._mouse = mouse_controller or MouseController()
    
    def move_camera(self, coords: Tuple[int, int]) -> None:
        """Переместить камеру.
        
        Move camera to specified coordinates.
        
        Args:
            coords: Target (x, y) coordinates
            
        Raises:
            ValueError: If coordinates are invalid
        """
        if not coords or len(coords) != 2:
            raise ValueError("Coords must be tuple of 2 integers")
        
        self._mouse.move_cursor(coords)


class PhysicalAttack:
    """Физическая атака.
    
    Physical attack controller.
    Manages physical combat actions.
    """
    
    def __init__(
        self,
        mouse_controller: Optional[MouseController] = None
    ) -> None:
        """Инициализация контроллера атак.
        
        Initialize attack controller.
        
        Args:
            mouse_controller: Mouse controller instance
        """
        self._mouse = mouse_controller or MouseController()
    
    def attack_combination(self, kick_count: int) -> None:
        """Выполнить комбинацию ударов.
        
        Execute attack combination.
        
        Args:
            kick_count: Number of attacks to perform
            
        Raises:
            ValueError: If kick_count is not positive
        """
        if kick_count <= 0:
            raise ValueError("kick_count must be positive")
        
        for _ in range(kick_count):
            time.sleep(0.001)
            self._mouse.click()


class Runner:
    """Контроллер бега.
    
    Running controller.
    Manages character running actions.
    """
    
    def __init__(
        self,
        keyboard_controller: Optional[KeyboardController] = None
    ) -> None:
        """Инициализация контроллера бега.
        
        Initialize running controller.
        
        Args:
            keyboard_controller: Keyboard controller instance
        """
        self._keyboard = keyboard_controller or KeyboardController()
    
    def start_run(self, key: str = 'shift') -> None:
        """Начать бег.
        
        Start running.
        
        Args:
            key: Key to press for running
            
        Raises:
            ValueError: If key is empty
        """
        if not key:
            raise ValueError("Key cannot be empty")
        
        self._keyboard.press_key(key)
    
    def stop_run(self, key: str = 'shift') -> None:
        """Остановить бег.
        
        Stop running.
        
        Args:
            key: Key to release
            
        Raises:
            ValueError: If key is empty
        """
        if not key:
            raise ValueError("Key cannot be empty")
        
        self._keyboard.release_key(key)


class ElementalAttack:
    """Элементальные атаки.
    
    Elemental attacks controller.
    Manages elemental skills and bursts.
    """
    
    def __init__(
        self,
        keyboard_controller: Optional[KeyboardController] = None
    ) -> None:
        """Инициализация контроллера элементальных атак.
        
        Initialize elemental attack controller.
        
        Args:
            keyboard_controller: Keyboard controller instance
        """
        self._keyboard = keyboard_controller or KeyboardController()
    
    def elemental_attack(self, key: str = 'e') -> None:
        """Элементальный навык.
        
        Execute elemental skill.
        
        Args:
            key: Key for elemental skill
            
        Raises:
            ValueError: If key is empty
        """
        if not key:
            raise ValueError("Key cannot be empty")
        
        self._keyboard.press_key(key)
    
    def ultimate_attack(self, key: str = 'q') -> None:
        """Элементальный взрыв.
        
        Execute elemental burst.
        
        Args:
            key: Key for elemental burst
            
        Raises:
            ValueError: If key is empty
        """
        if not key:
            raise ValueError("Key cannot be empty")
        
        self._keyboard.press_key(key)


class MoveController:
    """Контроллер перемещения.
    
    Movement controller.
    Manages character movement actions.
    """
    
    def __init__(
        self,
        keyboard_controller: Optional[KeyboardController] = None,
        key_to_press: str = 'w'
    ) -> None:
        """Инициализация контроллера перемещения.
        
        Initialize movement controller.
        
        Args:
            keyboard_controller: Keyboard controller instance
            key_to_press: Default movement key
            
        Raises:
            ValueError: If key_to_press is empty
        """
        if not key_to_press:
            raise ValueError("key_to_press cannot be empty")
        
        self._keyboard = keyboard_controller or KeyboardController()
        self._key = key_to_press
    
    def short_move(self) -> None:
        """Короткое перемещение.
        
        Perform short movement.
        """
        self._keyboard.press_key(self._key)
    
    def long_move(self, flag: bool) -> None:
        """Длинное перемещение.
        
        Perform long movement (hold key).
        
        Args:
            flag: True to start holding, False to release
        """
        if flag:
            self._keyboard.hold_key(self._key)
        else:
            self._keyboard.release_key(self._key)
