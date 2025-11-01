import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def event_button_listen(frame, action='invite'):
    """
    функция по типу отслеживаемого ивента (action)
    подбирает подходящий шаблон и ищет его на кадре (frame)
    Если шаблон найден, и он находится по Y около половины высоты кадра,
    тогда выводим, что можно жать на кнопку
    """
    # И кадр, и шаблон - в градацию серого
    img = cv.imread(frame, cv.IMREAD_GRAYSCALE)
    img2 = img.copy()
    template = cv.imread(f'{action}_template.png', cv.IMREAD_GRAYSCALE)
    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = template.shape[::-1]

    # Методы поиска
    methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
                'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']


    for meth in methods:
        img = img2.copy()
        im_h = img.shape[::-1][1]
        center = im_h // 2
        percent = round(im_h * 0.2)
        method = getattr(cv, meth)

        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        #Определяем положение 
        if all((center+percent) > tup[-1] > (center-percent) for tup in [bottom_right, top_left]):
            return 'Подтверждаю, можно нажимать'


