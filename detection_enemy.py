from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import pyautogui

# Загружаем модель для детекции врагов
enemy_model = YOLO('best.pt')


def detect_enemies(screenshot, confidence_threshold=0.5):
    if isinstance(screenshot, Image.Image):
        img_np = np.array(screenshot)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    else:
        img_cv = screenshot

    results = enemy_model(img_cv, conf=confidence_threshold, verbose=False)

    enemies = []

    if len(results) > 0 and results[0].boxes and len(results[0].boxes) > 0:
        boxes = results[0].boxes
        confidences = boxes.conf
        class_ids = boxes.cls

        for class_id, confidence, box in zip(class_ids, confidences, boxes.xyxy):
            enemy_type = int(class_id)
            enemies.append({
                'type': enemy_type,
                'type_name': ['босс', 'враг_со_статусом', 'враг_без_статуса'][enemy_type],
                'confidence': float(confidence),
                'bbox': box.cpu().numpy()
            })

    return enemies


def get_battle_strategy(enemies):
    if not enemies:
        return "no_enemies"

    enemy_types = [enemy['type'] for enemy in enemies]

    # Приоритет: босс > враг со статусом > враг без статуса
    if 0 in enemy_types:  # Есть босс
        return "focus_boss"
    elif 1 in enemy_types:  # Есть враги со статусом
        return "focus_status_enemies"
    else:  # Только обычные враги
        return "focus_normal_enemies"