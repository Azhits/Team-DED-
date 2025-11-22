#!/usr/bin/env python3
"""Main entry point for Genshin Impact Auto-Fight Bot.

Точка входа для бота Genshin Impact.

This script initializes and starts the bot with CLI interface.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from genshin_autobot import config
from genshin_autobot.core.use_cases.game_controller import (
    GameController
)


def setup_logging() -> None:
    """
    Configure logging for the application.
    
    Настраивает логирование для приложения.
    """
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper()),
        format=config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main() -> int:
    """
    Main function to start the bot.
    
    Главная функция запуска бота.
    
    Returns:
        Exit code (0 for success, 1 for error).
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Genshin Impact Auto-Fight Bot...")
        logger.info(f"Version: {config.__version__}")
        logger.info(f"Debug mode: {config.DEBUG_MODE}")
        
        # Initialize game controller
        controller = GameController()
        
        # Start the game
        logger.info("Initializing game controller...")
        controller.start_game()
        
        logger.info("Bot started successfully!")
        logger.info(
            "Press Ctrl+C to stop the bot."
        )
        
        # TODO: Add main game loop here
        # This would include:
        # - Vision system integration
        # - Decision making
        # - Action execution
        # - Event handling
        
        # For now, just keep it running
        import time
        while controller.is_running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received stop signal...")
        if 'controller' in locals():
            controller.stop_game()
        logger.info("Bot stopped successfully.")
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
