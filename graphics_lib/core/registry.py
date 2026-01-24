"""from __future__ import annotations
Registry system for managing palettes, typography, and plot types.

This module provides a flexible registry pattern for managing named
instances of palettes, typography sets, and plot classes.
"""

from abc import ABC
from collections.abc import Callable
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from graphics_lib.colours import Palette
    from graphics_lib.typography import Typography


T = TypeVar('T')


class Registry(ABC, Generic[T]):
    """
    Generic registry base class for managing named items.

    This class provides a common interface for registering and retrieving
    items by name, with helpful error messages and discovery features.

    Parameters
    ----------
    T : TypeVar
        The type of items stored in the registry.

    Attributes
    ----------
    _items : Dict[str, T]
        Internal storage for registered items.
    """

    _items: dict[str, T] = {}

    @classmethod
    def register(
        cls,
        name: str,
        item: T | Callable[[], T],
        override: bool = False
    ) -> None:
        """
        Register an item with the registry.

        Parameters
        ----------
        name : str
            The name to register the item under.
        item : Union[T, Callable[[], T]]
            The item to register, or a callable that returns the item.
        override : bool, optional
            Whether to override existing items. Default is False.

        Raises
        ------
        ValueError
            If the name is already registered and override is False.
        """
        if name in cls._items and not override:
            raise ValueError(
                f"'{name}' is already registered. "
                f"Use override=True to replace it."
            )
        cls._items[name] = item

    @classmethod
    def get(cls, name: str) -> T:
        """
        Get an item by name.

        Parameters
        ----------
        name : str
            The name of the item to retrieve.

        Returns
        -------
        T
            The registered item.

        Raises
        ------
        KeyError
            If the name is not found in the registry.
        """
        if name not in cls._items:
            available = ', '.join(cls.list_available())
            raise KeyError(
                f"'{name}' not found in registry. "
                f"Available: {available if available else 'none'}"
            )

        item = cls._items[name]

        # Support lazy instantiation via callables
        if callable(item) and not isinstance(item, type):
            item = item()
            cls._items[name] = item

        return item

    @classmethod
    def list_available(cls) -> list[str]:
        """
        List all registered item names.

        Returns
        -------
        List[str]
            A sorted list of all registered names.
        """
        return sorted(cls._items.keys())

    @classmethod
    def unregister(cls, name: str) -> None:
        """
        Remove an item from the registry.

        Useful for testing or dynamic configuration.

        Parameters
        ----------
        name : str
            The name of the item to remove.
        """
        cls._items.pop(name, None)

    @classmethod
    def clear(cls) -> None:
        """
        Clear all items from the registry.

        Useful for testing or resetting the registry state.
        """
        cls._items.clear()


class PaletteRegistry(Registry):
    """
    Registry for named color palettes.

    Use this registry to store and retrieve palettes by name,
    enabling string shortcuts in plot constructors.
    """

    _items: dict[str, 'Palette'] = {}


class TypographyRegistry(Registry):
    """
    Registry for named typography sets.

    Use this registry to store and retrieve typography configurations
    by name, enabling string shortcuts in plot constructors.
    """

    _items: dict[str, 'Typography'] = {}


class PlotRegistry(Registry):
    """
    Registry for plot types.

    Use this registry to store and retrieve plot classes by name,
    enabling factory functions and dynamic plot creation.
    """

    _items: dict[str, type] = {}
