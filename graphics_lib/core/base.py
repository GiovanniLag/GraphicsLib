from __future__ import annotations

"""
Base classes for all plot types in GraphicsLib.

This module defines the abstract base class that all plot implementations
must inherit from, providing a common interface for rendering, saving,
and displaying plots.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphics_lib.colours import Palette
    from graphics_lib.typography import Typography


class BasePlot(ABC):
    """
    Abstract base class for all plot types.

    This class defines the common interface and behavior for all plots,
    including palette and typography resolution, and abstract methods
    for rendering and output.

    Parameters
    ----------
    title : str, optional
        The title of the plot. Default is empty string.
    palette : Union[str, Palette, None], optional
        The color palette to use. Can be a Palette object or a string
        name that will be resolved via PaletteRegistry. Default is None.
    typography : Union[str, Typography, None], optional
        The typography configuration to use. Can be a Typography object
        or a string name that will be resolved via TypographyRegistry.
        Default is None.
    figsize : tuple, optional
        The size of the figure in inches (width, height).
        Default is (10, 6).
    **kwargs
        Additional keyword arguments for plot customization.

    Attributes
    ----------
    title : str
        The plot title.
    palette : Palette or None
        The resolved color palette.
    typography : Typography or None
        The resolved typography configuration.
    figsize : tuple
        The figure size.
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
        Initialize the base plot.

        Resolves string shortcuts for palette and typography via
        their respective registries.
        """
        self.title = title
        self.palette = self._resolve_palette(palette)
        self.typography = self._resolve_typography(typography)
        self.figsize = figsize
        self.extra_kwargs = kwargs

    def _resolve_palette(
        self,
        palette: str | 'Palette' | None
    ) -> 'Palette' | None:
        """
        Resolve palette from string or return the palette object.

        Parameters
        ----------
        palette : Union[str, Palette, None]
            The palette to resolve.

        Returns
        -------
        Palette or None
            The resolved palette object, or None if not provided.
        """
        if palette is None:
            return None

        if isinstance(palette, str):
            # Import here to avoid circular imports
            from graphics_lib.core.registry import PaletteRegistry
            return PaletteRegistry.get(palette)

        return palette

    def _resolve_typography(
        self,
        typography: str | 'Typography' | None
    ) -> 'Typography' | None:
        """
        Resolve typography from string or return the typography object.

        Parameters
        ----------
        typography : Union[str, Typography, None]
            The typography to resolve.

        Returns
        -------
        Typography or None
            The resolved typography object, or None if not provided.
        """
        if typography is None:
            return None

        if isinstance(typography, str):
            # Import here to avoid circular imports
            from graphics_lib.core.registry import TypographyRegistry
            return TypographyRegistry.get(typography)

        return typography

    @abstractmethod
    def _render(self) -> None:
        """
        Render the plot.

        This method must be implemented by all concrete plot classes
        to perform the actual rendering of the plot using the
        appropriate backend.
        """
        pass

    @abstractmethod
    def save(self, filename: str, **kwargs) -> None:
        """
        Save the plot to a file.

        Parameters
        ----------
        filename : str
            The output filename.
        **kwargs
            Backend-specific save options.
        """
        pass

    @abstractmethod
    def show(self) -> None:
        """
        Display the plot.

        This method displays the plot using the backend's display
        mechanism (e.g., plt.show() for matplotlib, fig.show() for Plotly).
        """
        pass
