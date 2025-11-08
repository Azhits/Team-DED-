import cv2 as cv
import numpy as numpy
import pyautogui as pgui
import easyocr

import os

def get_data_about_lifebar(frame: cv.typing.MatLike, reader: easyocr.Reader) -> tuple:
    """
    Функция смотрит только на шкалу жизни
    Из данной шкалы она берет числа - сколько всего HP, сколько осталось
    При помощи EasyOCR.
    Возвращает кортеж
    """
    height, width = frame.shape[:2]
    bottom_y = height
    window_widht = round(width * 0.1)
    window_height = round(height * 0.1)
    center_x = width // 2
    x1 = center_x - window_widht // 3
    y1 = bottom_y - int(window_height * 0.8)
    x2 = center_x + window_widht // 3
    y2 = bottom_y - int(window_height * 0.3)
    cropped_img = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    remain, full = int(reader.readtext(gray)[0][1].split('/')[0]), int(reader.readtext(gray)[0][1].split('/')[-1])
    return (full, remain)
