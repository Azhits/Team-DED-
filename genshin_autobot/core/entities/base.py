"""Base entity classes.

Этот модуль содержит базовые классы сущностей для представления игровых объектов.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Entity(ABC):
    """Abstract base class for all game entities.
    
    Представляет базовый класс для всех игровых сущностей.
    """

    def __init__(self, entity_id: Optional[str] = None) -> None:
        """Initialize entity.

        Args:
            entity_id: Unique identifier for the entity.
        """
        self._id = entity_id
        self._attributes: Dict[str, Any] = {}

    @property
    def id(self) -> Optional[str]:
        """Get entity identifier.

        Returns:
            Entity ID or None if not set.
        """
        return self._id

    @property
    def attributes(self) -> Dict[str, Any]:
        """Get entity attributes.

        Returns:
            Dictionary of entity attributes.
        """
        return self._attributes.copy()

    def set_attribute(self, key: str, value: Any) -> None:
        """Set entity attribute.

        Args:
            key: Attribute name.
            value: Attribute value.
        """
        self._attributes[key] = value

    def get_attribute(self, key: str, default: Any = None) -> Any:
        """Get entity attribute.

        Args:
            key: Attribute name.
            default: Default value if attribute not found.

        Returns:
            Attribute value or default.
        """
        return self._attributes.get(key, default)

    @abstractmethod
    def validate(self) -> bool:
        """Validate entity state.

        Returns:
            True if entity is valid, False otherwise.
        """
        pass

    def __repr__(self) -> str:
        """String representation of entity.

        Returns:
            String representation.
        """
        return f"{self.__class__.__name__}(id={self._id})"
