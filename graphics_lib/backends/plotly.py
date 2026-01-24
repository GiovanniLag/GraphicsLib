from __future__ import annotations

"""
Plotly backend for GraphicsLib.

This module provides the base class for all Plotly-based plots,
handling figure creation and Plotly-specific operations.
"""

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from graphics_lib.core.base import BasePlot

if TYPE_CHECKING:
    from graphics_lib.colours import Palette
    from graphics_lib.typography import Typography


class PlotlyPlot(BasePlot):
    """
    Abstract base class for Plotly-based interactive plots.

    This class extends BasePlot with Plotly-specific functionality,
    including figure management and Plotly-specific save and show
    implementations.

    Note: Plotly must be installed to use this backend.

    Parameters
    ----------
    title : str, optional
        The title of the plot. Default is empty string.
    palette : Union[str, Palette, None], optional
        The color palette to use. Default is None.
    typography : Union[str, Typography, None], optional
        The typography configuration to use. Default is None.
    figsize : tuple, optional
        The size of the figure in pixels (width, height).
        Default is (1000, 600).
    **kwargs
        Additional keyword arguments for plot customization.

    Attributes
    ----------
    figure : plotly.graph_objects.Figure or None
        The Plotly Figure object.
    """

    def __init__(
        self,
        title: str = '',
        palette: str | 'Palette' | None = None,
        typography: str | 'Typography' | None = None,
        figsize: tuple = (1000, 600),
        **kwargs
    ) -> None:
        """
        Initialize the Plotly plot.

        Creates the figure for rendering.
        """
        super().__init__(
            title=title,
            palette=palette,
            typography=typography,
            figsize=figsize,
            **kwargs
        )
        self.figure: Any | None = None  # plotly.graph_objects.Figure

    def save(
        self,
        filename: str,
        **kwargs
    ) -> None:
        """
        Save the plot to a file.

        Parameters
        ----------
        filename : str
            The output filename. The file format is inferred from
            the extension:
            - .html for interactive HTML files
            - .png, .jpg, .jpeg, .webp, .svg, .pdf for static images
              (requires kaleido package)
        **kwargs
            Additional Plotly write_html or write_image parameters.

        Raises
        ------
        RuntimeError
            If the plot has not been rendered yet.
        ImportError
            If Plotly is not installed.
        """
        if self.figure is None:
            raise RuntimeError(
                "Plot has not been rendered yet. "
                "Call _render() first or check initialization."
            )

        try:
            import plotly.graph_objects as go
        except ImportError as exc:
            raise ImportError(
                "Plotly is not installed. "
                "Install it with: pip install plotly"
            ) from exc

        # Determine output format from extension
        if filename.endswith('.html'):
            self.figure.write_html(filename, **kwargs)
        else:
            # Requires kaleido for static image export
            try:
                self.figure.write_image(filename, **kwargs)
            except Exception as e:
                raise RuntimeError(
                    f"Failed to save static image. "
                    f"Install kaleido with: pip install kaleido. "
                    f"Error: {e}"
                ) from e

    def show(self) -> None:
        """
        Display the plot interactively.

        Raises
        ------
        RuntimeError
            If the plot has not been rendered yet.
        ImportError
            If Plotly is not installed.
        """
        if self.figure is None:
            raise RuntimeError(
                "Plot has not been rendered yet. "
                "Call _render() first or check initialization."
            )

        try:
            import plotly.graph_objects as go
        except ImportError as exc:
            raise ImportError(
                "Plotly is not installed. "
                "Install it with: pip install plotly"
            ) from exc

        self.figure.show()

    @abstractmethod
    def _render(self) -> None:
        """
        Render the plot.

        This method must be implemented by concrete plot classes
        to create the actual visualization.
        """
        pass

    def _create_figure(self, **kwargs) -> Any:
        """
        Create a Plotly figure.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments for go.Figure().

        Returns
        -------
        plotly.graph_objects.Figure
            The Plotly Figure object.

        Raises
        ------
        ImportError
            If Plotly is not installed.
        """
        try:
            import plotly.graph_objects as go
        except ImportError as exc:
            raise ImportError(
                "Plotly is not installed. "
                "Install it with: pip install plotly"
            ) from exc

        return go.Figure(**kwargs)

    def _apply_typography(self) -> None:
        """
        Apply typography settings to the figure.

        Updates the figure's layout with font settings from
        the typography configuration.
        """
        if self.typography is None or self.figure is None:
            return

        # Apply typography to layout
        self.figure.update_layout(
            title_font={
                'family': self.typography.title.font,
                'size': self.typography.title.size
            },
            font={
                'family': self.typography.body.font,
                'size': self.typography.body.size
            },
            xaxis={
                'title_font': {
                    'family': self.typography.body.font,
                    'size': self.typography.body.size
                }
            },
            yaxis={
                'title_font': {
                    'family': self.typography.body.font,
                    'size': self.typography.body.size
                }
            }
        )

    def to_json(self) -> str:
        """
        Export the figure as JSON.

        Returns
        -------
        str
            JSON representation of the figure.

        Raises
        ------
        RuntimeError
            If the plot has not been rendered yet.
        """
        if self.figure is None:
            raise RuntimeError(
                "Plot has not been rendered yet. "
                "Call _render() first or check initialization."
            )

        return self.figure.to_json()
