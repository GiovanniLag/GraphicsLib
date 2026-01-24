"""
Example usage of ScatterPlot with different coloring strategies.

This script demonstrates various ways to use the ScatterPlot class,
including:
- Single scatter plot with uniform colors
- Scatter plot with different colors per point
- Multiple scatter series with gradient
- Scatter plot with varying sizes
"""

import numpy as np

from graphics_lib.plots import ScatterPlot

# Set random seed for reproducibility
np.random.seed(42)


def example_1_uniform_colors():
    """
    Example 1: Single scatter plot with uniform colors.

    Creates a simple scatter plot with all points having the same color
    from the palette.
    """
    print("Example 1: Uniform colors")

    # Generate random data
    x = np.random.rand(50)
    y = np.random.rand(50)

    # Create scatter plot
    plot = ScatterPlot(
        x, y,
        title='Scatter Plot - Uniform Colors',
        xlabel='Random X',
        ylabel='Random Y',
        palette='qscience',
        sizes=100,
        alpha=0.6
    )

    # Save the plot
    plot.save('examples/output/scatter_uniform.png')
    print("  Saved to: examples/output/scatter_uniform.png\n")


def example_2_point_colors():
    """
    Example 2: Scatter plot with different colors per point.

    Colors each point based on a condition - demonstrates point-wise
    color control.
    """
    print("Example 2: Different colors per point")

    # Generate random data
    x = np.random.rand(100)
    y = np.random.rand(100)

    # Assign random colors for each point
    colors = [f"#{np.random.randint(0, 256**3):06x}" for _ in range(len(x))]

    # Create scatter plot
    plot = ScatterPlot(
        x, y,
        title='Scatter Plot - Point-wise Colors',
        xlabel='Random X',
        ylabel='Random Y',
        colors=colors,
        sizes=80,
        alpha=0.7,
        edgecolors='black',
        linewidths=0.5
    )

    # Save the plot
    plot.save('examples/output/scatter_point_colors.png')
    print("  Saved to: examples/output/scatter_point_colors.png\n")


def example_3_multiple_series():
    """
    Example 3: Multiple scatter series with gradient.

    Creates multiple scatter series with a color gradient between
    specified colors.
    """
    print("Example 3: Multiple series with gradient")

    # Generate three groups of random data
    x1 = np.random.randn(30) + 0
    y1 = np.random.randn(30) + 0

    x2 = np.random.randn(30) + 2
    y2 = np.random.randn(30) + 2

    x3 = np.random.randn(30) + 4
    y3 = np.random.randn(30) + 4

    # Create scatter plot with multiple series
    plot = ScatterPlot(
        [x1, x2, x3],
        [y1, y2, y3],
        title='Multiple Scatter Series with Gradient',
        xlabel='X Position',
        ylabel='Y Position',
        labels=['Group A', 'Group B', 'Group C'],
        colors=['#FF0000', '#0000FF'],  # Red to Blue gradient
        gradient=True,
        sizes=100,
        alpha=0.6,
        palette='qscience'
    )

    # Save the plot
    plot.save('examples/output/scatter_multiple_series.png')
    print("  Saved to: examples/output/scatter_multiple_series.png\n")


def example_4_varying_sizes():
    """
    Example 4: Scatter plot with varying point sizes.

    Demonstrates how to use different sizes for each point, useful
    for bubble plots.
    """
    print("Example 4: Varying point sizes")

    # Generate random data
    x = np.random.rand(100)
    y = np.random.rand(100)

    # Varying sizes based on distance from center
    distances = np.sqrt((x - 0.5)**2 + (y - 0.5)**2)
    sizes = (1 - distances) * 500  # Larger points closer to center

    # Create scatter plot
    plot = ScatterPlot(
        x, y,
        title='Scatter Plot - Variable Sizes',
        xlabel='X Position',
        ylabel='Y Position',
        sizes=sizes,
        alpha=0.5,
        palette='qscience',
        edgecolors='black',
        linewidths=0.5
    )

    # Save the plot
    plot.save('examples/output/scatter_variable_sizes.png')
    print("  Saved to: examples/output/scatter_variable_sizes.png\n")


def example_5_categorical_colors():
    """
    Example 5: Scatter plot with categorical colors.

    Colors points based on categorical data, useful for
    classification visualization.
    """
    print("Example 5: Categorical colors")

    # Generate random data with categories
    n_points = 150
    categories = np.random.choice(['A', 'B', 'C'], n_points)

    x = np.random.randn(n_points)
    y = np.random.randn(n_points)

    # Define color mapping
    color_map = {
        'A': '#E63946',  # Red
        'B': '#457B9D',  # Blue
        'C': '#2A9D8F'   # Green
    }

    # Assign colors based on category
    colors = [color_map[cat] for cat in categories]

    # Create scatter plot
    plot = ScatterPlot(
        x, y,
        title='Scatter Plot - Categorical Colors',
        xlabel='Feature 1',
        ylabel='Feature 2',
        colors=colors,
        sizes=100,
        alpha=0.7,
        edgecolors='white',
        linewidths=1.0
    )

    # Save the plot
    plot.save('examples/output/scatter_categorical.png')
    print("  Saved to: examples/output/scatter_categorical.png\n")


def example_6_different_markers():
    """
    Example 6: Multiple series with different markers.

    Demonstrates using different marker styles for different series.
    """
    print("Example 6: Different markers")

    # Generate three groups with different distributions
    x1 = np.random.randn(40)
    y1 = np.random.randn(40)

    x2 = np.random.randn(40) + 1.5
    y2 = np.random.randn(40) + 1.5

    x3 = np.random.randn(40) + 3
    y3 = np.random.randn(40) + 3

    # Create scatter plot with different markers
    plot = ScatterPlot(
        [x1, x2, x3],
        [y1, y2, y3],
        title='Scatter Plot - Different Markers',
        xlabel='X Value',
        ylabel='Y Value',
        labels=['Circles', 'Squares', 'Triangles'],
        marker=['o', 's', '^'],  # Circle, square, triangle
        colors=['#E63946', '#457B9D', '#2A9D8F'],
        sizes=120,
        alpha=0.6,
        edgecolors='black',
        linewidths=1.0,
        palette='qscience'
    )

    # Save the plot
    plot.save('examples/output/scatter_different_markers.png')
    print("  Saved to: examples/output/scatter_different_markers.png\n")


def main():
    """Run all scatter plot examples."""
    print("=" * 60)
    print("Scatter Plot Examples")
    print("=" * 60 + "\n")

    # Run all examples
    example_1_uniform_colors()
    example_2_point_colors()
    example_3_multiple_series()
    example_4_varying_sizes()
    example_5_categorical_colors()
    example_6_different_markers()

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
