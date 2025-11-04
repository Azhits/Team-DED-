import cv2 as cv
import numpy as numpy
import pyautogui as pgui

import os
import json


def check_clicable_event_button(frame: cv.typing.MatLike, event_type: str):
    """
    функция по типу отслеживаемого ивента (action)
    подбирает подходящий шаблон и ищет его на кадре (frame)
    Если шаблон найден, и он находится по Y около половины высоты кадра,
    тогда выводим, что можно жать на кнопку
    """
    # И кадр, и шаблон - в градацию серого
    flag = False
    center = im_h // 2
    percent = round(im_h * 0.2)
    img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    template = cv.imread(f'../static/{event_type}_template.png', cv.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    # Методы поиска
    methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED',
                'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']

    # Используя все методы поиска, ищем шаблон на кадре
    for meth in methods:
        img = img2.copy()
        im_h = img.shape[::-1][1]
        method = getattr(cv, meth)

        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
    # Смотрим на положение шаблона в кадре. Если удовлетворяет условию, то вернет True
    if all((center+percent) > tup[-1] > (center-percent) for tup in [bottom_right, top_left]):
        flag = True
    return flag
