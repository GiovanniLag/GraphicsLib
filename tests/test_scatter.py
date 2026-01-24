"""
Unit tests for ScatterPlot class.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing

import numpy as np
import pytest

from graphics_lib.plots.matplotlib.scatter import ScatterPlot


def test_scatter_plot_basic():
    """Test basic scatter plot creation."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])

    plot = ScatterPlot(x, y, title='Test Plot')

    assert plot.title == 'Test Plot'
    assert len(plot.x_data) == 1
    assert len(plot.y_data) == 1
    assert plot.n_plots == 1
    assert plot.fig is not None
    assert plot.axes is not None


def test_scatter_plot_with_colors():
    """Test scatter plot with series-level colors."""
    x = np.array([1, 2, 3])
    y = np.array([1, 2, 3])
    colors = ['red', 'green', 'blue']

    plot = ScatterPlot(x, y, colors=colors)

    # For single series with list of colors, first color is used
    assert plot.plot_colors[0] == 'red'


def test_scatter_plot_with_pointwise_colors():
    """Test scatter plot with point-wise colors."""
    x = np.array([1, 2, 3])
    y = np.array([1, 2, 3])
    # Pass as list of lists to indicate point-wise colors
    colors = [['red', 'green', 'blue']]

    plot = ScatterPlot(x, y, colors=colors)

    # Should preserve the list of colors for point-wise coloring
    assert plot.plot_colors[0] == ['red', 'green', 'blue']


def test_scatter_plot_multiple_series():
    """Test scatter plot with multiple series."""
    x = [np.array([1, 2, 3]), np.array([4, 5, 6])]
    y = [np.array([1, 2, 3]), np.array([4, 5, 6])]

    plot = ScatterPlot(x, y, labels=['Series 1', 'Series 2'])

    assert plot.n_plots == 2
    assert len(plot.x_data) == 2
    assert len(plot.y_data) == 2
    assert plot.plot_labels[0] == 'Series 1'
    assert plot.plot_labels[1] == 'Series 2'


def test_scatter_plot_with_sizes():
    """Test scatter plot with varying sizes."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    sizes = np.array([50, 100, 150, 200, 250])

    plot = ScatterPlot(x, y, sizes=sizes)

    assert isinstance(plot.plot_sizes[0], np.ndarray)
    assert len(plot.plot_sizes[0]) == 5


def test_scatter_plot_gradient():
    """Test scatter plot with gradient colors."""
    x = [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]
    y = [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]

    plot = ScatterPlot(
        x, y,
        colors=['#FF0000', '#0000FF'],
        gradient=True
    )

    assert plot.n_plots == 3
    assert len(plot.plot_colors) == 3
    # First should be red, last should be blue
    assert plot.plot_colors[0] == '#ff0000'
    assert plot.plot_colors[2] == '#0000ff'


def test_scatter_plot_mismatched_data():
    """Test that mismatched x and y data raises error."""
    x = [np.array([1, 2]), np.array([3, 4])]
    y = [np.array([1, 2])]

    # Should broadcast y to match x
    plot = ScatterPlot(x, y)
    assert plot.n_plots == 2


def test_scatter_plot_invalid_data():
    """Test that invalid data raises appropriate error."""
    x = [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]
    y = [np.array([1, 2]), np.array([3, 4])]

    with pytest.raises(ValueError):
        ScatterPlot(x, y)


def test_scatter_plot_markers():
    """Test scatter plot with different markers."""
    x = [np.array([1, 2]), np.array([3, 4])]
    y = [np.array([1, 2]), np.array([3, 4])]

    plot = ScatterPlot(x, y, marker=['o', 's'])

    assert plot.plot_markers[0] == 'o'
    assert plot.plot_markers[1] == 's'


def test_scatter_plot_alpha():
    """Test scatter plot with custom alpha values."""
    x = np.array([1, 2, 3])
    y = np.array([1, 2, 3])

    plot = ScatterPlot(x, y, alpha=0.5)

    assert plot.plot_alphas[0] == 0.5


def test_scatter_plot_edge_properties():
    """Test scatter plot with edge colors and widths."""
    x = np.array([1, 2, 3])
    y = np.array([1, 2, 3])

    plot = ScatterPlot(
        x, y,
        edgecolors='black',
        linewidths=2.0
    )

    assert plot.plot_edgecolors[0] == 'black'
    assert plot.plot_linewidths[0] == 2.0
