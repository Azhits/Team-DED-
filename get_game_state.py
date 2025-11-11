from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import pyautogui
from detection_enemy import detect_enemies

def detect_game_state(screenshot):
    """
    Простая эвристическая система определения состояния игры
    Будет улучшаться со временем
    """
    if isinstance(screenshot, Image.Image):
        img_np = np.array(screenshot)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    else:
        img_cv = screenshot

    # Простые проверки по цвету (замените координаты на реальные)
    h, w = img_cv.shape[:2]

    # Проверяем наличие врагов (используем вашу модель)
    enemies = detect_enemies(screenshot, confidence_threshold=0.3)

    if enemies:
        return "battle", enemies

    # Проверяем другие состояния по характерным точкам
    # Пример: проверяем есть ли иконка карты в углу (замените координаты)
    map_region = img_cv[50:100, 50:100]  # Примерные координаты иконки карты
    map_color = np.mean(map_region)

    if map_color > 100:  # Настроить под вашу игру
        return "map", []

    # Добавьте другие проверки по мере необходимости
    # character_select, reward_tree, idle и т.д.

    return "exploring", []