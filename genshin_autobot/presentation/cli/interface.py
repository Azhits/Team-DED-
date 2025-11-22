"""Bot Interface Module.

Модуль интерфейса бота.

This module provides a graphical user interface for the Genshin Impact
auto-bot using tkinter.

Этот модуль предоставляет графический интерфейс для автобота
Genshin Impact с использованием tkinter.
"""

import tkinter as tk
from typing import Optional, Callable


class BotInterface(tk.Tk):
    """Graphical user interface for the bot.
    
    Графический интерфейс для бота.
    
    This class provides a minimal overlay window that displays
    the bot status and allows user interaction.
    
    Attributes:
        button_clicked: Whether the start button has been clicked.
        status_label: Label widget showing bot status.
    """

    def __init__(
        self,
        title: str = 'Genshin Auto-Bot v0.1.0',
        width: int = 250,
        height: int = 100,
        on_start: Optional[Callable[[], None]] = None
    ) -> None:
        """Initialize the bot interface.
        
        Args:
            title: Window title text.
            width: Window width in pixels.
            height: Window height in pixels.
            on_start: Callback function when start button clicked.
            
        Raises:
            ValueError: If width or height are non-positive.
        """
        if width <= 0 or height <= 0:
            raise ValueError(
                f"Width and height must be positive, "
                f"got width={width}, height={height}"
            )
        
        super().__init__()
        
        self.title(title)
        self.resizable(False, False)
        self.button_clicked: bool = False
        self._on_start_callback: Optional[Callable[[], None]] = on_start
        
        # Calculate position (right side, vertically centered)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_pos = screen_width - width - 20
        y_pos = (screen_height - height) // 2
        
        self.geometry(f'{width}x{height}+{x_pos}+{y_pos}')
        self._create_widgets()
        
    def _create_widgets(self) -> None:
        """Create and configure interface widgets.
        
        Creates the frame, status label, and start button.
        """
        # Main frame
        frame = tk.Frame(self)
        frame.pack(expand=True, fill='both')
        
        # Status label
        self.status_label = tk.Label(
            self,
            text='Ожидание запуска...',
            width=30
        )
        self.status_label.pack(pady=5)
        self.status_label.bind("<Button-1>", self._on_button_click)
        
    def _on_button_click(self, event: tk.Event) -> None:
        """Handle button click event.
        
        Args:
            event: Tkinter event object.
        """
        self.button_clicked = True
        self.status_label.config(text='Бот запущен!')
        
        if self._on_start_callback:
            self._on_start_callback()
            
    def set_transparent(self, alpha: float = 0.3) -> None:
        """Set window transparency level.
        
        Args:
            alpha: Transparency level (0.0 to 1.0).
            
        Raises:
            ValueError: If alpha not in valid range.
        """
        if not 0.0 <= alpha <= 1.0:
            raise ValueError(
                f"Alpha must be between 0.0 and 1.0, got {alpha}"
            )
        self.attributes('-alpha', alpha)
        
    def set_topmost(self, topmost: bool = True) -> None:
        """Set window always-on-top behavior.
        
        Args:
            topmost: Whether window should stay on top.
        """
        self.attributes('-topmost', topmost)
        
    def update_status(self, status: str) -> None:
        """Update the status label text.
        
        Args:
            status: New status text to display.
        """
        self.status_label.config(text=status)
        self.update_idletasks()
