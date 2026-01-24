from __future__ import annotations

"""
Matplotlib backend for GraphicsLib.

This module provides the base class for all matplotlib-based plots,
handling figure/axes creation and matplotlib-specific operations.
"""

from abc import abstractmethod
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from graphics_lib.core.base import BasePlot

if TYPE_CHECKING:
    from graphics_lib.colours import Palette
    from graphics_lib.typography import Typography


class MatplotlibPlot(BasePlot):
    """
    Abstract base class for matplotlib-based plots.

    This class extends BasePlot with matplotlib-specific functionality,
    including figure and axes management, and matplotlib-specific
    save and show implementations.

    Parameters
    ----------
    title : str, optional
        The title of the plot. Default is empty string.
    palette : Union[str, Palette, None], optional
        The color palette to use. Default is None.
    typography : Union[str, Typography, None], optional
        The typography configuration to use. Default is None.
    figsize : tuple, optional
        The size of the figure in inches (width, height).
        Default is (10, 6).
    **kwargs
        Additional keyword arguments for plot customization.

    Attributes
    ----------
    fig : Figure or None
        The matplotlib Figure object.
    axes : Axes or list of Axes or None
        The matplotlib Axes object(s).
    """

    def __init__(
        self,
        title: str = '',
        palette: str | 'Palette' | None = None,
        typography: str | 'Typography' | None = None,
        figsize: tuple = (10, 6),
        **kwargs
    ) -> None:
        """
        Initialize the matplotlib plot.

        Creates the figure and axes for rendering.
        """
        super().__init__(
            title=title,
            palette=palette,
            typography=typography,
            figsize=figsize,
            **kwargs
        )
        self.fig: Figure | None = None
        self.axes: Axes | list | None = None

    def save(
        self,
        filename: str,
        dpi: int = 300,
        bbox_inches: str = 'tight',
        **kwargs
    ) -> None:
        """
        Save the plot to a file.

        Parameters
        ----------
        filename : str
            The output filename. The file format is inferred from
            the extension (e.g., .png, .pdf, .svg).
        dpi : int, optional
            The resolution in dots per inch. Default is 300.
        bbox_inches : str, optional
            The bounding box adjustment. Default is 'tight'.
        **kwargs
            Additional matplotlib savefig parameters.

        Raises
        ------
        RuntimeError
            If the plot has not been rendered yet.
        """
        if self.fig is None:
            raise RuntimeError(
                "Plot has not been rendered yet. "
                "Call _render() first or check initialization."
            )

        self.fig.savefig(
            filename,
            dpi=dpi,
            bbox_inches=bbox_inches,
            **kwargs
        )

    def show(self) -> None:
        """
        Display the plot.

        Raises
        ------
        RuntimeError
            If the plot has not been rendered yet.
        """
        if self.fig is None:
            raise RuntimeError(
                "Plot has not been rendered yet. "
                "Call _render() first or check initialization."
            )

        plt.show()

    @abstractmethod
    def _render(self) -> None:
        """
        Render the plot.

        This method must be implemented by concrete plot classes
        to create the actual visualization.
        """
        pass

    def _create_figure(
        self,
        nrows: int = 1,
        ncols: int = 1,
        **kwargs
    ) -> tuple[Figure, Axes | list]:
        """
        Create a matplotlib figure and axes.

        Parameters
        ----------
        nrows : int, optional
            Number of rows in the subplot grid. Default is 1.
        ncols : int, optional
            Number of columns in the subplot grid. Default is 1.
        **kwargs
            Additional keyword arguments for plt.subplots().

        Returns
        -------
        fig : Figure
            The matplotlib Figure object.
        axes : Axes or list of Axes
            The matplotlib Axes object(s).
        """
        fig, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=self.figsize,
            **kwargs
        )
        return fig, axes

    def _apply_typography(self, ax: Axes) -> None:
        """
        Apply typography settings to an axes.

        Parameters
        ----------
        ax : Axes
            The axes to apply typography to.
        """
        if self.typography is None:
            return

        # Apply title font
        if self.title:
            ax.set_title(
                self.title,
                fontsize=self.typography.title.size,
                fontfamily=self.typography.title.family,
                fontname=self.typography.title.font
            )

        # Apply body font to axis labels
        ax.set_xlabel(
            ax.get_xlabel(),
            fontsize=self.typography.body.size,
            fontfamily=self.typography.body.family,
            fontname=self.typography.body.font
        )
        ax.set_ylabel(
            ax.get_ylabel(),
            fontsize=self.typography.body.size,
            fontfamily=self.typography.body.family,
            fontname=self.typography.body.font
        )

        # Apply caption font to tick labels
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(self.typography.caption.size)
            label.set_fontfamily(self.typography.caption.family)
            label.set_fontname(self.typography.caption.font)
