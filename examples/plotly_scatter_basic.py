"""
Simple Plotly scatter plot example.

This example demonstrates basic usage of the interactive Plotly
scatter plot with different colors, sizes, and marker shapes.
"""

import numpy as np

from graphics_lib.plots.plotly import ScatterPlot

# Set random seed for reproducibility
np.random.seed(42)


def main():
    """Create and display a simple interactive scatter plot."""
    print("Creating interactive scatter plot...")

    # Generate sample data - three groups
    group1_x = np.random.randn(30) + 0
    group1_y = np.random.randn(30) + 0

    group2_x = np.random.randn(30) + 3
    group2_y = np.random.randn(30) + 2

    group3_x = np.random.randn(30) + 1.5
    group3_y = np.random.randn(30) + 4

    # Create interactive scatter plot with different markers and colors
    plot = ScatterPlot(
        x=[group1_x, group2_x, group3_x],
        y=[group1_y, group2_y, group3_y],
        title='Interactive Scatter Plot Demo',
        xlabel='X Coordinate',
        ylabel='Y Coordinate',
        labels=['Dataset A', 'Dataset B', 'Dataset C'],
        colors=['#FF6B6B', '#4ECDC4', '#45B7D1'],
        marker=['circle', 'square', 'diamond'],
        sizes=12,
        opacity=0.7,
        palette='qscience'
    )

    # Display the interactive plot in browser
    plot.show()
    print("Interactive plot displayed in browser!")


if __name__ == '__main__':
    main()
