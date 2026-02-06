from __future__ import annotations

"""
Line plot implementation using matplotlib.

This module provides a flexible line plot class that supports single
or multiple data series with automatic color cycling and gradients.
"""

from itertools import cycle
from typing import TYPE_CHECKING

import numpy as np
from matplotlib.axes import Axes

from graphics_lib.backends.matplotlib import MatplotlibPlot
from graphics_lib.utils.color_helpers import (
    get_plot_colors,
    interpolate_colors,
)

if TYPE_CHECKING:
    from graphics_lib.colours import Palette
    from graphics_lib.typography import Typography


class LinePlot(MatplotlibPlot):
    """
    Flexible line plot supporting single or multiple data series.

    This class creates line plots with automatic color management,
    gradient support, and full integration with palette and typography
    settings. It can handle single or multiple data series seamlessly.

    Parameters
    ----------
    x : array-like or list of array-like
        X data for the plot(s). Can be a single array or list of arrays
        for multiple plots.
    y : array-like or list of array-like
        Y data for the plot(s). Can be a single array or list of arrays
        for multiple plots.
    title : str, optional
        Title of the plot. Default is 'Plot'.
    palette : Union[str, Palette, None], optional
        The color palette for the plot. Can be a Palette object or
        a string name for registry lookup. Default is None.
    typography : Union[str, Typography, None], optional
        The typography settings for the plot. Can be a Typography
        object or a string name for registry lookup. Default is None.
    xlabel : str, optional
        Label for the x-axis. Default is 'X-axis'.
    ylabel : str, optional
        Label for the y-axis. Default is 'Y-axis'.
    figsize : tuple, optional
        Figure size in inches (width, height). Default is (10, 6).
    grid : bool, optional
        Whether to show grid lines. Default is True.
    labels : str or list of str, optional
        Legend labels for the plot(s). Can be a single string or list
        of strings. Default is None.
    colors : str or list of str, optional
        Colors for the plot(s). Can be a single color or list of colors.
        If not provided, colors will be automatically cycled from the
        palette. Default is None.
    gradient : bool, optional
        If True, interpolates between the colors in the 'colors' list
        to create a gradient across all plots. If False, colors are
        used as discrete values. Default is False.
    ax : Axes, optional
        Matplotlib axes object to draw the plot on. If provided, the plot
        will be drawn on this axes instead of creating a new figure.
        Default is None.
    **kwargs
        Additional keyword arguments for plot customization.

    Attributes
    ----------
    x_data : list of np.ndarray
        List of x-axis data arrays.
    y_data : list of np.ndarray
        List of y-axis data arrays.
    n_plots : int
        Number of data series to plot.
    plot_labels : list
        Labels for each data series.
    plot_colors : list
        Colors for each data series.

    Examples
    --------
    >>> import numpy as np
    >>> from graphics_lib import LinePlot
    >>>
    >>> # Single plot
    >>> x = np.linspace(0, 10, 100)
    >>> y = np.sin(x)
    >>> plot = LinePlot(x, y, title='Sine Wave', palette='qscience')
    >>> plot.show()
    >>>
    >>> # Multiple plots with gradient
    >>> x = np.linspace(0, 10, 100)
    >>> y_list = [np.sin(x), np.cos(x), np.sin(2*x)]
    >>> plot = LinePlot(
    ...     x, y_list,
    ...     title='Trigonometric Functions',
    ...     labels=['sin(x)', 'cos(x)', 'sin(2x)'],
    ...     colors=['#FF0000', '#0000FF'],
    ...     gradient=True,
    ...     palette='qscience'
    ... )
    >>> plot.show()
    """

    def __init__(
        self,
        x: np.ndarray | list[np.ndarray],
        y: np.ndarray | list[np.ndarray],
        title: str = 'Plot',
        palette: str | 'Palette' | None = None,
        typography: str | 'Typography' | None = None,
        xlabel: str = 'X-axis',
        ylabel: str = 'Y-axis',
        figsize: tuple = (10, 6),
        grid: bool = True,
        labels: str | list[str] | None = None,
        colors: str | list[str] | None = None,
        gradient: bool = False,
        ax: Axes | None = None,
        **kwargs
    ) -> None:
        """Initialize the line plot and render it."""
        super().__init__(
            title=title,
            palette=palette,
            typography=typography,
            figsize=figsize,
            **kwargs
        )

        # Store plot-specific attributes
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.grid_enabled = grid
        self.gradient = gradient
        self.external_ax = ax

        # Process data into lists for consistent handling
        self.x_data, self.y_data = self._normalize_data(x, y)
        self.n_plots = len(self.y_data)

        # Process labels and colors
        self.plot_labels = self._process_labels(labels)
        self.plot_colors = self._process_colors(colors)

        # Render the plot
        self._render()

    def _normalize_data(
        self,
        x: np.ndarray | list[np.ndarray],
        y: np.ndarray | list[np.ndarray]
    ) -> tuple:
        """
        Normalize input data to lists of arrays.

        Parameters
        ----------
        x : array-like or list of array-like
            X data.
        y : array-like or list of array-like
            Y data.

        Returns
        -------
        tuple
            (x_data, y_data) as lists of numpy arrays.
        """
        def _to_list(data):
            """Convert single items or lists to lists."""
            if isinstance(data, (list, tuple)):
                # Check if it's multiple plots or single plot
                if (len(data) > 0 and hasattr(data[0], '__len__') and
                        not isinstance(data[0], str)):
                    return [np.asarray(d) for d in data]
                else:
                    return [np.asarray(data)]
            else:
                return [np.asarray(data)]

        x_data = _to_list(x)
        y_data = _to_list(y)

        # Broadcast x or y if necessary
        if len(x_data) == 1 and len(y_data) > 1:
            x_data = x_data * len(y_data)
        elif len(y_data) == 1 and len(x_data) > 1:
            y_data = y_data * len(x_data)
        elif len(x_data) != len(y_data):
            raise ValueError(
                f"Number of x datasets ({len(x_data)}) must match "
                f"number of y datasets ({len(y_data)})"
            )

        return x_data, y_data

    def _process_labels(
        self,
        labels: str | list[str] | None
    ) -> list[str | None]:
        """
        Process labels into a list matching the number of plots.

        Parameters
        ----------
        labels : str, list of str, or None
            Input labels.

        Returns
        -------
        List[Optional[str]]
            List of labels, one per plot.
        """
        if labels is None:
            return [None] * self.n_plots
        elif isinstance(labels, str):
            if self.n_plots == 1:
                return [labels]
            else:
                return [f"{labels} {i+1}" for i in range(self.n_plots)]
        elif isinstance(labels, (list, tuple)):
            plot_labels = list(labels)
            # Pad with None if not enough labels provided
            while len(plot_labels) < self.n_plots:
                plot_labels.append(None)
            return plot_labels
        else:
            return [None] * self.n_plots

    def _process_colors(
        self,
        colors: str | list[str] | None
    ) -> list[str]:
        """
        Process colors into a list matching the number of plots.

        Parameters
        ----------
        colors : str, list of str, or None
            Input colors.

        Returns
        -------
        List[str]
            List of color strings, one per plot.
        """
        if colors is None:
            return get_plot_colors(self.palette, self.n_plots)
        elif isinstance(colors, str):
            return [colors] * self.n_plots
        elif isinstance(colors, (list, tuple)):
            if self.gradient and len(colors) >= 2:
                # Use gradient interpolation
                return interpolate_colors(list(colors), self.n_plots)
            else:
                # Use colors as discrete values
                plot_colors = list(colors)
                if len(plot_colors) < self.n_plots:
                    # Cycle through colors
                    color_cycle = cycle(plot_colors)
                    plot_colors = [
                        next(color_cycle) for _ in range(self.n_plots)
                    ]
                return plot_colors
        else:
            return get_plot_colors(self.palette, self.n_plots)

    def _render(self) -> None:
        """Render the line plot."""
        # Create figure and axes or use provided axes
        if self.external_ax is not None:
            ax = self.external_ax
            self.fig = ax.get_figure()
            self.axes = ax
        else:
            self.fig, ax = self._create_figure()
            self.axes = ax

        # Plot all datasets
        for i in range(self.n_plots):
            ax.plot(
                self.x_data[i],
                self.y_data[i],
                color=self.plot_colors[i],
                linewidth=2,
                label=self.plot_labels[i]
            )

        # Apply styling
        self._style_axes(ax)

    def _style_axes(self, ax: Axes) -> None:
        """
        Apply styling to the axes.

        Parameters
        ----------
        ax : Axes
            The axes to style.
        """
        # Get colors from palette
        text_color = (
            str(self.palette.colours['text_primary'])
            if self.palette and 'text_primary' in self.palette.colours
            else 'black'
        )
        neutral_color = (
            str(self.palette.colours['neutral_light'])
            if self.palette and 'neutral_light' in self.palette.colours
            else 'white'
        )
        axes_border_color = (
            str(self.palette.colours['neutral_dark'])
            if self.palette and 'neutral_dark' in self.palette.colours
            else 'black'
        )
        grid_color = (
            str(self.palette.neutral_dark.lighten(20))
            if self.palette and hasattr(self.palette, 'neutral_dark')
            else 'gray'
        )

        # Set title and labels
        title_kwargs = {}
        label_kwargs = {}

        if self.typography:
            title_kwargs = {
                'fontname': self.typography.title.font,
                'fontsize': self.typography.title.size,
                'color': text_color
            }
            label_kwargs = {
                'fontname': self.typography.subtitle.font,
                'fontsize': self.typography.subtitle.size,
                'color': text_color
            }
        else:
            title_kwargs = {'color': text_color}
            label_kwargs = {'color': text_color}

        ax.set_title(
            self.title,
            fontweight='bold',
            pad=20,
            **title_kwargs
        )
        ax.set_ylabel(self.ylabel, **label_kwargs)
        ax.set_xlabel(self.xlabel, **label_kwargs)

        # Add grid
        ax.grid(
            self.grid_enabled,
            alpha=0.3,
            linestyle='--',
            color=grid_color
        )

        # Set background colors
        self.fig.patch.set_facecolor(neutral_color)
        ax.set_facecolor(neutral_color)

        # Style spines
        for spine in ax.spines.values():
            spine.set_linewidth(1.2)
            spine.set_edgecolor(axes_border_color)

        # Set tick colors
        ax.tick_params(
            axis='both',
            colors=axes_border_color,
            labelcolor=text_color
        )

        # Add legend if there are labels
        if any(label is not None for label in self.plot_labels):
            legend_kwargs = (
                {'fontsize': self.typography.body.size}
                if self.typography
                else {}
            )
            ax.legend(
                frameon=True,
                fancybox=True,
                shadow=True,
                facecolor=neutral_color,
                edgecolor=axes_border_color,
                **legend_kwargs
            )

        # Use tight layout only if not using external axes
        if self.external_ax is None:
            self.fig.tight_layout()
