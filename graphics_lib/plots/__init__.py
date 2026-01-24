"""
Matplotlib-based plot implementations for GraphicsLib.

This module contains concrete plot classes that use matplotlib
as the rendering backend.
"""

from graphics_lib.plots.matplotlib.fit import FitPlot
from graphics_lib.plots.matplotlib.line import LinePlot
from graphics_lib.plots.matplotlib.scatter import ScatterPlot

__all__ = ['FitPlot', 'LinePlot', 'ScatterPlot']
