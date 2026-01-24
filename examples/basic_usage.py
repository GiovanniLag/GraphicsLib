"""
Basic usage examples for GraphicsLib.

This script demonstrates the basic functionality of GraphicsLib,
including creating plots with string shortcuts for palettes and
typography.
"""

import numpy as np
from graphics_lib import FitPlot, LinePlot
from pathlib import Path

# Create output directory
OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)


def example_fit_plot():
    """
    Example: Creating a fit plot with string shortcuts.
    """
    print("Example 1: Fit Plot with String Shortcuts")
    print("-" * 50)

    # Generate sample data
    x = np.linspace(0, 10, 100)
    y = 3 * np.exp(-x / 2) + np.random.normal(0, 0.1, 100)
    data = {'x': x, 'y': y}

    # Define model
    def exp_model(x, amplitude, tau):
        return amplitude * np.exp(-x / tau)

    # Create plot using string shortcuts
    plot = FitPlot(
        data=data,
        model=exp_model,
        model_params={'amplitude': 3, 'tau': 2},
        palette='qscience',      # String shortcut!
        typography='qscience',   # String shortcut!
        title='Exponential Decay',
        xlabel='Time (s)',
        ylabel='Signal (V)'
    )

    # Save and display
    plot.save(OUTPUT_DIR / 'fit_plot_example.png')
    print("✓ Fit plot created and saved to 'fit_plot_example.png'")
    print()


def example_line_plot_single():
    """
    Example: Creating a single line plot.
    """
    print("Example 2: Single Line Plot")
    print("-" * 50)

    # Generate sample data
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    # Create plot
    plot = LinePlot(
        x, y,
        title='Sine Wave',
        xlabel='x',
        ylabel='sin(x)',
        palette='qscience',
        typography='qscience',
        labels='sin(x)'
    )

    plot.save(OUTPUT_DIR / 'line_plot_single.png')
    print("✓ Single line plot created and saved to 'line_plot_single.png'")
    print()


def example_line_plot_multiple():
    """
    Example: Creating multiple line plots with gradient colors.
    """
    print("Example 3: Multiple Line Plots with Gradient")
    print("-" * 50)

    # Generate sample data
    x = np.linspace(0, 2 * np.pi, 100)
    y_list = [
        np.sin(x),
        np.sin(2 * x),
        np.sin(3 * x)
    ]

    # Create plot with gradient colors
    plot = LinePlot(
        x, y_list,
        title='Sine Waves with Different Frequencies',
        xlabel='x',
        ylabel='y',
        palette='qscience',
        typography='qscience',
        labels=['sin(x)', 'sin(2x)', 'sin(3x)'],
        colors=['#FF0000', '#0000FF'],  # Red to Blue gradient
        gradient=True
    )

    plot.save(OUTPUT_DIR / 'line_plot_multiple.png')
    print("✓ Multiple line plots created and saved to 'line_plot_multiple.png'")
    print()


def example_explicit_palette():
    """
    Example: Using explicit Palette and Typography objects.
    """
    print("Example 4: Explicit Palette and Typography Objects")
    print("-" * 50)

    from graphics_lib import QSciencePalette, QScienceTypography

    # Generate sample data
    x = np.linspace(0, 10, 100)
    y = np.cos(x) * np.exp(-x / 5)

    # Create plot with explicit objects
    plot = LinePlot(
        x, y,
        title='Damped Cosine',
        xlabel='Time',
        ylabel='Amplitude',
        palette=QSciencePalette,      # Explicit object
        typography=QScienceTypography  # Explicit object
    )

    plot.save(OUTPUT_DIR / 'line_plot_explicit.png')
    print("✓ Plot with explicit objects created and saved to 'line_plot_explicit.png'")
    print()


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("GraphicsLib Basic Usage Examples")
    print("=" * 50 + "\n")

    example_fit_plot()
    example_line_plot_single()
    example_line_plot_multiple()
    example_explicit_palette()

    print("=" * 50)
    print("All examples completed successfully!")
    print("=" * 50)
