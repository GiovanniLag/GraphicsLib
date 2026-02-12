from __future__ import annotations

"""
Scatter plot implementation using matplotlib.

This module provides a flexible scatter plot class that supports
different colors for individual points, automatic color cycling,
and gradients.
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


class ScatterPlot(MatplotlibPlot):
    """
    Flexible scatter plot supporting single or multiple data series.

    This class creates scatter plots with automatic color management,
    gradient support, point-wise color control, and full integration
    with palette and typography settings. It can handle single or
    multiple data series seamlessly, and allows different colors for
    individual points.

    Parameters
    ----------
    x : array-like or list of array-like
        X data for the plot(s). Can be a single array or list of arrays
        for multiple scatter series.
    y : array-like or list of array-like
        Y data for the plot(s). Can be a single array or list of arrays
        for multiple scatter series.
    title : str, optional
        Title of the plot. Default is 'Scatter Plot'.
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
        Legend labels for the scatter series. Can be a single string
        or list of strings. Default is None.
    colors : str, list of str, or list of list of str, optional
        Colors for the scatter points. Can be:
        - A single color string (applied to all points)
        - A list of colors (one per series, or cycled)
        - A list of lists (point-wise colors for each series)
        If not provided, colors will be automatically cycled from the
        palette. Default is None.
    sizes : float, array-like, or list of array-like, optional
        Marker sizes for the scatter points. Can be:
        - A single float (applied to all points)
        - An array (point-wise sizes for single series)
        - A list of arrays (point-wise sizes for each series)
        Default is 50.
    marker : str or list of str, optional
        Marker style(s) for the scatter points. Can be a single marker
        or list of markers. Default is 'o' (circle).
    alpha : float or list of float, optional
        Transparency level(s) for the scatter points. Can be a single
        value or list of values. Default is 0.7.
    edgecolors : str, list of str, or None, optional
        Edge colors for the markers. Default is None.
    linewidths : float or list of float, optional
        Width(s) of marker edges. Default is 1.0.
    error : dict, np.ndarray, list, or None, optional
        Error bar specification for the scatter points. Accepts
        several formats:

        - None: No error bars on any series.
        - A dict with ``'x'`` and/or ``'y'`` keys containing arrays:
          applied to every series (or the single series).
        - A 1D array: Interpreted as x-direction errors for a
          single series.
        - A 2D array of shape ``(2, n)``: First row is x errors,
          second row is y errors, for a single series.
        - A list of the above: Per-series error specs. Each element
          can be None (plain scatter), a dict, a 1D array, or a 2D
          array. Length should match the number of series; shorter
          lists are padded with None.

        When error bars are active for a series, ``ax.errorbar`` is
        used instead of ``ax.scatter``. Default is None.
    gradient : bool, optional
        If True, interpolates between the colors in the 'colors' list
        to create a gradient across all series. If False, colors are
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
        Number of scatter series to plot.
    plot_labels : list
        Labels for each scatter series.
    plot_colors : list
        Colors for each scatter series or individual points.
    plot_sizes : list
        Sizes for points in each scatter series.
    plot_markers : list
        Marker styles for each scatter series.
    plot_alphas : list
        Transparency values for each scatter series.
    plot_errors : list of dict
        Per-series error specs. Each element is a dict with ``'x'``
        and ``'y'`` keys (values are arrays or None).

    Examples
    --------
    >>> import numpy as np
    >>> from graphics_lib import ScatterPlot
    >>>
    >>> # Single scatter plot with uniform colors
    >>> x = np.random.rand(50)
    >>> y = np.random.rand(50)
    >>> plot = ScatterPlot(
    ...     x, y,
    ...     title='Random Points',
    ...     palette='qscience'
    ... )
    >>> plot.show()
    >>>
    >>> # Single scatter plot with different colors per point
    >>> x = np.random.rand(50)
    >>> y = np.random.rand(50)
    >>> colors = ['red' if xi > 0.5 else 'blue' for xi in x]
    >>> plot = ScatterPlot(
    ...     x, y,
    ...     title='Colored by X value',
    ...     colors=colors,
    ...     palette='qscience'
    ... )
    >>> plot.show()
    >>>
    >>> # Multiple scatter series with gradient
    >>> x = [np.random.rand(30), np.random.rand(30), np.random.rand(30)]
    >>> y = [np.random.rand(30), np.random.rand(30), np.random.rand(30)]
    >>> plot = ScatterPlot(
    ...     x, y,
    ...     title='Multiple Series',
    ...     labels=['Group A', 'Group B', 'Group C'],
    ...     colors=['#FF0000', '#0000FF'],
    ...     gradient=True,
    ...     palette='qscience'
    ... )
    >>> plot.show()
    >>>
    >>> # Scatter plot with varying sizes
    >>> x = np.random.rand(100)
    >>> y = np.random.rand(100)
    >>> sizes = np.random.rand(100) * 200
    >>> plot = ScatterPlot(
    ...     x, y,
    ...     title='Variable Sizes',
    ...     sizes=sizes,
    ...     alpha=0.5
    ... )
    >>> plot.show()
    >>>
    >>> # Scatter with error bars on selected series
    >>> x = [np.arange(10), np.arange(10)]
    >>> y = [np.random.rand(10), np.random.rand(10)]
    >>> plot = ScatterPlot(
    ...     x, y,
    ...     labels=['With errors', 'Plain'],
    ...     error=[{'y': np.random.rand(10) * 0.1}, None],
    ... )
    >>> plot.show()
    """

    def __init__(
        self,
        x: np.ndarray | list[np.ndarray],
        y: np.ndarray | list[np.ndarray],
        title: str = 'Scatter Plot',
        palette: str | Palette | None = None,
        typography: str | Typography | None = None,
        xlabel: str = 'X-axis',
        ylabel: str = 'Y-axis',
        figsize: tuple = (10, 6),
        grid: bool = True,
        labels: str | list[str] | None = None,
        colors: (
            str | list[str] | list[list[str]] | None
        ) = None,
        sizes: float | np.ndarray | list | None = None,
        marker: str | list[str] = 'o',
        alpha: float | list[float] = 0.7,
        edgecolors: str | list[str] | None = None,
        linewidths: float | list[float] = 1.0,
        error: np.ndarray | dict | list | None = None,
        gradient: bool = False,
        ax: Axes | None = None,
        **kwargs
    ) -> None:
        """Initialize the scatter plot and render it."""
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

        # Process labels and visual properties
        self.plot_labels = self._process_labels(labels)
        self.plot_colors = self._process_colors(colors)
        self.plot_sizes = self._process_sizes(sizes)
        self.plot_markers = self._process_markers(marker)
        self.plot_alphas = self._process_alphas(alpha)
        self.plot_edgecolors = self._process_edgecolors(edgecolors)
        self.plot_linewidths = self._process_linewidths(linewidths)
        self.plot_errors = self._process_errors(error)

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
        colors: str | list[str] | list[list[str]] | None
    ) -> list:
        """
        Process colors into appropriate format for each plot.

        Supports:
        - Single color (applied to all plots)
        - List of colors (one per series or cycled)
        - List of lists (point-wise colors for each series)

        Parameters
        ----------
        colors : str, list of str, list of lists, or None
            Input colors.

        Returns
        -------
        list
            List of colors for each series (can be single colors or
            arrays for point-wise coloring).
        """
        if colors is None:
            return get_plot_colors(self.palette, self.n_plots)
        elif isinstance(colors, str):
            return [colors] * self.n_plots
        elif isinstance(colors, (list, tuple)):
            # Check if it's point-wise colors (list of lists)
            if (len(colors) > 0 and
                    isinstance(colors[0], (list, tuple, np.ndarray))):
                # Point-wise colors for each series
                plot_colors = list(colors)
                # Pad with None if not enough color arrays
                while len(plot_colors) < self.n_plots:
                    plot_colors.append(None)
                return plot_colors
            else:
                # Check if this is point-wise colors for a single series
                # (list of color strings matching data length)
                if (self.n_plots == 1 and len(colors) > 0 and
                        isinstance(colors[0], str) and
                        len(colors) == len(self.x_data[0])):
                    # Point-wise colors for single series
                    return [list(colors)]
                # Series-level colors
                elif self.gradient and len(colors) >= 2:
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

    def _process_sizes(
        self,
        sizes: float | np.ndarray | list | None
    ) -> list:
        """
        Process sizes into appropriate format for each plot.

        Parameters
        ----------
        sizes : float, array-like, list, or None
            Input sizes.

        Returns
        -------
        list
            List of sizes for each series (can be single values or
            arrays for point-wise sizing).
        """
        if sizes is None:
            return [50] * self.n_plots
        elif isinstance(sizes, (int, float)):
            return [sizes] * self.n_plots
        elif isinstance(sizes, np.ndarray):
            # Single array of sizes
            if self.n_plots == 1:
                return [sizes]
            else:
                return [sizes] + [50] * (self.n_plots - 1)
        elif isinstance(sizes, (list, tuple)):
            # Check if it's point-wise sizes (list of arrays)
            if (len(sizes) > 0 and
                    isinstance(sizes[0], (list, tuple, np.ndarray))):
                # Point-wise sizes for each series
                plot_sizes = [np.asarray(s) for s in sizes]
                # Pad with default if not enough
                while len(plot_sizes) < self.n_plots:
                    plot_sizes.append(50)
                return plot_sizes
            else:
                # Could be a single array as list
                if self.n_plots == 1:
                    return [np.asarray(sizes)]
                else:
                    return [np.asarray(sizes)] + [50] * (self.n_plots - 1)
        else:
            return [50] * self.n_plots

    def _process_markers(
        self,
        marker: str | list[str]
    ) -> list[str]:
        """
        Process markers into a list matching the number of plots.

        Parameters
        ----------
        marker : str or list of str
            Input marker(s).

        Returns
        -------
        List[str]
            List of marker styles, one per plot.
        """
        if isinstance(marker, str):
            return [marker] * self.n_plots
        elif isinstance(marker, (list, tuple)):
            markers = list(marker)
            if len(markers) < self.n_plots:
                # Cycle through markers
                marker_cycle = cycle(markers)
                markers = [next(marker_cycle) for _ in range(self.n_plots)]
            return markers
        else:
            return ['o'] * self.n_plots

    def _process_alphas(
        self,
        alpha: float | list[float]
    ) -> list[float]:
        """
        Process alpha values into a list matching the number of plots.

        Parameters
        ----------
        alpha : float or list of float
            Input alpha value(s).

        Returns
        -------
        List[float]
            List of alpha values, one per plot.
        """
        if isinstance(alpha, (int, float)):
            return [alpha] * self.n_plots
        elif isinstance(alpha, (list, tuple)):
            alphas = list(alpha)
            if len(alphas) < self.n_plots:
                # Cycle through alphas
                alpha_cycle = cycle(alphas)
                alphas = [next(alpha_cycle) for _ in range(self.n_plots)]
            return alphas
        else:
            return [0.7] * self.n_plots

    def _process_edgecolors(
        self,
        edgecolors: str | list[str] | None
    ) -> list[str | None]:
        """
        Process edge colors into a list matching the number of plots.

        Parameters
        ----------
        edgecolors : str, list of str, or None
            Input edge color(s).

        Returns
        -------
        List[Optional[str]]
            List of edge colors, one per plot.
        """
        if edgecolors is None:
            return [None] * self.n_plots
        elif isinstance(edgecolors, str):
            return [edgecolors] * self.n_plots
        elif isinstance(edgecolors, (list, tuple)):
            edges = list(edgecolors)
            if len(edges) < self.n_plots:
                # Cycle through edge colors
                edge_cycle = cycle(edges)
                edges = [next(edge_cycle) for _ in range(self.n_plots)]
            return edges
        else:
            return [None] * self.n_plots

    def _process_linewidths(
        self,
        linewidths: float | list[float]
    ) -> list[float]:
        """
        Process line widths into a list matching the number of plots.

        Parameters
        ----------
        linewidths : float or list of float
            Input line width(s).

        Returns
        -------
        List[float]
            List of line widths, one per plot.
        """
        if isinstance(linewidths, (int, float)):
            return [linewidths] * self.n_plots
        elif isinstance(linewidths, (list, tuple)):
            widths = list(linewidths)
            if len(widths) < self.n_plots:
                # Cycle through linewidths
                width_cycle = cycle(widths)
                widths = [next(width_cycle) for _ in range(self.n_plots)]
            return widths
        else:
            return [1.0] * self.n_plots

    def _process_errors(
        self,
        error: np.ndarray | dict | list | None
    ) -> list[dict[str, np.ndarray | None]]:
        """
        Process error input into per-series standard format.

        Parameters
        ----------
        error : np.ndarray, dict, list, or None
            Error bar specification. Accepted formats:

            - None: No error bars on any series.
            - dict with ``'x'`` and/or ``'y'`` keys: Applied to
              every series.
            - 1D array: X-direction errors for a single series.
            - 2D array ``(2, n)``: Row 0 = x errors,
              row 1 = y errors, for a single series.
            - list of the above: Per-series specs. Each element
              can be None, a dict, a 1D array or a 2D array.

        Returns
        -------
        list of dict
            One dict per series with ``'x'`` and ``'y'`` keys
            (values are numpy arrays or None).

        Raises
        ------
        ValueError
            If an error array has more than 2 dimensions.
        """
        no_error: dict[str, np.ndarray | None] = {
            'x': None, 'y': None
        }

        if error is None:
            return [dict(no_error) for _ in range(self.n_plots)]

        # ----------------------------------------------------------
        # Helper: convert a single spec into a normalised dict
        # ----------------------------------------------------------
        def _normalise_single(
            spec: np.ndarray | dict | None,
        ) -> dict[str, np.ndarray | None]:
            """Convert one error spec to {'x': ..., 'y': ...}."""
            if spec is None:
                return dict(no_error)
            if isinstance(spec, dict):
                return {
                    'x': (
                        np.asarray(spec['x'])
                        if 'x' in spec
                        else None
                    ),
                    'y': (
                        np.asarray(spec['y'])
                        if 'y' in spec
                        else None
                    ),
                }
            arr = np.asarray(spec)
            if arr.ndim == 1:
                return {'x': arr, 'y': None}
            elif arr.ndim == 2:
                return {'x': arr[0], 'y': arr[1]}
            else:
                raise ValueError(
                    "Error array must be 1D or 2D, "
                    f"got {arr.ndim}D."
                )

        # ----------------------------------------------------------
        # Detect whether *error* is a per-series list
        # ----------------------------------------------------------
        if isinstance(error, list):
            # Heuristic: if every element is None, a dict, or an
            # ndarray/list whose first element is also a sequence,
            # treat it as a per-series list. The simplest reliable
            # check: if any element is None or dict, it must be a
            # per-series list.
            is_per_series = any(
                item is None or isinstance(item, dict)
                for item in error
            )
            if not is_per_series:
                # Could still be per-series (list of arrays). Check
                # if length matches n_plots and each element looks
                # like an array whose length matches the data.
                if len(error) == self.n_plots:
                    is_per_series = all(
                        hasattr(item, '__len__')
                        and len(item) == len(self.x_data[idx])
                        for idx, item in enumerate(error)
                    )

            if is_per_series:
                result = [
                    _normalise_single(item) for item in error
                ]
                # Pad with no-error if shorter than n_plots
                while len(result) < self.n_plots:
                    result.append(dict(no_error))
                return result

        # ----------------------------------------------------------
        # Single spec – broadcast to all series
        # ----------------------------------------------------------
        single = _normalise_single(error)
        return [dict(single) for _ in range(self.n_plots)]

    def _render(self) -> None:
        """Render the scatter plot."""
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
            xerr_i = self.plot_errors[i]['x']
            yerr_i = self.plot_errors[i]['y']
            has_errors = xerr_i is not None or yerr_i is not None

            if has_errors:
                # Use errorbar for this series
                # Map scatter size to approximate marker size
                size_val = self.plot_sizes[i]
                if isinstance(size_val, (int, float)):
                    msize = max(1.0, np.sqrt(size_val) / 2)
                else:
                    # Point-wise sizes: use median as marker size
                    msize = max(
                        1.0,
                        np.sqrt(np.median(size_val)) / 2
                    )

                color_i = self.plot_colors[i]
                edge_i = (
                    self.plot_edgecolors[i]
                    if self.plot_edgecolors[i] is not None
                    else color_i
                )

                ax.errorbar(
                    self.x_data[i],
                    self.y_data[i],
                    xerr=xerr_i,
                    yerr=yerr_i,
                    fmt=self.plot_markers[i],
                    color=color_i,
                    ecolor=edge_i,
                    elinewidth=self.plot_linewidths[i],
                    capsize=3,
                    capthick=self.plot_linewidths[i],
                    markersize=msize,
                    markeredgecolor=edge_i,
                    markeredgewidth=self.plot_linewidths[i],
                    alpha=self.plot_alphas[i],
                    label=self.plot_labels[i],
                    zorder=2,
                )
            else:
                ax.scatter(
                    self.x_data[i],
                    self.y_data[i],
                    c=self.plot_colors[i],
                    s=self.plot_sizes[i],
                    marker=self.plot_markers[i],
                    alpha=self.plot_alphas[i],
                    edgecolors=self.plot_edgecolors[i],
                    linewidths=self.plot_linewidths[i],
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
