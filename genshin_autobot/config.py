"""Application configuration settings.

Конфигурация приложения.

Этот модуль содержит все константы и настройки
для работы бота Genshin Impact.

This module contains all constants and settings
for the Genshin Impact bot.
"""

import os
from pathlib import Path


# Paths / Пути
BASE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = BASE_DIR / "infrastructure" / "resources"
STATIC_DIR = RESOURCES_DIR / "static"
IMAGES_DIR = RESOURCES_DIR / "images"

# Screen settings / Настройки экрана
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_REGION = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Game window settings / Настройки окна игры
GAME_WINDOW_TITLE = "Genshin Impact"
GAME_WINDOW_CLASS = "UnityWndClass"

# Vision settings / Настройки распознавания
MATCH_THRESHOLD = 0.8  # Template matching confidence
MATCH_THRESHOLD_HIGH = 0.9  # High confidence threshold
MATCH_THRESHOLD_LOW = 0.7  # Low confidence threshold

# Timing settings / Настройки тайминга
DEFAULT_DELAY = 0.5  # seconds
FAST_DELAY = 0.1  # seconds
SLOW_DELAY = 1.0  # seconds
CHECK_INTERVAL = 0.2  # seconds
MAX_WAIT_TIME = 30.0  # seconds

# Combat settings / Настройки боя
COMBAT_TIMEOUT = 60.0  # seconds
SKILL_COOLDOWN = 2.0  # seconds
BURST_COOLDOWN = 3.0  # seconds
DODGE_COOLDOWN = 1.0  # seconds

# Character switching / Переключение персонажей
CHARACTER_SWITCH_DELAY = 0.3  # seconds
MAX_CHARACTERS = 4

# Keyboard bindings / Клавиатурные привязки
KEY_ATTACK = "left"
KEY_SKILL = "e"
KEY_BURST = "q"
KEY_JUMP = "space"
KEY_SPRINT = "shift"
KEY_CHARACTER_1 = "1"
KEY_CHARACTER_2 = "2"
KEY_CHARACTER_3 = "3"
KEY_CHARACTER_4 = "4"
KEY_INTERACT = "f"
KEY_MENU = "esc"

# Mouse settings / Настройки мыши
MOUSE_MOVE_SPEED = 0.1  # seconds for smooth movement
CLICK_DELAY = 0.05  # seconds between press and release

# Logging settings / Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOG_FILE = BASE_DIR / "genshin_autobot.log"

# Debug mode / Режим отладки
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"
SAVE_SCREENSHOTS = DEBUG_MODE
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Performance settings / Настройки производительности
FRAME_SKIP = 1  # Process every Nth frame
CPU_THREADS = os.cpu_count() or 4
