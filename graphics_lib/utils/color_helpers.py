from __future__ import annotations

"""
Color utility functions for GraphicsLib.

This module provides helper functions for extracting and manipulating
colors from palettes and generating color gradients.
"""

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from graphics_lib.colours import Palette


def get_plot_colors(
    palette: 'Palette' | None,
    n_colors: int | None = None
) -> list[str]:
    """
    Get a list of colors suitable for plotting from a palette.

    Extracts colors from a palette in a preferred order suitable for
    multi-series plots. If no palette is provided, returns matplotlib
    default colors.

    Parameters
    ----------
    palette : Palette or None
        The color palette to extract colors from.
    n_colors : int, optional
        Number of colors needed. If None, returns the default cycling
        colors. If specified, cycles through available colors to reach
        the requested number.

    Returns
    -------
    List[str]
        List of color strings (hex format) suitable for plotting.

    Notes
    -----
    Color extraction priority:
    1. primary
    2. accent
    3. secondary
    4. accent2
    5. status_info
    6. status_success
    7. status_warning
    8. status_error
    """
    if palette is None:
        # Default matplotlib colors if no palette provided
        default_colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        return default_colors[:n_colors] if n_colors else default_colors

    # Define the preferred order of colors for plotting from a palette
    color_priority = [
        'primary', 'accent', 'secondary', 'accent2',
        'status_info', 'status_success', 'status_warning', 'status_error'
    ]

    plot_colors = []
    for color_name in color_priority:
        if color_name in palette.colours:
            plot_colors.append(str(palette.colours[color_name]))

    # If no colors found, use a fallback
    if not plot_colors:
        return ['blue']

    # If we need more colors than available, cycle through what we have
    if n_colors and len(plot_colors) < n_colors:
        repeat_count = (n_colors // len(plot_colors)) + 1
        plot_colors = (plot_colors * repeat_count)[:n_colors]

    return plot_colors


def interpolate_colors(colors: list[str], n_colors: int) -> list[str]:
    """
    Interpolate between colors to generate a gradient.

    Creates a smooth color gradient by linearly interpolating between
    the provided colors in RGB space.

    Parameters
    ----------
    colors : List[str]
        List of color strings to interpolate between. Colors should be
        in a format recognized by matplotlib (hex, named colors, etc.).
    n_colors : int
        Number of colors to generate in the gradient.

    Returns
    -------
    List[str]
        List of interpolated color strings in hex format.

    Notes
    -----
    - If only one color is provided, returns that color repeated.
    - If n_colors is less than or equal to the number of input colors,
      returns the first n_colors from the input.
    - Interpolation is performed in RGB space using linear interpolation.

    Examples
    --------
    >>> colors = ['#FF0000', '#0000FF']  # Red to Blue
    >>> interpolate_colors(colors, 5)
    ['#ff0000', '#bf003f', '#7f007f', '#3f00bf', '#0000ff']
    """
    if len(colors) < 2:
        # If only one color provided, return that color repeated
        return [colors[0]] * n_colors if colors else ['blue'] * n_colors

    if n_colors <= len(colors):
        # If we need fewer colors than provided, just take a subset
        return colors[:n_colors]

    # Import matplotlib.colors for color interpolation
    from matplotlib.colors import to_hex, to_rgb

    # Convert colors to RGB
    rgb_colors = [to_rgb(color) for color in colors]

    # Create interpolation points
    original_positions = np.linspace(0, 1, len(rgb_colors))
    target_positions = np.linspace(0, 1, n_colors)

    # Interpolate each RGB channel
    interpolated_colors = []
    for pos in target_positions:
        # Find the two colors to interpolate between
        idx = np.searchsorted(original_positions, pos)

        if idx == 0:
            interpolated_colors.append(rgb_colors[0])
        elif idx >= len(rgb_colors):
            interpolated_colors.append(rgb_colors[-1])
        else:
            # Linear interpolation between two colors
            t = (pos - original_positions[idx - 1]) / (
                original_positions[idx] - original_positions[idx - 1]
            )
            rgb1 = np.array(rgb_colors[idx - 1])
            rgb2 = np.array(rgb_colors[idx])
            interpolated_rgb = rgb1 + t * (rgb2 - rgb1)
            interpolated_colors.append(tuple(interpolated_rgb))

    # Convert back to hex strings
    return [to_hex(rgb) for rgb in interpolated_colors]
