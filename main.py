from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import pyautogui
from detection_enemy import detect_enemies
from detection_enemy import get_battle_strategy
from get_game_state import detect_game_state
import time
import pygetwindow as gw

def activate_game_window(window_title="Genshin Impact"):
    """
    Автоматически находит и активирует окно игры
    """
    try:
        # Ищем окно с игрой
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            game_window = windows[0]
            if game_window.isMinimized:
                game_window.restore()
            game_window.activate()
            print(f"✅ Активировано окно: {window_title}")
            return True
        else:
            print(f"❌ Окно '{window_title}' не найдено")
            return False
    except Exception as e:
        print(f"❌ Ошибка активации окна: {e}")
        return False
class CombatBot:
    def __init__(self):
        self.current_state = "unknown"
        self.last_strategy = "none"

    def handle_battle(self, enemies):
        """Обработка боевой ситуации"""
        strategy = get_battle_strategy(enemies)

        if strategy != self.last_strategy:
            print(f" Смена стратегии: {strategy}")
            self.last_strategy = strategy

        # Логика для каждой стратегии
        if strategy == "focus_boss":
            print("Фокусируюсь на боссе!")
            # Кликаем по боссу или используем AoE атаки
            pyautogui.click(button='right')  # Пример: заряженная атака

        elif strategy == "focus_status_enemies":
            print("Фокусируюсь на врагах со статусами!")
            pyautogui.press('e')  # Пример: использование элементального навыка

        elif strategy == "focus_normal_enemies":
            print(" Атакую обычных врагов!")
            pyautogui.click()  # Обычная атака

        else:
            print(" Врагов не видно, продолжаю осмотр")
            pyautogui.press('w')  # Двигаемся вперед

    def handle_map(self):
        """Обработка карты"""
        print("🗺На карте, ищу точку входа в данж")
        # Логика навигации по карте
        pyautogui.press('m')  # Закрыть карту

    def handle_exploring(self):
        """Исследование мира"""
        print(" Исследую локацию...")
        pyautogui.press('w')  # Двигаемся вперед

    def update(self, screenshot):
        """Основной цикл обновления"""
        state, data = detect_game_state(screenshot)

        if state != self.current_state:
            print(f"Смена состояния: {self.current_state} -> {state}")
            self.current_state = state

        # Обработка состояний
        if state == "battle":
            self.handle_battle(data)
        elif state == "map":
            self.handle_map()
        elif state == "exploring":
            self.handle_exploring()


def main():
    """Главный цикл бота"""
    bot = CombatBot()
    activate_game_window()
    print("Genshin Impact Bot запущен!")
    print("Для остановки нажмите Ctrl+C")
    print("Начинаю работу через 3 секунды...")
    time.sleep(3)

    try:
        while True:
            screenshot = pyautogui.screenshot()
            bot.update(screenshot)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n Бот остановлен пользователем")



if __name__ == "__main__":
        main()
