"""
Interactive Plotly scatter plot examples.

This script demonstrates various ways to use the Plotly ScatterPlot
class, including:
- Single scatter plot with different colors per point
- Multiple scatter series with different markers
- Scatter plot with varying sizes
- Interactive display of plots
"""

import numpy as np

from graphics_lib.plots.plotly import ScatterPlot

# Set random seed for reproducibility
np.random.seed(42)


def example_1_point_colors():
    """
    Example 1: Scatter plot with different colors per point.

    Colors each point based on a condition - demonstrates point-wise
    color control.
    """
    print("Example 1: Interactive scatter with point-wise colors")

    # Generate random data
    x = np.random.rand(100)
    y = np.random.rand(100)

    # Assign colors based on x value
    colors = [f"#{np.random.randint(0, 256**3):06x}" for _ in range(len(x))]

    # Create interactive scatter plot
    plot = ScatterPlot(
        x, y,
        title='Interactive Scatter - Point-wise Colors',
        xlabel='Random X',
        ylabel='Random Y',
        colors=colors,
        sizes=12,
        opacity=0.7,
        palette='qscience'
    )

    # Display the interactive plot
    plot.show()
    print("  Interactive plot displayed!\n")


def example_2_multiple_markers():
    """
    Example 2: Multiple series with different markers and colors.

    Demonstrates using different marker symbols for different series
    in an interactive plot.
    """
    print("Example 2: Multiple series with different markers")

    # Generate three groups with different distributions
    x1 = np.random.randn(40)
    y1 = np.random.randn(40)

    x2 = np.random.randn(40) + 2
    y2 = np.random.randn(40) + 2

    x3 = np.random.randn(40) + 4
    y3 = np.random.randn(40) + 4

    # Create scatter plot with different markers
    plot = ScatterPlot(
        [x1, x2, x3],
        [y1, y2, y3],
        title='Interactive Scatter - Different Markers',
        xlabel='X Value',
        ylabel='Y Value',
        labels=['Circles', 'Squares', 'Triangles'],
        marker=['circle', 'square', 'triangle-up'],
        colors=['#E63946', '#457B9D', '#2A9D8F'],
        sizes=12,
        opacity=0.7,
        palette='qscience'
    )

    # Display the interactive plot
    plot.show()
    print("  Interactive plot displayed!\n")


def example_3_varying_sizes():
    """
    Example 3: Scatter plot with varying point sizes.

    Demonstrates how to use different sizes for each point in an
    interactive bubble plot.
    """
    print("Example 3: Interactive scatter with variable sizes")

    # Generate random data
    x = np.random.rand(80)
    y = np.random.rand(80)

    # Varying sizes based on distance from center
    distances = np.sqrt((x - 0.5)**2 + (y - 0.5)**2)
    sizes = (1 - distances) * 30 + 5  # Scale for Plotly

    # Create scatter plot
    plot = ScatterPlot(
        x, y,
        title='Interactive Scatter - Variable Sizes',
        xlabel='X Position',
        ylabel='Y Position',
        sizes=sizes,
        opacity=0.6,
        palette='qscience',
        marker='circle'
    )

    # Display the interactive plot
    plot.show()
    print("  Interactive plot displayed!\n")


def example_4_gradient_colors():
    """
    Example 4: Multiple series with color gradient.

    Creates multiple scatter series with a color gradient between
    specified colors.
    """
    print("Example 4: Multiple series with gradient")

    # Generate four groups
    groups = []
    for i in range(4):
        x = np.random.randn(25) + i * 1.5
        y = np.random.randn(25) + i * 0.5
        groups.append((x, y))

    x_data = [g[0] for g in groups]
    y_data = [g[1] for g in groups]

    # Create scatter plot with gradient
    plot = ScatterPlot(
        x_data,
        y_data,
        title='Interactive Scatter - Gradient Colors',
        xlabel='X Position',
        ylabel='Y Position',
        labels=[f'Group {i+1}' for i in range(4)],
        colors=['#FF0000', '#0000FF'],  # Red to Blue gradient
        gradient=True,
        sizes=10,
        opacity=0.7,
        palette='qscience'
    )

    # Display the interactive plot
    plot.show()
    print("  Interactive plot displayed!\n")


def example_5_categorical_data():
    """
    Example 5: Scatter plot with categorical colors and shapes.

    Colors and shapes points based on categorical data, useful for
    classification visualization.
    """
    print("Example 5: Categorical colors and shapes")

    # Generate random data with categories
    n_points = 150
    categories = np.random.choice([0, 1, 2], n_points)

    x = np.random.randn(n_points)
    y = np.random.randn(n_points)

    # Separate by category
    x_data = []
    y_data = []
    for cat in range(3):
        mask = categories == cat
        x_data.append(x[mask])
        y_data.append(y[mask])

    # Create scatter plot with different markers per category
    plot = ScatterPlot(
        x_data,
        y_data,
        title='Interactive Scatter - Categorical Data',
        xlabel='Feature 1',
        ylabel='Feature 2',
        labels=['Category A', 'Category B', 'Category C'],
        colors=['#E63946', '#457B9D', '#2A9D8F'],
        marker=['circle', 'square', 'diamond'],
        sizes=10,
        opacity=0.7,
        palette='qscience'
    )

    # Display the interactive plot
    plot.show()
    print("  Interactive plot displayed!\n")


def example_6_point_wise_everything():
    """
    Example 6: Advanced scatter with point-wise colors and sizes.

    Demonstrates complete control over individual point properties.
    """
    print("Example 6: Point-wise colors and sizes")

    # Generate random data
    x = np.random.rand(60)
    y = np.random.rand(60)

    # Create colors based on both x and y values
    colors = []
    for xi, yi in zip(x, y, strict=True):
        if xi > 0.5 and yi > 0.5:
            colors.append('#FF6B6B')  # Red - top right
        elif xi > 0.5:
            colors.append('#4ECDC4')  # Cyan - bottom right
        elif yi > 0.5:
            colors.append('#FFE66D')  # Yellow - top left
        else:
            colors.append('#95E1D3')  # Green - bottom left

    # Sizes based on proximity to edges
    edge_dist = np.minimum(
        np.minimum(x, 1 - x),
        np.minimum(y, 1 - y)
    )
    sizes = edge_dist * 40 + 5

    # Create scatter plot
    plot = ScatterPlot(
        x, y,
        title='Interactive Scatter - Complete Point Control',
        xlabel='X Position',
        ylabel='Y Position',
        colors=colors,
        sizes=sizes,
        opacity=0.7,
        marker='circle'
    )

    # Display the interactive plot
    plot.show()
    print("  Interactive plot displayed!\n")


def main():
    """
    Run all Plotly scatter plot examples.

    Each example will display an interactive plot in your browser.
    """
    print("=" * 60)
    print("Plotly Interactive Scatter Plot Examples")
    print("=" * 60 + "\n")

    # Run all examples
    example_1_point_colors()
    example_2_multiple_markers()
    example_3_varying_sizes()
    example_4_gradient_colors()
    example_5_categorical_data()
    example_6_point_wise_everything()

    print("=" * 60)
    print("All examples completed!")
    print("Check your browser for interactive plots.")
    print("=" * 60)


if __name__ == '__main__':
    main()
