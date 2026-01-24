"""
Plotly-based plot implementations for GraphicsLib.

This module contains interactive plot classes using Plotly
as the rendering backend.

Note: Install the 'interactive' extras to use Plotly:

    pip install graphics-lib[interactive]

For advanced interactive features with Dash, install the
'dash' extras:

    pip install graphics-lib[dash]
"""

from graphics_lib.plots.plotly.scatter import ScatterPlot
from graphics_lib.plots.plotly.dash_scatter import DashScatterPlot

__all__ = ['ScatterPlot', 'DashScatterPlot']
