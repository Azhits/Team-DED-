"""Frame Text Coordinator Module.

Модуль координатора текста на кадре.

This module provides OCR text extraction from game frames with
coordinate mapping for detected text regions.

Этот модуль обеспечивает OCR-извлечение текста из игровых кадров
с картографированием координат обнаруженных текстовых областей.
"""

from typing import Dict, List, Tuple

import cv2 as cv
import numpy as np
import easyocr


class FrameTextCoordinator:
    """Coordinate text extraction from game frames.
    
    Координатор извлечения текста из игровых кадров.
    
    This class performs OCR text processing from frames and
    calculates coordinates of detected text regions.
    
    Attributes:
        _frame: Game screenshot frame.
        _reader: EasyOCR reader instance.
        _confidence_threshold: Minimum confidence for text detection.
    """

    DEFAULT_CONFIDENCE = 0.7

    def __init__(
        self,
        frame: cv.typing.MatLike,
        language: str = 'ru',
        use_gpu: bool = False,
        confidence_threshold: float = DEFAULT_CONFIDENCE
    ) -> None:
        """Initialize frame text coordinator.
        
        Args:
            frame: Game screenshot frame.
            language: OCR language code (default: 'ru').
            use_gpu: Whether to use GPU acceleration.
            confidence_threshold: Minimum confidence (0.0-1.0).
            
        Raises:
            ValueError: If frame is invalid or confidence out of range.
        """
        if frame is None or frame.size == 0:
            raise ValueError("Invalid frame provided")
        
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError(
                f"Confidence must be 0.0-1.0, got {confidence_threshold}"
            )
        
        self._frame: cv.typing.MatLike = frame
        self._confidence_threshold: float = confidence_threshold
        self._reader: easyocr.Reader = easyocr.Reader(
            [language],
            gpu=use_gpu
        )

    def get_text_and_coords(self) -> Dict[str, List[Tuple[int, int]]]:
        """Extract text with coordinates from frame.
        
        Извлекает текст с координатами из кадра.
        
        Processes the frame through OCR and returns a dictionary
        mapping detected text to bounding box coordinates.
        
        Returns:
            Dictionary with text as key and coordinate list as value.
            Coordinates are (x, y) tuples for bbox corners.
        """
        prepared = self._prepare_frame()
        ocr_results = self._read_text_from_frame(prepared)
        return self._build_text_coords_dict(ocr_results)

    def _prepare_frame(self) -> cv.typing.MatLike:
        """Prepare frame for OCR processing.
        
        Converts frame to grayscale for better OCR performance.
        
        Returns:
            Grayscale version of the frame.
        """
        return cv.cvtColor(self._frame, cv.COLOR_BGR2GRAY)

    def _read_text_from_frame(
        self,
        prepared_frame: cv.typing.MatLike
    ) -> List[Tuple]:
        """Read text from prepared frame using OCR.
        
        Args:
            prepared_frame: Preprocessed grayscale frame.
            
        Returns:
            List of (bbox, text, probability) tuples from OCR.
        """
        return self._reader.readtext(prepared_frame)

    def _build_text_coords_dict(
        self,
        ocr_results: List[Tuple]
    ) -> Dict[str, List[Tuple[int, int]]]:
        """Build dictionary from OCR results.
        
        Filters results by confidence threshold and creates
        text-to-coordinates mapping.
        
        Args:
            ocr_results: Raw OCR output tuples.
            
        Returns:
            Dictionary mapping text to bbox coordinates.
        """
        text_coords: Dict[str, List[Tuple[int, int]]] = {}
        
        for bbox, text, confidence in ocr_results:
            if confidence >= self._confidence_threshold:
                # Convert bbox to list of (x, y) tuples
                coords = [(int(x), int(y)) for x, y in bbox]
                text_coords[text] = coords
        
        return text_coords
