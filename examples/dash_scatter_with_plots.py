"""
Demonstration of DashScatterPlot using actual plot objects as detail views.

This example shows how to use plots from the library (both matplotlib and plotly)
as detail plots when clicking on scatter points.

Run with:
    python examples/dash_scatter_with_plots.py
"""

import numpy as np
import plotly.graph_objects as go

from graphics_lib.plots.plotly import DashScatterPlot
from graphics_lib.plots.matplotlib.line import LinePlot
from graphics_lib.plots.matplotlib.fit import FitPlot

# Generate sample data
np.random.seed(42)
n_points = 15
x = np.linspace(0, 10, n_points)
y = 2 * x + 1 + np.random.normal(0, 2, n_points)


# Example 1: Using matplotlib LinePlot objects
print("=" * 60)
print("Example 1: Matplotlib LinePlot as detail views")
print("=" * 60)


def create_line_plot(index):
    """Create a matplotlib LinePlot for each point."""
    t = np.linspace(0, 2 * np.pi, 100)
    freq = 1 + index * 0.2
    signal = np.sin(freq * t) * y[index]
    
    # Create a LinePlot from the library
    plot = LinePlot(
        x=t,
        y=signal,
        title=f'Time Series for Point {index}',
        palette='qscience',
        xlabel='Time',
        ylabel='Amplitude'
    )
    
    # Return the plot object itself
    return plot


plot1 = DashScatterPlot(
    x=x,
    y=y,
    detail_plot_data=create_line_plot,
    title='Click Points to See Matplotlib Line Plots',
    palette='qscience',
    xlabel='X Value',
    ylabel='Y Value',
    figsize=(800, 600),
    detail_figsize=(600, 400)
)

print("Click on any point to see a matplotlib LinePlot")
plot1.show()


# Example 2: Using matplotlib FitPlot objects
print("\n" + "=" * 60)
print("Example 2: Matplotlib FitPlot as detail views")
print("=" * 60)


def create_fit_plot(index):
    """Create a matplotlib FitPlot for each point."""
    # Generate some data with noise
    x_data = np.linspace(0, 5, 50)
    y_true = 2 * x_data + y[index]
    y_noisy = y_true + np.random.normal(0, 1, 50)
    
    # Create a FitPlot from the library
    plot = FitPlot(
        x=x_data,
        y=y_noisy,
        fit_type='linear',
        title=f'Linear Fit for Point {index}',
        palette='qscience',
        show_residuals=True
    )
    
    return plot


plot2 = DashScatterPlot(
    x=x,
    y=y,
    detail_plot_data=create_fit_plot,
    title='Click Points to See Fit Plots with Residuals',
    palette='qscience',
    xlabel='X Value',
    ylabel='Y Value',
    figsize=(800, 600),
    detail_figsize=(700, 500)
)

print("Click on any point to see a FitPlot with residuals")
plot2.show()


# Example 3: Using Plotly Figure objects directly
print("\n" + "=" * 60)
print("Example 3: Direct Plotly Figure objects")
print("=" * 60)


def create_plotly_figure(index):
    """Create a custom Plotly figure."""
    # Create a 3D scatter plot
    t = np.linspace(0, 4 * np.pi, 100)
    x_3d = np.sin(t) * (1 + index * 0.1)
    y_3d = np.cos(t) * (1 + index * 0.1)
    z_3d = t
    
    fig = go.Figure(data=[go.Scatter3d(
        x=x_3d,
        y=y_3d,
        z=z_3d,
        mode='lines',
        line=dict(
            color=z_3d,
            colorscale='Viridis',
            width=4
        )
    )])
    
    fig.update_layout(
        title=f'3D Helix for Point {index}',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        width=600,
        height=500
    )
    
    return fig


plot3 = DashScatterPlot(
    x=x,
    y=y,
    detail_plot_data=create_plotly_figure,
    title='Click Points to See 3D Plotly Visualizations',
    palette='qscience',
    xlabel='X Value',
    ylabel='Y Value',
    figsize=(800, 600),
    detail_figsize=(600, 500)
)

print("Click on any point to see a 3D Plotly figure")
plot3.show()


# Example 4: Mixed approach - dict with 'figure' key
print("\n" + "=" * 60)
print("Example 4: Mixed data structures")
print("=" * 60)


def create_mixed_detail(index):
    """Return different types based on index."""
    if index % 3 == 0:
        # Return a matplotlib plot object
        t = np.linspace(0, 10, 50)
        signal = np.exp(-t / 5) * np.cos(2 * np.pi * t)
        plot = LinePlot(
            x=t,
            y=signal,
            title=f'Damped Oscillation (Point {index})',
            palette='qscience'
        )
        return plot
    elif index % 3 == 1:
        # Return a Plotly figure in a dict
        categories = ['A', 'B', 'C', 'D', 'E']
        values = np.random.randint(10, 100, 5) + index * 5
        fig = go.Figure(data=[go.Bar(x=categories, y=values)])
        fig.update_layout(title=f'Bar Chart for Point {index}')
        return {'figure': fig}
    else:
        # Return traditional x/y data dict
        t = np.linspace(0, 2 * np.pi, 100)
        wave = np.sin(t * (index + 1))
        return {
            'x': t,
            'y': wave,
            'title': f'Sine Wave for Point {index}'
        }


plot4 = DashScatterPlot(
    x=x,
    y=y,
    detail_plot_data=create_mixed_detail,
    title='Mixed Detail Types - Matplotlib, Plotly, and Data',
    palette='qscience',
    xlabel='X Value',
    ylabel='Y Value',
    figsize=(800, 600),
    detail_figsize=(600, 400)
)

print("Click points to see different detail types:")
print("- Indices divisible by 3: Matplotlib LinePlot")
print("- Indices with remainder 1: Plotly bar chart")
print("- Indices with remainder 2: Simple line from data")
plot4.show()


print("\n" + "=" * 60)
print("All examples completed!")
print("=" * 60)
