# Examples

This directory contains example scripts demonstrating how to use GraphicsLib.

## Files

### `basic_usage.py`
Demonstrates the basic functionality of GraphicsLib:
- Creating fit plots with string shortcuts
- Single and multiple line plots
- Using gradient colors
- Explicit palette and typography objects

Run with:
```bash
python examples/basic_usage.py
```

### `custom_palette.py`
Shows how to create and register custom palettes and typography:
- Creating custom palettes from colors
- Creating palettes from color strings
- Registering custom typography sets
- Using custom styles in plots
- Palette visualization and saving
- Color manipulation features

Run with:
```bash
python examples/custom_palette.py
```

### `scatter_demo.py`
Quick demonstration of ScatterPlot with different point colors:
- Creating scatter plots with point-wise color control
- Coloring points based on data properties
- Customizable marker sizes and edge properties

Run with:
```bash
python examples/scatter_demo.py
```

### `scatter_usage.py`
Comprehensive examples of ScatterPlot functionality:
- Uniform colors for all points
- Different colors per point
- Multiple scatter series with gradient
- Varying point sizes (bubble plots)
- Categorical colors
- Different markers for different series

Run with:
```bash
python examples/scatter_usage.py
```

### `plotly_scatter_basic.py`
Basic Plotly interactive scatter plot examples:
- Single scatter plot with uniform colors
- Point-wise color control
- Multiple scatter series with different markers
- Interactive features (zoom, pan, hover)

Run with:
```bash
python examples/plotly_scatter_basic.py
```

### `plotly_scatter_demo.py`
Advanced Plotly scatter plot demonstrations:
- Point-wise colors and sizes
- Multiple series with gradients
- Categorical data visualization
- Complex styling options

Run with:
```bash
python examples/plotly_scatter_demo.py
```

### `dash_scatter_demo.py`
**NEW!** Advanced interactive scatter plots with click-triggered detail plots:
- List data structure (all points have details)
- Dictionary data structure (sparse detail data)
- Callable data structure (dynamic generation)
- Multiple series with different detail plot types
- Works in both browser and Jupyter notebooks
- Auto-detects environment and uses appropriate display mode

**Requirements:**
```bash
pip install graphics-lib[dash]
```

Run with:
```bash
python examples/dash_scatter_demo.py
```

For Jupyter notebooks:
```python
from graphics_lib.plots.plotly import DashScatterPlot
# ... create plot ...
plot.show()  # Automatically displays inline
```

### `dash_scatter_with_plots.py`
**NEW!** Using actual plot objects from the library as detail views:
- Matplotlib LinePlot objects as details
- Matplotlib FitPlot objects with residuals
- Direct Plotly Figure objects (including 3D plots)
- Mixed approach with different plot types per point
- Demonstrates automatic matplotlib-to-plotly conversion

**Requirements:**
```bash
pip install graphics-lib[dash]
```

Run with:
```bash
python examples/dash_scatter_with_plots.py
```

## Output

The example scripts will generate several image files demonstrating different plot types and styling options:
- `fit_plot_example.png` - Model fit with residuals
- `line_plot_single.png` - Single line plot
- `line_plot_multiple.png` - Multiple lines with gradient colors
- `line_plot_explicit.png` - Plot with explicit objects
- `custom_style_plot.png` - Plot with custom palette and typography
- `ocean_palette.png` - Visualization of custom palette
- `ocean_palette.json` - Saved palette data
- `scatter_demo.png` - Scatter plot with distance-based coloring
- `scatter_uniform.png` - Scatter plot with uniform colors
- `scatter_point_colors.png` - Scatter plot with point-wise colors
- `scatter_multiple_series.png` - Multiple scatter series
- `scatter_variable_sizes.png` - Scatter plot with varying sizes
- `scatter_categorical.png` - Scatter plot with categorical colors
- `scatter_different_markers.png` - Scatter plot with different markers
