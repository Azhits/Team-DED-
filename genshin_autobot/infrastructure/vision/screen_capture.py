"""Screen capture module.

Модуль для захвата экрана.
"""

import numpy as np
from typing import Optional, Tuple

try:
    import mss
except ImportError:
    mss = None

try:
    from PIL import Image
except ImportError:
    Image = None


class ScreenCapture:
    """Screen capture utility using MSS library.
    
    Класс для захвата экрана с использованием MSS.
    """

    def __init__(self) -> None:
        """Initialize screen capture.
        
        Raises:
            ImportError: If mss library is not installed.
        """
        if mss is None:
            raise ImportError(
                "mss library required. Install: pip install mss"
            )
        self._sct = mss.mss()

    def capture_screen(
        self,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> np.ndarray:
        """Capture screen or screen region.

        Args:
            region: Optional region (left, top, width, height).
                   If None, captures entire primary monitor.

        Returns:
            Captured image as numpy array (BGR format).

        Raises:
            ValueError: If region parameters are invalid.
        """
        if region is not None:
            if not self._validate_region(region):
                raise ValueError(
                    f"Invalid region: {region}. "
                    "Expected (left, top, width, height)."
                )
            monitor = {
                "left": region[0],
                "top": region[1],
                "width": region[2],
                "height": region[3]
            }
        else:
            monitor = self._sct.monitors[1]

        screenshot = self._sct.grab(monitor)
        img = np.array(screenshot)
        
        # Convert BGRA to BGR
        return img[:, :, :3]

    def _validate_region(
        self,
        region: Tuple[int, int, int, int]
    ) -> bool:
        """Validate region parameters.

        Args:
            region: Region tuple to validate.

        Returns:
            True if valid, False otherwise.
        """
        if len(region) != 4:
            return False
        return all(isinstance(x, int) and x > 0 for x in region[2:])

    def __del__(self) -> None:
        """Clean up resources."""
        if hasattr(self, '_sct'):
            self._sct.close()
