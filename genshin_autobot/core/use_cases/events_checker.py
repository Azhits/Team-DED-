"""Events Checker Use Case Module.

Модуль сценария проверки событий.

This module provides use cases for detecting game events such as
dungeon invites, activation prompts, and squad completion.

Этот модуль предоставляет сценарии для обнаружения игровых событий,
таких как приглашения в подземелье, запросы активации и завершение отряда.
"""

from typing import Dict, Optional, Tuple
from enum import Enum

import cv2 as cv
import numpy as np


class EventType(Enum):
    """Game event types.
    
    Типы игровых событий.
    """
    DUNGEON_INVITE = "invite"
    DUNGEON_ACTIVATE = "activate"
    SQUAD_COMPLETE = "squad_complete"


class EventsChecker:
    """Use case for checking game events from screen.
    
    Сценарий для проверки игровых событий по экрану.
    
    This class processes game events visible on screen such as
    dungeon entrance, trial start, etc. and sets event flags.
    
    Attributes:
        _frame: Current game frame.
        _text_coords: OCR text coordinates dictionary.
    """

    def __init__(
        self,
        frame: cv.typing.MatLike,
        text_coords_dict: Optional[Dict[str, list]] = None
    ) -> None:
        """Initialize events checker.
        
        Args:
            frame: Game screenshot frame.
            text_coords_dict: Dictionary mapping text to bounding box
                coordinates. Key: text string, Value: list of corner
                coordinates.
                
        Raises:
            ValueError: If frame is invalid.
        """
        if frame is None or frame.size == 0:
            raise ValueError("Invalid frame provided")
        
        self._frame: cv.typing.MatLike = frame
        self._text_coords: Dict[str, list] = text_coords_dict or {}

    def check_events(self) -> list:
        """Проверить наличие игровых событий.

        Check for game events.

        Проверяет экран на наличие игровых событий таких как
        приглашения в подземелье, активация и завершение отряда.

        This method checks the screen for game events such as
        dungeon invitations, activation prompts, and squad completion.

        Returns:
            List of detected events.
            Список обнаруженных событий.
        """
        events = []

        # Check for dungeon invitation
        if self.check_dungeon_invite():
            events.append(EventType.DUNGEON_INVITE)

        # Check for dungeon activation
        if self.check_dungeon_activation():
            events.append(EventType.DUNGEON_ACTIVATE)

        # Check for squad completion
        if self.get_squad_completion_coordinates():
            events.append(EventType.SQUAD_COMPLETE)

        return events

    def check_dungeon_invite(self) -> bool:
        """Check if dungeon invitation is present.
        
        Проверяет наличие приглашения в подземелье.
        
        Returns:
            True if dungeon invite button is detected.
        """
        return self._check_event_button(EventType.DUNGEON_INVITE)

    def check_dungeon_activation(self) -> bool:
        """Check if dungeon activation prompt is present.
        
        Проверяет наличие запроса активации подземелья.
        
        Returns:
            True if activation button is detected.
        """
        return self._check_event_button(EventType.DUNGEON_ACTIVATE)

    def get_squad_completion_coords(self) -> Optional[Tuple[int, ...]]:
        """Get coordinates of squad completion confirmation.
        
        Получает координаты подтверждения завершения отряда.
        
        Searches through OCR text to find squad completion message
        and returns its bounding box coordinates.
        
        Returns:
            Tuple of coordinates (x1, y1, x2, y2) or None if not found.
        """
        for text, coords in self._text_coords.items():
            if self._is_squad_complete_text(text):
                return tuple(coords)
        return None

    def _check_event_button(
        self,
        event_type: EventType
    ) -> bool:
        """Check for clickable event button using template matching.
        
        Args:
            event_type: Type of event to check.
            
        Returns:
            True if event button template is found.
            
        Note:
            Requires template images in resources directory.
            Placeholder implementation - needs template matcher.
        """
        # TODO: Implement template matching with ImageMatcher
        # from infrastructure layer
        return False

    def _is_squad_complete_text(self, text: str) -> bool:
        """Check if text indicates squad completion.
        
        Args:
            text: OCR text to check.
            
        Returns:
            True if text matches squad completion pattern.
        """
        keywords = [
            "squad",
            "отряд",
            "complete",
            "завершен",
            "ready",
            "готов"
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
