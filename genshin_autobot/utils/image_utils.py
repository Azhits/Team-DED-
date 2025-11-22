"""Модуль утилит для работы с изображениями.
Image utilities module.

Этот модуль содержит функции для обработки изображений,
таких как обрезка кадров.
This module contains functions for image processing,
such as frame cropping.
"""

import cv2 as cv
import numpy as np
from typing import Union


def frame_cropper(
    frame: cv.typing.MatLike,
    crop_percent: float,
    to_x1: Union[int, float],
    to_x2: Union[int, float],
    to_y1: Union[int, float],
    to_y2: Union[int, float]
) -> cv.typing.MatLike:
    """Обрезать изображение по заданным параметрам.
    
    Crop image by specified parameters.
    
    This function crops a frame based on percentage and offset
    parameters to extract a region of interest.
    
    Args:
        frame: Input image/frame to crop
        crop_percent: Percentage of frame to use as crop window
                     (0.0 to 1.0)
        to_x1: X offset divisor for left edge
        to_x2: X offset divisor for right edge  
        to_y1: Y offset divisor for top edge
        to_y2: Y offset divisor for bottom edge
    
    Returns:
        Cropped image region
        
    Raises:
        ValueError: If frame is empty or parameters are invalid
        TypeError: If frame is not valid image type
    
    Example:
        >>> frame = cv.imread('image.png')
        >>> cropped = frame_cropper(frame, 0.5, 2, 2, 2, 2)
    """
    if frame is None or frame.size == 0:
        raise ValueError("Frame cannot be empty")
    
    if not isinstance(frame, np.ndarray):
        raise TypeError("Frame must be numpy array")
    
    if not (0.0 <= crop_percent <= 1.0):
        raise ValueError(
            "crop_percent must be between 0.0 and 1.0"
        )
    
    if any(val <= 0 for val in [to_x1, to_x2, to_y1, to_y2]):
        raise ValueError(
            "Offset parameters must be positive"
        )
    
    # Get frame dimensions
    height, width = frame.shape[:2]
    bottom_y = height
    
    # Calculate crop window dimensions
    window_width = round(width * crop_percent)
    window_height = round(height * crop_percent)
    center_x = width // 2
    
    # Calculate crop coordinates
    x1 = center_x - window_width // to_x1
    y1 = bottom_y - int(window_height * to_y1)
    x2 = center_x + window_width // to_x2
    y2 = bottom_y - int(window_height * to_y2)
    
    # Ensure coordinates are within bounds
    x1 = max(0, int(x1))
    y1 = max(0, int(y1))
    x2 = min(width, int(x2))
    y2 = min(height, int(y2))
    
    # Crop and return
    cropped_img = frame[y1:y2, x1:x2]
    
    if cropped_img.size == 0:
        raise ValueError(
            "Crop parameters resulted in empty region"
        )
    
    return cropped_img
