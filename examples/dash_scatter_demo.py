"""
Demonstration of DashScatterPlot with click-triggered detail plots.

This example shows three data structures for providing detail plot data:
1. List - All points have detail data
2. Dict - Sparse detail data (only some points)
3. Callable - Dynamic detail plot generation

Run with:
    python examples/dash_scatter_demo.py
"""

import numpy as np

from graphics_lib.plots.plotly import DashScatterPlot

# Generate sample data
np.random.seed(42)
n_points = 20
x = np.linspace(0, 10, n_points)
y = 2 * x + 1 + np.random.normal(0, 2, n_points)


# Example 1: List data structure - All points have time series detail
print("=" * 60)
print("Example 1: List data structure (all points)")
print("=" * 60)

# Create time series data for each point
detail_data_list = []
for i in range(n_points):
    t = np.linspace(0, 2 * np.pi, 100)
    # Different frequency for each point
    freq = 1 + i * 0.1
    signal = np.sin(freq * t) * y[i]
    detail_data_list.append({
        'x': t,
        'y': signal,
        'title': f'Time Series for Point {i} (freq={freq:.1f})'
    })

plot1 = DashScatterPlot(
    x=x,
    y=y,
    detail_plot_data=detail_data_list,
    detail_plot_type='line',
    title='Interactive Scatter - Click to View Time Series',
    xlabel='X Value',
    ylabel='Y Value',
    figsize=(800, 600),
    detail_figsize=(600, 400)
)

print("Click on any point to see its time series detail plot")
plot1.show()


# Example 2: Dict data structure - Sparse detail data
print("\n" + "=" * 60)
print("Example 2: Dict data structure (sparse data)")
print("=" * 60)

# Only provide detail for points at indices 0, 5, 10, 15
detail_data_dict = {}
for i in [0, 5, 10, 15]:
    histogram_data = np.random.normal(y[i], 1, 1000)
    detail_data_dict[i] = {
        'x': None,  # Not used for histogram
        'y': histogram_data,
        'title': f'Distribution Around Point {i}'
    }

plot2 = DashScatterPlot(
    x=x,
    y=y,
    detail_plot_data=detail_data_dict,
    detail_plot_type='histogram',
    title='Sparse Detail Data - Only Some Points Have Details',
    xlabel='X Value',
    ylabel='Y Value',
    figsize=(800, 600),
    detail_figsize=(600, 400)
)

print("Only points 0, 5, 10, 15 have detail data")
print("Click on these points to see histograms")
plot2.show()


# Example 3: Callable data structure - Dynamic generation
print("\n" + "=" * 60)
print("Example 3: Callable data structure (dynamic)")
print("=" * 60)


def generate_detail_plot(index):
    """Dynamically generate detail plot based on point properties."""
    # Generate different waveforms based on point index
    t = np.linspace(0, 4 * np.pi, 200)
    
    if index % 3 == 0:
        # Sine wave
        wave = np.sin(t) * y[index]
        title = f'Sine Wave for Point {index}'
    elif index % 3 == 1:
        # Square wave
        wave = np.sign(np.sin(t)) * y[index]
        title = f'Square Wave for Point {index}'
    else:
        # Sawtooth wave
        wave = (t % (2 * np.pi) - np.pi) / np.pi * y[index]
        title = f'Sawtooth Wave for Point {index}'
    
    return {
        'x': t,
        'y': wave,
        'title': title
    }


plot3 = DashScatterPlot(
    x=x,
    y=y,
    detail_plot_data=generate_detail_plot,
    detail_plot_type='line',
    title='Dynamic Detail Generation - Different Waveforms',
    xlabel='X Value',
    ylabel='Y Value',
    figsize=(800, 600),
    detail_figsize=(600, 400)
)

print("Click any point to see dynamically generated waveforms")
print("Sine (index%3==0), Square (index%3==1), Sawtooth (index%3==2)")
plot3.show()


# Example 4: Multiple series with bar chart details
print("\n" + "=" * 60)
print("Example 4: Multiple series with bar charts")
print("=" * 60)

# Create two series
x1 = np.linspace(0, 10, 10)
y1 = 2 * x1 + np.random.normal(0, 1, 10)
x2 = np.linspace(0, 10, 10)
y2 = -x2 + 5 + np.random.normal(0, 1, 10)

x_combined = np.concatenate([x1, x2])
y_combined = np.concatenate([y1, y2])
labels = ['Series A'] * len(x1) + ['Series B'] * len(x2)

# Bar chart data for each point
bar_data = []
for i in range(len(x_combined)):
    categories = ['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4']
    values = np.abs(np.random.normal(y_combined[i], 2, 4))
    bar_data.append({
        'x': categories,
        'y': values,
        'title': f'Categories for Point {i} ({labels[i]})'
    })

plot4 = DashScatterPlot(
    x=x_combined,
    y=y_combined,
    detail_plot_data=bar_data,
    detail_plot_type='bar',
    title='Two Series with Bar Chart Details',
    xlabel='X Value',
    ylabel='Y Value',
    labels=labels,
    figsize=(800, 600),
    detail_figsize=(600, 400),
    show_legend=True
)

print("Click any point to see categorical bar chart")
plot4.show()

print("\n" + "=" * 60)
print("All examples completed!")
print("=" * 60)
