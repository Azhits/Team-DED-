"""Модуль оркестрации игрового процесса бота.
Pipeline orchestration module for game bot.

Этот модуль предоставляет основной конвейер выполнения бота,
координирующий различные компоненты системы.
This module provides main execution pipeline coordinating
various system components.
"""

import time
import logging
from typing import Optional, Dict, Any

from genshin_autobot.core.entities.character import (
    CharacterStateChecker
)
from genshin_autobot.core.use_cases.events_checker import (
    EventsChecker
)
from genshin_autobot.core.use_cases.game_controller import (
    GameController
)
from genshin_autobot.infrastructure.vision.frame_coordinator import (
    FrameTextCoordinator
)


class Pipeline:
    """Основной конвейер выполнения бота.
    
    Main execution pipeline for bot operations.
    Coordinates character state checking, event detection,
    and gameplay control.
    
    Attributes:
        character_checker: Character state monitoring component
        events_checker: Game events detection component
        game_controller: Gameplay actions controller
        frame_coordinator: Frame text extraction coordinator
        is_running: Pipeline execution status flag
    """

    def __init__(
        self,
        character_checker: CharacterStateChecker,
        events_checker: EventsChecker,
        game_controller: GameController,
        frame_coordinator: FrameTextCoordinator
    ) -> None:
        """Инициализация конвейера.
        
        Initialize pipeline with required components.
        
        Args:
            character_checker: Character state checker instance
            events_checker: Events checker instance
            game_controller: Game controller instance
            frame_coordinator: Frame coordinator instance
            
        Raises:
            TypeError: If any component is not of expected type
        """
        if not isinstance(character_checker, CharacterStateChecker):
            raise TypeError(
                "character_checker must be CharacterStateChecker"
            )
        if not isinstance(events_checker, EventsChecker):
            raise TypeError(
                "events_checker must be EventsChecker"
            )
        if not isinstance(game_controller, GameController):
            raise TypeError(
                "game_controller must be GameController"
            )
        if not isinstance(frame_coordinator, FrameTextCoordinator):
            raise TypeError(
                "frame_coordinator must be FrameTextCoordinator"
            )
        
        self._character_checker = character_checker
        self._events_checker = events_checker
        self._game_controller = game_controller
        self._frame_coordinator = frame_coordinator
        self._is_running = False
        self._logger = logging.getLogger(__name__)

    def start(self) -> None:
        """Запуск конвейера выполнения.
        
        Start pipeline execution loop.
        """
        self._is_running = True
        self._logger.info("Pipeline started")

    def stop(self) -> None:
        """Остановка конвейера выполнения.
        
        Stop pipeline execution.
        """
        self._is_running = False
        self._logger.info("Pipeline stopped")

    def execute_cycle(self) -> Dict[str, Any]:
        """Выполнение одного цикла конвейера.
        
        Execute single pipeline cycle.
        
        Returns:
            Dictionary with cycle execution results containing:
            - character_state: Character health status
            - detected_events: List of detected game events
            - actions_taken: List of performed actions
            
        Raises:
            RuntimeError: If pipeline is not running
        """
        if not self._is_running:
            raise RuntimeError(
                "Cannot execute cycle: pipeline not running"
            )
        
        results = {
            'character_state': None,
            'detected_events': [],
            'actions_taken': []
        }
        
        try:
            # Check character state
            char_state = self._character_checker.check_state()
            results['character_state'] = char_state
            
            # Check for game events
            events = self._events_checker.check_events()
            results['detected_events'] = events
            
            # Execute game actions based on state and events
            if char_state and char_state.is_critical:
                action = self._game_controller.execute_healing()
                results['actions_taken'].append(action)
            
            for event in events:
                action = self._game_controller.handle_event(event)
                results['actions_taken'].append(action)
                
        except Exception as e:
            self._logger.error(f"Error in pipeline cycle: {e}")
            raise
        
        return results

    def run(self, max_cycles: Optional[int] = None) -> None:
        """Запуск основного цикла конвейера.
        
        Run main pipeline loop.
        
        Args:
            max_cycles: Maximum number of cycles to execute.
                       None for infinite loop.
                       
        Raises:
            ValueError: If max_cycles is negative
        """
        if max_cycles is not None and max_cycles < 0:
            raise ValueError(
                "max_cycles must be non-negative"
            )
        
        self.start()
        cycle_count = 0
        
        try:
            while self._is_running:
                if max_cycles and cycle_count >= max_cycles:
                    break
                    
                self.execute_cycle()
                cycle_count += 1
                time.sleep(0.1)  # Small delay between cycles
                
        except KeyboardInterrupt:
            self._logger.info("Pipeline interrupted by user")
        finally:
            self.stop()

    @property
    def is_running(self) -> bool:
        """Получить статус выполнения конвейера.
        
        Get pipeline running status.
        
        Returns:
            True if pipeline is running, False otherwise
        """
        return self._is_running
