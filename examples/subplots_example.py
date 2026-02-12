"""
Example demonstrating the use of ScatterPlot, LinePlot, and FitPlot with custom subplots.

This example shows how to use the ax parameter to create multiple plots
in a single figure with full control over the layout.
"""

import numpy as np
import matplotlib.pyplot as plt
from graphics_lib import ScatterPlot, LinePlot, FitPlot


def exponential_model(x, amplitude, decay):
    """Exponential decay model for fitting."""
    return amplitude * np.exp(-x / decay)


def main():
    """Create a figure with subplots demonstrating all three plot types."""
    # Set up the figure with 2x2 subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Example 1: Single ScatterPlot
    print("Creating scatter plot on ax1...")
    np.random.seed(42)
    x_scatter = np.random.rand(50) * 10
    y_scatter = 2 * x_scatter + np.random.randn(50) * 2
    
    ScatterPlot(
        x_scatter,
        y_scatter,
        title='Scatter Plot Example',
        xlabel='X Value',
        ylabel='Y Value',
        palette='qscience',
        ax=ax1
    )
    
    # Example 2: Multiple LinePlots
    print("Creating line plots on ax2...")
    x_line = np.linspace(0, 10, 100)
    y_lines = [
        np.sin(x_line),
        np.cos(x_line),
        np.sin(2 * x_line) * 0.5
    ]
    
    LinePlot(
        x_line,
        y_lines,
        title='Multiple Line Plots',
        xlabel='Time',
        ylabel='Amplitude',
        labels=['sin(x)', 'cos(x)', 'sin(2x)/2'],
        colors=['#FF6B6B', '#4ECDC4', '#45B7D1'],
        palette='qscience',
        ax=ax2
    )
    
    # Example 3: FitPlot (without residuals since we're using custom ax)
    print("Creating fit plot on ax3...")
    x_fit = np.linspace(0, 5, 50)
    y_fit = exponential_model(x_fit, amplitude=10, decay=2) + np.random.randn(50) * 0.5
    data = {'x': x_fit, 'y': y_fit}
    
    FitPlot(
        data=data,
        model=exponential_model,
        model_params={'amplitude': 10, 'decay': 2},
        title='Exponential Fit',
        xlabel='Time (s)',
        ylabel='Signal',
        data_label='Measured',
        model_label='Fit',
        show_residuals=False,  # Must be False when using custom ax
        palette='qscience',
        ax=ax3
    )
    
    # Example 4: Multiple Scatter series with gradient
    print("Creating multi-series scatter plot on ax4...")
    np.random.seed(123)
    x_multi = [
        np.random.randn(30) + 0,
        np.random.randn(30) + 2,
        np.random.randn(30) + 4
    ]
    y_multi = [
        np.random.randn(30) + 0,
        np.random.randn(30) + 2,
        np.random.randn(30) + 4
    ]
    
    ScatterPlot(
        x_multi,
        y_multi,
        title='Multi-Series Scatter',
        xlabel='X Coordinate',
        ylabel='Y Coordinate',
        labels=['Group A', 'Group B', 'Group C'],
        colors=['#E63946', '#457B9D'],
        gradient=True,
        alpha=0.6,
        sizes=60,
        palette='qscience',
        ax=ax4
    )
    
    # Apply tight layout to the entire figure
    print("Applying tight layout...")
    plt.tight_layout()
    
    # Save the figure
    output_path = 'examples/output/subplots_example.png'
    print(f"Saving figure to {output_path}...")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Figure saved successfully!")
    
    # Display the figure
    print("Displaying figure...")
    plt.show()
    
    print("\nExample completed successfully!")
    print(f"- All three plot types work correctly with custom axes")
    print(f"- tight_layout() was applied to the figure without conflicts")
    print(f"- Output saved to: {output_path}")


if __name__ == '__main__':
    main()
