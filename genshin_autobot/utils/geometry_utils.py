"""Модуль геометрических утилит.
Geometry utilities module.

Этот модуль содержит функции для геометрических вычислений,
таких как расчет центра ограничивающего прямоугольника.
This module contains functions for geometric calculations,
such as bounding box center calculation.
"""

import numpy as np
from typing import List, Tuple


def get_center_coords(
    corners: List[List[int]]
) -> Tuple[int, int]:
    """Вычислить координаты центра ограничивающего прямоугольника.
    
    Calculate bounding box center coordinates.
    
    Args:
        corners: List of corner coordinates [[x1, y1], [x2, y2], ...]
                Each corner is a list of two integers [x, y]
    
    Returns:
        Tuple of center coordinates (center_x, center_y)
        
    Raises:
        ValueError: If corners list has invalid length or structure
        TypeError: If corner values are not numeric
    
    Example:
        >>> corners = [[100, 100], [200, 100], [200, 200]]
        >>> get_center_coords(corners)
        (150, 150)
    """
    if not corners or len(corners) < 3:
        raise ValueError(
            "corners must contain at least 3 coordinate pairs"
        )
    
    for corner in corners:
        if not isinstance(corner, (list, tuple)) or len(corner) != 2:
            raise ValueError(
                "Each corner must be a list/tuple of 2 values"
            )
        if not all(isinstance(c, (int, float, np.integer)) 
                   for c in corner):
            raise TypeError(
                "Corner coordinates must be numeric"
            )
    
    # Calculate width and height from corners
    lnx = round(
        np.sqrt(
            abs(
                (corners[1][0] - corners[0][0])**2 - 
                (corners[1][1] - corners[0][1])**2
            )
        )
    ) // 2
    
    lny = round(
        np.sqrt(
            abs(
                (corners[2][0] - corners[1][0])**2 - 
                (corners[2][1] - corners[1][1])**2
            )
        )
    ) // 2
    
    # Calculate center coordinates
    center_coords = (
        corners[0][0] + lnx,
        corners[0][1] + lny
    )
    
    return center_coords
