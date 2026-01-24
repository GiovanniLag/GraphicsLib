"""
Core module for GraphicsLib.

This module contains base classes and infrastructure for the library.
"""

from graphics_lib.core.base import BasePlot
from graphics_lib.core.registry import (
    Registry,
    PaletteRegistry,
    TypographyRegistry,
    PlotRegistry
)

__all__ = [
    'BasePlot',
    'Registry',
    'PaletteRegistry',
    'TypographyRegistry',
    'PlotRegistry'
]
