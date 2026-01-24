"""
Quick demonstration of ScatterPlot with different point colors.

This script shows the main feature: creating scatter plots where
individual points can have different colors.
"""

import numpy as np

from graphics_lib.plots import ScatterPlot

# Set random seed for reproducibility
np.random.seed(123)


def main():
    """
    Demonstrate scatter plot with point-wise color control.

    This example creates a scatter plot where points are colored
    based on their distance from the center, showcasing the ability
    to assign different colors to different points.
    """
    # Generate random points
    n_points = 200
    x = np.random.randn(n_points)
    y = np.random.randn(n_points)

    # Calculate distance from origin for each point
    distances = np.sqrt(x**2 + y**2)

    # Create color mapping based on distance
    # Close points (< 1.0) = Blue, Medium (1.0-2.0) = Green, Far (> 2.0) = Red
    colors = []
    for dist in distances:
        if dist < 1.0:
            colors.append('#3498db')  # Blue
        elif dist < 2.0:
            colors.append('#2ecc71')  # Green
        else:
            colors.append('#e74c3c')  # Red

    # Create scatter plot with point-wise colors
    plot = ScatterPlot(
        x, y,
        title='Scatter Plot - Points Colored by Distance from Origin',
        xlabel='X Coordinate',
        ylabel='Y Coordinate',
        colors=colors,
        sizes=80,
        alpha=0.6,
        edgecolors='black',
        linewidths=0.3,
        palette='qscience'
    )

    # Save and display
    plot.save('examples/output/scatter_demo.png')
    print("Scatter plot created successfully!")
    print("Saved to: examples/output/scatter_demo.png")
    print("\nFeatures demonstrated:")
    print("  ✓ Different colors for different points")
    print("  ✓ Colors based on data properties (distance)")
    print("  ✓ Customizable marker sizes and edge properties")


if __name__ == '__main__':
    main()
