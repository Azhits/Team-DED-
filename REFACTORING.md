# Руководство по рефакторингу кода

Этот документ содержит практические примеры рефакторинга существующего кода проекта согласно стандартам PEP8 и принципам Clean Architecture.

## 📋 Содержание

1. [Примеры рефакторинга классов](#примеры-рефакторинга-классов)
2. [Улучшение структуры модулей](#улучшение-структуры-модулей)
3. [Добавление type hints и docstrings](#type-hints-и-docstrings)
4. [Рефакторинг контроллеров](#рефакторинг-контроллеров)

---

## Примеры рефакторинга классов

### ❌ ДО: keyboard_and_mouse_controllers.py

```python
class MouseMover:
    def move_cursor_to_coords(self, coords: tuple[int, int], duration: float=0.1):
        pgui.moveTo(x=coords[2], y=coords[1], duration=duration)
```

**Проблемы:**
- Неправильный индекс coords[2] (должен быть coords[0])
- Отсутствует docstring
- Нет проверки валидности координат
- Не указан return type (None)

### ✅ ПОСЛЕ: infrastructure/input/mouse_controller.py

```python
from typing import Tuple
import pyautogui as pgui


class MouseController:
    """Контроллер для управления мышью."""
    
    def move_cursor_to_coords(
        self,
        coords: Tuple[int, int],
        duration: float = 0.1
    ) -> None:
        """Перемещает курсор в указанные координаты.
        
        Args:
            coords: Кортеж (x, y) с координатами экрана.
            duration: Длительность перемещения в секундах.
            
        Raises:
            ValueError: Если координаты выходят за пределы экрана.
        """
        x, y = coords
        screen_width, screen_height = pgui.size()
        
        if not (0 <= x <= screen_width and 0 <= y <= screen_height):
            raise ValueError(
                f"Координаты ({x}, {y}) выходят за пределы экрана "
                f"({screen_width}x{screen_height})"
            )
        
        pgui.moveTo(x=x, y=y, duration=duration)
```

---

## Улучшение структуры модулей

### ❌ ДО: Model/gameplay_controllers.py

Все контроллеры геймплея в одном файле (60+ строк)

### ✅ ПОСЛЕ: Разделение по ответственностям

```
infrastructure/input/
├── __init__.py
├── keyboard_controller.py
├── mouse_controller.py
└── base_controller.py

core/use_cases/
├── __init__.py
├── combat_manager.py  # Управление боем
├── character_controller.py  # Управление персонажем
└── camera_controller.py  # Управление камерой
```

---

## Type Hints и Docstrings

### ❌ ДО: EventsChecker.py

```python
class EventsChecker:
    def check_invite_in_dungeon(self, event_type: str='invite'):
        return state.event_listeners.check_clicable_event_button(self.frame, event_type)
```

### ✅ ПОСЛЕ: infrastructure/vision/event_detector.py

```python
import cv2
import numpy as np
from typing import Optional
from enum import Enum


class EventType(Enum):
    """Типы игровых событий."""
    INVITE = "invite"
    ACTIVATE = "activate"
    START_SQUAD = "start_squad"


class EventDetector:
    """Детектор игровых событий на экране."""
    
    def __init__(self, frame: np.ndarray, templates_dir: str):
        """Инициализация детектора событий.
        
        Args:
            frame: Кадр игры для анализа.
            templates_dir: Путь к директории с шаблонами.
        """
        self.frame = frame
        self.templates_dir = templates_dir
    
    def check_invite_in_dungeon(
        self,
        event_type: EventType = EventType.INVITE
    ) -> bool:
        """Проверяет наличие приглашения в подземелье.
        
        Args:
            event_type: Тип события для проверки.
            
        Returns:
            True если событие обнаружено, False иначе.
        """
        template_path = self._get_template_path(event_type)
        return self._match_template(template_path, threshold=0.8)
    
    def _get_template_path(self, event_type: EventType) -> str:
        """Получает путь к шаблону для типа события."""
        return f"{self.templates_dir}/{event_type.value}_template.png"
    
    def _match_template(
        self,
        template_path: str,
        threshold: float = 0.8
    ) -> bool:
        """Ищет шаблон на кадре.
        
        Args:
            template_path: Путь к файлу шаблона.
            threshold: Порог совпадения (0-1).
            
        Returns:
            True если совпадение найдено.
        """
        template = cv2.imread(template_path)
        result = cv2.matchTemplate(self.frame, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val >= threshold
```

---

## Рефакторинг контроллеров

### ❌ ДО: gameplay_controllers.py

```python
class Runner:
    def __init__(self, keybord_controller=controllers.KeyboardController()):
        self.keybord_controller =keybord_controller
    
    def start_run(self, key='shift'):
        self.keybord_controller.start_run(key=key)
```

**Проблемы:**
- Опечатка: keybord → keyboard
- Нет пробела после знака =
- Отсутствует type hinting
- Нет docstring

### ✅ ПОСЛЕ: core/use_cases/movement_controller.py

```python
from typing import Optional
from infrastructure.input.keyboard_controller import KeyboardController


class MovementController:
    """Контроллер управления передвижением персонажа."""
    
    def __init__(
        self,
        keyboard_controller: Optional[KeyboardController] = None
    ):
        """Инициализация контроллера движения.
        
        Args:
            keyboard_controller: Контроллер клавиатуры.
                Если None, создается новый экземпляр.
        """
        self._keyboard = keyboard_controller or KeyboardController()
    
    def start_run(self, key: str = 'shift') -> None:
        """Начинает бег персонажа.
        
        Args:
            key: Клавиша для бега (по умолчанию 'shift').
        """
        self._keyboard.press_key(key)
    
    def stop_run(self, key: str = 'shift') -> None:
        """Останавливает бег персонажа.
        
        Args:
            key: Клавиша для остановки бега.
        """
        self._keyboard.release_key(key)
```

---

## Создание базовых классов

### ✅ НОВОЕ: core/entities/base.py

```python
from abc import ABC, abstractmethod
from typing import Dict, Any


class Entity(ABC):
    """Базовый класс для всех игровых сущностей."""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Конвертирует сущность в словарь."""
        pass
    
    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Загружает сущность из словаря."""
        pass
```

### ✅ НОВОЕ: core/entities/character.py

```python
from typing import Dict, Any
from .base import Entity


class Character(Entity):
    """Модель игрового персонажа."""
    
    def __init__(
        self,
        name: str,
        level: int = 1,
        hp: int = 100,
        energy: int = 100
    ):
        """Инициализация персонажа.
        
        Args:
            name: Имя персонажа.
            level: Уровень персонажа.
            hp: Здоровье персонажа.
            energy: Энергия персонажа.
        """
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.energy = energy
        self.max_energy = energy
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертирует персонажа в словарь."""
        return {
            'name': self.name,
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'energy': self.energy,
            'max_energy': self.max_energy,
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Загружает персонажа из словаря."""
        self.name = data['name']
        self.level = data['level']
        self.hp = data['hp']
        self.max_hp = data['max_hp']
        self.energy = data['energy']
        self.max_energy = data['max_energy']
    
    def is_alive(self) -> bool:
        """Проверяет, жив ли персонаж."""
        return self.hp > 0
    
    def __repr__(self) -> str:
        return (
            f"Character(name={self.name!r}, level={self.level}, "
            f"hp={self.hp}/{self.max_hp})"
        )
```

---

## Checklist рефакторинга

- [ ] Все классы следуют PascalCase
- [ ] Все функции/методы следуют snake_case
- [ ] Константы в UPPER_SNAKE_CASE
- [ ] Все публичные функции имеют docstrings
- [ ] Добавлены type hints для всех параметров и возвратов
- [ ] Строки не длиннее 79 символов (или 99 для docstrings)
- [ ] Между top-level определениями 2 пустые строки
- [ ] Импорты сгруппированы: stdlib → third-party → local
- [ ] Нет unused imports
- [ ] Файлы разбиты по принципу единой ответственности
- [ ] Созданы __init__.py для всех пакетов

---

## Инструменты для автоматизации

### Установка инструментов качества кода:

```bash
pip install black flake8 mypy pylint isort
```

### Автоформатирование с black:

```bash
black genshin_autobot/
```

### Проверка с flake8:

```bash
flake8 genshin_autobot/ --max-line-length=88
```

### Проверка типов с mypy:

```bash
mypy genshin_autobot/ --strict
```

### Сортировка импортов с isort:

```bash
isort genshin_autobot/
```

---

## Следующие шаги

1. Начните с рефакторинга одного модуля (например, keyboard_and_mouse_controllers.py)
2. Напишите unit-тесты для рефакторенного кода
3. Постепенно мигрируйте остальные модули
4. Настройте pre-commit hooks для автоматической проверки
5. Обновите документацию

Удачи в рефакторинге! 🚀
