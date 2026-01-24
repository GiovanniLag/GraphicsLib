"""
Plotly-based plot implementations for GraphicsLib.

This module contains interactive plot classes using Plotly
as the rendering backend.

Note: Install the 'interactive' extras to use Plotly:

    pip install graphics-lib[interactive]
"""

from graphics_lib.plots.plotly.scatter import ScatterPlot

__all__ = ['ScatterPlot']
