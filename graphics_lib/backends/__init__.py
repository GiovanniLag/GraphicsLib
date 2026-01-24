"""
Backend implementations for GraphicsLib.

This module contains backend-specific base classes and utilities
for rendering plots with different visualization libraries.
"""

from graphics_lib.backends.matplotlib import MatplotlibPlot

__all__ = ['MatplotlibPlot']
