"""Image matching and computer vision operations.

Операции сопоставления изображений и компьютерного зрения.

Этот модуль содержит функционал для поиска и сопоставления
изображений с использованием OpenCV.

This module contains functionality for finding and matching
images using OpenCV.
"""

from typing import Optional, Tuple, List
import numpy as np
import cv2


class ImageMatcher:
    """
    Image matching using template matching and OpenCV.
    
    Сопоставление изображений с помощью template matching и OpenCV.
    
    This class provides methods for template matching,
    object detection, and element location on screen.
    
    Attributes:
        _threshold: Minimum confidence threshold for matches.
    """
    
    def __init__(
        self,
        threshold: float = 0.8
    ) -> None:
        """
        Initialize the image matcher.
        
        Инициализирует сопоставитель изображений.
        
        Args:
            threshold: Minimum confidence for match (0.0-1.0).
        
        Raises:
            ValueError: If threshold is not in valid range.
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(
                f"Threshold must be between 0.0 and 1.0, "
                f"got {threshold}"
            )
        
        self._threshold = threshold
    
    def match_template(
        self,
        image: np.ndarray,
        template: np.ndarray,
        threshold: Optional[float] = None
    ) -> Optional[Tuple[int, int, float]]:
        """
        Find template in image using template matching.
        
        Находит шаблон в изображении.
        
        Args:
            image: Source image to search in.
            template: Template image to find.
            threshold: Optional custom threshold.
        
        Returns:
            Tuple of (x, y, confidence) if found, None otherwise.
        
        Raises:
            ValueError: If image or template is invalid.
        """
        if image is None or image.size == 0:
            raise ValueError("Image cannot be empty")
        
        if template is None or template.size == 0:
            raise ValueError("Template cannot be empty")
        
        threshold = (
            threshold if threshold is not None
            else self._threshold
        )
        
        result = cv2.matchTemplate(
            image,
            template,
            cv2.TM_CCOEFF_NORMED
        )
        min_val, max_val, min_loc, max_loc = (
            cv2.minMaxLoc(result)
        )
        
        if max_val >= threshold:
            x, y = max_loc
            return (x, y, max_val)
        
        return None
    
    def detect_objects(
        self,
        image: np.ndarray,
        template: np.ndarray,
        threshold: Optional[float] = None
    ) -> List[Tuple[int, int, int, int, float]]:
        """
        Detect all occurrences of template in image.
        
        Обнаруживает все вхождения шаблона в изображении.
        
        Args:
            image: Source image to search in.
            template: Template image to find.
            threshold: Optional custom threshold.
        
        Returns:
            List of (x, y, width, height, confidence) tuples.
        
        Raises:
            ValueError: If image or template is invalid.
        """
        if image is None or image.size == 0:
            raise ValueError("Image cannot be empty")
        
        if template is None or template.size == 0:
            raise ValueError("Template cannot be empty")
        
        threshold = (
            threshold if threshold is not None
            else self._threshold
        )
        
        result = cv2.matchTemplate(
            image,
            template,
            cv2.TM_CCOEFF_NORMED
        )
        
        locations = np.where(result >= threshold)
        matches = []
        
        h, w = template.shape[:2]
        
        for pt in zip(*locations[::-1]):
            x, y = pt
            confidence = result[y, x]
            matches.append((x, y, w, h, float(confidence)))
        
        return matches
    
    def locate_element(
        self,
        image: np.ndarray,
        template: np.ndarray
    ) -> Optional[Tuple[int, int]]:
        """
        Locate center position of template in image.
        
        Определяет центральную позицию шаблона в изображении.
        
        Args:
            image: Source image to search in.
            template: Template image to find.
        
        Returns:
            Tuple of (center_x, center_y) if found, None otherwise.
        
        Raises:
            ValueError: If image or template is invalid.
        """
        match = self.match_template(image, template)
        
        if match is None:
            return None
        
        x, y, confidence = match
        h, w = template.shape[:2]
        
        center_x = x + w // 2
        center_y = y + h // 2
        
        return (center_x, center_y)
