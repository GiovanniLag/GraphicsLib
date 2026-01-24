from __future__ import annotations

"""
Model fitting plot implementation using matplotlib.

This module provides a sophisticated plot class for visualizing
model fits to data, with optional residuals subplot.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import numpy as np
from matplotlib.axes import Axes

from graphics_lib.backends.matplotlib import MatplotlibPlot

if TYPE_CHECKING:
    from graphics_lib.colours import Palette
    from graphics_lib.typography import Typography


class FitPlot(MatplotlibPlot):
    """
    Plot for visualizing model fits to data with residuals.

    This class creates a publication-quality plot showing data points,
    a fitted model curve, and optionally a residuals subplot. It
    automatically applies palette colors and typography settings.

    Parameters
    ----------
    data : dict or array-like
        The data to plot. Should contain 'x' and 'y' keys if dict,
        or be a 2D array with shape (n, 2) or (n,) for y-only data.
    model : Callable
        The model function to fit the data. Should accept x as first
        argument and model parameters as keyword arguments.
    model_params : dict
        Parameters for the model function. Should match the model's
        expected parameters.
    title : str, optional
        The title of the plot. Default is 'Model Fit'.
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
    data_label : str, optional
        Label for the data points in the legend. Default is 'Data'.
    model_label : str, optional
        Label for the model line in the legend. Default is 'Model'.
    show_residuals : bool, optional
        Whether to show residuals plot below main plot.
        Default is True.
    figsize : tuple, optional
        Figure size (width, height) in inches. Default is (10, 8).
    rasterize_points : bool, optional
        Whether to rasterize the scatter points for better performance
        with large datasets. Default is False.
    **kwargs
        Additional keyword arguments for customization.

    Attributes
    ----------
    data : dict
        The plot data with 'x' and 'y' keys.
    model : Callable
        The model function.
    model_params : dict
        The model parameters.
    residuals : np.ndarray
        The calculated residuals (y_data - y_model).

    Examples
    --------
    >>> import numpy as np
    >>> from graphics_lib import FitPlot
    >>>
    >>> # Generate sample data
    >>> x = np.linspace(0, 10, 100)
    >>> y = 3 * np.exp(-x/2) + np.random.normal(0, 0.1, 100)
    >>> data = {'x': x, 'y': y}
    >>>
    >>> # Define model
    >>> def exp_model(x, amplitude, tau):
    ...     return amplitude * np.exp(-x/tau)
    >>>
    >>> # Create plot
    >>> plot = FitPlot(
    ...     data=data,
    ...     model=exp_model,
    ...     model_params={'amplitude': 3, 'tau': 2},
    ...     palette='qscience',
    ...     title='Exponential Decay'
    ... )
    >>> plot.show()
    """

    def __init__(
        self,
        data: dict | np.ndarray,
        model: Callable,
        model_params: dict[str, Any],
        title: str = 'Model Fit',
        palette: str | 'Palette' | None = None,
        typography: str | 'Typography' | None = None,
        xlabel: str = 'X-axis',
        ylabel: str = 'Y-axis',
        data_label: str = 'Data',
        model_label: str = 'Model',
        show_residuals: bool = True,
        figsize: tuple = (10, 8),
        rasterize_points: bool = False,
        **kwargs
    ) -> None:
        """Initialize the fit plot and render it."""
        super().__init__(
            title=title,
            palette=palette,
            typography=typography,
            figsize=figsize,
            **kwargs
        )

        # Store plot-specific attributes
        self.data = self._process_data(data)
        self.model = model
        self.model_params = model_params
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.data_label = data_label
        self.model_label = model_label
        self.show_residuals = show_residuals
        self.rasterize_points = rasterize_points
        self.residuals: np.ndarray | None = None

        # Render the plot
        self._render()

    def _process_data(
        self,
        data: dict | np.ndarray
    ) -> dict[str, np.ndarray]:
        """
        Process input data into standard format.

        Parameters
        ----------
        data : dict or array-like
            The input data.

        Returns
        -------
        dict
            Dictionary with 'x' and 'y' keys containing numpy arrays.
        """
        if isinstance(data, dict):
            return {
                'x': np.asarray(data['x']),
                'y': np.asarray(data['y'])
            }
        else:
            data_array = np.asarray(data)
            if data_array.ndim > 1:
                return {
                    'x': data_array[:, 0],
                    'y': data_array[:, 1]
                }
            else:
                return {
                    'x': np.arange(len(data_array)),
                    'y': data_array
                }

    def _render(self) -> None:
        """Render the fit plot with data, model, and optionally residuals."""
        # Create figure and axes
        if self.show_residuals:
            self.fig, (ax_main, ax_residuals) = self._create_figure(
                nrows=2,
                ncols=1,
                gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.1}
            )
            self.axes = [ax_main, ax_residuals]
        else:
            self.fig, ax_main = self._create_figure()
            ax_residuals = None
            self.axes = ax_main

        # Extract data
        x_data = self.data['x']
        y_data = self.data['y']

        # Get colors from palette
        scatter_color = (
            str(self.palette.colours['primary'])
            if self.palette
            else '#1f77b4'
        )
        line_color = (
            str(self.palette.colours['accent'])
            if self.palette
            else '#ff7f0e'
        )
        edge_color = (
            self.palette.primary.darken(10)
            if self.palette
            else '#0d5a87'
        )

        # Plot data points
        ax_main.scatter(
            x_data,
            y_data,
            color=scatter_color,
            alpha=0.3,
            s=30,
            label=self.data_label,
            zorder=2,
            edgecolors=str(edge_color),
            linewidth=0.8,
            rasterized=self.rasterize_points
        )

        # Generate smooth model curve
        x_fit = np.linspace(x_data.min(), x_data.max(), 300)
        y_fit = self.model(x_fit, **self.model_params)

        # Plot model line
        ax_main.plot(
            x_fit,
            y_fit,
            color=line_color,
            linewidth=2,
            label=self.model_label,
            zorder=3,
            alpha=0.9
        )

        # Calculate residuals
        y_model_data = self.model(x_data, **self.model_params)
        self.residuals = y_data - y_model_data

        # Apply styling to main plot
        self._style_axes(ax_main, show_xlabel=not self.show_residuals)

        # Handle residuals plot
        if self.show_residuals and ax_residuals is not None:
            self._plot_residuals(ax_residuals, x_data)

            # Share x-axis with main plot
            ax_main.sharex(ax_residuals)
            ax_main.tick_params(labelbottom=False)

    def _style_axes(
        self,
        ax: Axes,
        show_xlabel: bool = True
    ) -> None:
        """
        Apply styling to an axes object.

        Parameters
        ----------
        ax : Axes
            The axes to style.
        show_xlabel : bool, optional
            Whether to show x-axis label. Default is True.
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

        if show_xlabel:
            ax.set_xlabel(self.xlabel, **label_kwargs)

        # Add grid
        ax.grid(
            True,
            alpha=0.3,
            linestyle='--',
            color=grid_color
        )

        # Add legend
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

    def _plot_residuals(
        self,
        ax: Axes,
        x_data: np.ndarray
    ) -> None:
        """
        Plot residuals on a separate axes.

        Parameters
        ----------
        ax : Axes
            The axes to plot residuals on.
        x_data : np.ndarray
            The x-axis data.
        """
        # Get colors from palette
        scatter_color = (
            str(self.palette.colours['primary'])
            if self.palette
            else '#1f77b4'
        )
        line_color = (
            str(self.palette.colours['accent'])
            if self.palette
            else '#ff7f0e'
        )
        edge_color = (
            self.palette.primary.darken(10)
            if self.palette
            else '#0d5a87'
        )
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

        # Plot residuals
        ax.scatter(
            x_data,
            self.residuals,
            color=scatter_color,
            alpha=0.3,
            s=30,
            edgecolors=str(edge_color),
            linewidth=0.7,
            rasterized=self.rasterize_points
        )

        # Add zero line
        ax.axhline(
            y=0,
            color=line_color,
            linestyle='-',
            linewidth=1.5,
            alpha=0.8
        )

        # Set labels
        label_kwargs = {}
        if self.typography:
            label_kwargs = {
                'fontname': self.typography.subtitle.font,
                'fontsize': self.typography.subtitle.size,
                'color': text_color
            }
        else:
            label_kwargs = {'color': text_color}

        ax.set_xlabel(self.xlabel, **label_kwargs)
        ax.set_ylabel('Residuals', **label_kwargs)

        # Add grid
        ax.grid(
            True,
            alpha=0.5,
            linestyle='--',
            color=grid_color
        )

        # Set background color
        ax.set_facecolor(neutral_color)

        # Style spines
        for spine in ax.spines.values():
            spine.set_linewidth(1.2)
            spine.set_edgecolor(axes_border_color)

        # Set tick colors
        tick_kwargs = {}
        if self.typography:
            tick_kwargs = {
                'labelsize': self.typography.body.size - 1,
                'colors': axes_border_color,
                'labelcolor': text_color
            }
        else:
            tick_kwargs = {
                'colors': axes_border_color,
                'labelcolor': text_color
            }

        ax.tick_params(axis='both', **tick_kwargs)
