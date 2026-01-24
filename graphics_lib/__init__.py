"""
Graphics Library - A simple graphics library.

This library provides tools for graphics operations.
"""

__version__ = "0.1.0"
__author__ = "Giovanni Laganà"

# Core components
from graphics_lib.colours import Colour, Palette, COLOURS, coolors_palette
from graphics_lib.typography import Font, Typography

# Plot classes
from graphics_lib.plots.matplotlib import FitPlot, LinePlot

# Registries for string shortcuts
from graphics_lib.core.registry import (
    PaletteRegistry,
    TypographyRegistry,
    PlotRegistry
)

# Example palettes and typography (triggers registration)
from graphics_lib.palettes import QSciencePalette, create_simple_palette
from graphics_lib.typography import QScienceTypography

# Utility functions
from graphics_lib.utils.color_helpers import get_plot_colors, interpolate_colors


# Legacy function-based API for backward compatibility
import warnings
from typing import Union, Callable, Dict, Any, Optional


def plot_fit(
    data,
    model: Callable,
    model_params: Dict[str, Any],
    title: str = 'Model Fit',
    palette: Union[str, Palette, None] = None,
    typography: Union[str, Typography, None] = None,
    **kwargs
):
    """
    Create a fit plot (legacy function interface).

    .. deprecated:: 0.2.0
        Use `FitPlot` class instead for better functionality.

    Parameters
    ----------
    data : dict or array-like
        The data to plot.
    model : Callable
        The model function.
    model_params : dict
        Parameters for the model function.
    title : str, optional
        The title of the plot.
    palette : Union[str, Palette, None], optional
        The color palette to use.
    typography : Union[str, Typography, None], optional
        The typography settings.
    **kwargs
        Additional keyword arguments.

    Returns
    -------
    tuple
        (fig, axes) where axes is the matplotlib axes object(s).

    Notes
    -----
    This function is deprecated. Use the `FitPlot` class instead:

        >>> from graphics_lib import FitPlot
        >>> plot = FitPlot(data, model, model_params, ...)
        >>> plot.show()
    """
    warnings.warn(
        "plot_fit function is deprecated. Use FitPlot class instead.",
        DeprecationWarning,
        stacklevel=2
    )
    plot = FitPlot(
        data=data,
        model=model,
        model_params=model_params,
        title=title,
        palette=palette,
        typography=typography,
        **kwargs
    )
    return plot.fig, plot.axes


def plot(x, y, **kwargs):
    """
    Create a line plot (legacy function interface).

    .. deprecated:: 0.2.0
        Use `LinePlot` class instead for better functionality.

    Parameters
    ----------
    x : array-like or list of array-like
        X data for the plot(s).
    y : array-like or list of array-like
        Y data for the plot(s).
    **kwargs
        Additional keyword arguments.

    Returns
    -------
    tuple or None
        (fig, ax) if return_fig=True, otherwise None.

    Notes
    -----
    This function is deprecated. Use the `LinePlot` class instead:

        >>> from graphics_lib import LinePlot
        >>> plot = LinePlot(x, y, ...)
        >>> plot.show()
    """
    warnings.warn(
        "plot function is deprecated. Use LinePlot class instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return_fig = kwargs.pop('return_fig', False)
    line_plot = LinePlot(x=x, y=y, **kwargs)

    if return_fig:
        return line_plot.fig, line_plot.axes
    else:
        line_plot.show()
        return None


__all__ = [
    # Version info
    '__version__',
    '__author__',

    # Core classes
    'Colour',
    'Palette',
    'Font',
    'Typography',

    # Plot classes
    'FitPlot',
    'LinePlot',

    # Registries
    'PaletteRegistry',
    'TypographyRegistry',
    'PlotRegistry',

    # Example palettes and typography
    'QSciencePalette',
    'QScienceTypography',

    # Utility functions
    'COLOURS',
    'coolors_palette',
    'create_simple_palette',
    'get_plot_colors',
    'interpolate_colors',

    # Legacy API (deprecated)
    'plot_fit',
    'plot',
]
