"""Character State Entity Module.

Модуль сущности состояния персонажа.

This module provides entities and services for checking character state
in Genshin Impact, including health, energy, and ability cooldowns.

Этот модуль предоставляет сущности и сервисы для проверки состояния
персонажа в Genshin Impact, включая здоровье, энергию и перезарядку способностей.
"""

from typing import Tuple, Optional
from dataclasses import dataclass

import cv2 as cv
import numpy as np
import easyocr


@dataclass
class CharacterHealth:
    """Character health state.
    
    Состояние здоровья персонажа.
    
    Attributes:
        current: Current health points.
        maximum: Maximum health points.
    """
    current: int
    maximum: int
    
    @property
    def percentage(self) -> float:
        """Get health as percentage (0.0 to 1.0).
        
        Returns:
            Health percentage.
        """
        if self.maximum <= 0:
            return 0.0
        return self.current / self.maximum
    
    @property
    def is_critical(self) -> bool:
        """Check if health is critically low (<30%).
        
        Returns:
            True if health is critical.
        """
        return self.percentage < 0.3


class CharacterStateChecker:
    """Service for checking character state from game frame.
    
    Сервис для проверки состояния персонажа по кадру игры.
    
    This class analyzes game screenshots to extract character state
    information using OCR and computer vision techniques.
    
    Attributes:
        _ocr_reader: EasyOCR reader for text extraction.
    """

    def __init__(self, ocr_reader: easyocr.Reader) -> None:
        """Initialize character state checker.
        
        Args:
            ocr_reader: Configured EasyOCR reader instance.
            
        Raises:
            ValueError: If ocr_reader is None.
        """
        if ocr_reader is None:
            raise ValueError("OCR reader cannot be None")
        self._ocr_reader: easyocr.Reader = ocr_reader

    def _crop_health_bar_region(
        self,
        frame: cv.typing.MatLike
    ) -> cv.typing.MatLike:
        """Crop health bar region from game frame.
        
        Args:
            frame: Game screenshot frame.
            
        Returns:
            Cropped image containing health bar area.
            
        Raises:
            ValueError: If frame is invalid.
        """
        if frame is None or frame.size == 0:
            raise ValueError("Invalid frame provided")
        
        height, width = frame.shape[:2]
        
        # Health bar is typically in top-left area
        # Crop: left 30%, top 10-20%
        x1 = int(width * 0.05)
        x2 = int(width * 0.35)
        y1 = int(height * 0.05)
        y2 = int(height * 0.15)
        
        cropped = frame[y1:y2, x1:x2]
        return cropped

    def check_health(
        self,
        frame: cv.typing.MatLike
    ) -> Optional[CharacterHealth]:
        """Check character health from game frame.
        
        Args:
            frame: Game screenshot frame.
            
        Returns:
            CharacterHealth object or None if detection failed.
            
        Raises:
            ValueError: If frame is invalid.
        """
        cropped = self._crop_health_bar_region(frame)
        gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
        
        try:
            # Read text from health bar region
            results = self._ocr_reader.readtext(gray)
            
            if not results:
                return None
            
            # Parse health text (format: "current/maximum")
            text = results[0][1]
            if '/' not in text:
                return None
            
            parts = text.split('/')
            current = int(parts[0].strip())
            maximum = int(parts[1].strip())
            
            return CharacterHealth(current=current, maximum=maximum)
            
        except (IndexError, ValueError, AttributeError):
            return None

    def check_elemental_skill_ready(self) -> bool:
        """Check if elemental skill (E) is ready.
        
        Returns:
            True if skill is ready, False otherwise.
            
        Note:
            Placeholder implementation - requires visual detection.
        """
        # TODO: Implement skill cooldown detection
        return True

    def check_elemental_burst_ready(self) -> bool:
        """Check if elemental burst (Q) is ready.
        
        Returns:
            True if burst is ready, False otherwise.
            
        Note:
            Placeholder implementation - requires visual detection.
        """
        # TODO: Implement burst energy detection
        return True
