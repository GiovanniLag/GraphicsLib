# GraphicsLib Reorganization - Implementation Complete

## Overview

GraphicsLib has been successfully reorganized with a modular, extensible architecture that supports multiple rendering backends (matplotlib and Plotly) and provides intuitive string shortcuts for palettes and typography.

## New Structure

```
graphics_lib/
├── core/
│   ├── __init__.py
│   ├── base.py              # BasePlot abstract class
│   └── registry.py          # Registry system for palettes/typography
├── backends/
│   ├── __init__.py
│   ├── matplotlib.py        # MatplotlibPlot base class
│   └── plotly.py            # PlotlyPlot base class
├── plots/
│   ├── __init__.py
│   ├── matplotlib/
│   │   ├── __init__.py
│   │   ├── fit.py           # FitPlot class
│   │   └── line.py          # LinePlot class
│   └── plotly/
│       └── __init__.py      # (placeholder for future interactive plots)
├── utils/
│   ├── __init__.py
│   └── color_helpers.py     # Color utilities
├── __init__.py              # Public API
├── colours.py               # (unchanged)
├── typography.py            # (updated with registry)
└── palettes.py              # (new clean version with examples)

examples/
├── README.md
├── basic_usage.py           # Basic examples with string shortcuts
└── custom_palette.py        # Custom palette/typography registration
```

## Key Features Implemented

### 1. **Abstract Base Classes**
- `BasePlot`: Common interface for all plot types
  - `_render()`: Abstract method for plot-specific rendering
  - `save()`: Abstract method for saving plots
  - `show()`: Abstract method for displaying plots
  - `_resolve_palette()`: Converts string shortcuts to Palette objects
  - `_resolve_typography()`: Converts string shortcuts to Typography objects

### 2. **Backend-Specific Classes**
- `MatplotlibPlot`: Base class for matplotlib-based plots
  - Handles figure/axes creation
  - Implements matplotlib-specific `save()` and `show()`
  - Provides `_apply_typography()` for consistent styling

- `PlotlyPlot`: Base class for Plotly-based plots
  - Handles Plotly figure creation
  - Implements Plotly-specific `save()` (HTML and static images)
  - Provides `_apply_typography()` for Plotly layouts
  - Ready for interactive plot implementations

### 3. **Registry System**
- `PaletteRegistry`: Stores named palettes for string shortcuts
- `TypographyRegistry`: Stores named typography sets
- `PlotRegistry`: Stores plot types for factory functions
- Features:
  - `register()`: Add new items
  - `get()`: Retrieve by name
  - `list_available()`: Discover registered items
  - `unregister()`, `clear()`: Management methods

### 4. **Concrete Plot Classes**

#### FitPlot (matplotlib)
- Model fitting visualization with residuals
- Constructor parameters:
  - `data`: dict or array
  - `model`: Callable model function
  - `model_params`: dict of parameters
  - `palette`: string or Palette object
  - `typography`: string or Typography object
  - `show_residuals`: bool (default True)
  - And many more customization options

#### LinePlot (matplotlib)
- Single or multiple line plots
- Constructor parameters:
  - `x`, `y`: data arrays or lists of arrays
  - `palette`, `typography`: string shortcuts or objects
  - `labels`: single or list of labels
  - `colors`: single or list of colors
  - `gradient`: bool for color interpolation
  - And more customization options

### 5. **Utility Functions**
- `get_plot_colors()`: Extract colors from palette in priority order
- `interpolate_colors()`: Generate color gradients

### 6. **Example Palettes and Typography**
- `QSciencePalette`: Quantum science theme (auto-registered as 'qscience')
- `QScienceTypography`: Matching typography (auto-registered as 'qscience')
- `create_simple_palette()`: Helper for creating simple palettes from color strings

## Usage Examples

### Basic Usage with String Shortcuts

```python
from graphics_lib import FitPlot
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y = 3 * np.exp(-x/2) + np.random.normal(0, 0.1, 100)
data = {'x': x, 'y': y}

# Define model
def exp_model(x, amplitude, tau):
    return amplitude * np.exp(-x/tau)

# Create plot with string shortcuts
plot = FitPlot(
    data=data,
    model=exp_model,
    model_params={'amplitude': 3, 'tau': 2},
    palette='qscience',      # String shortcut!
    typography='qscience',   # String shortcut!
    title='Exponential Decay'
)

plot.show()
plot.save('decay.png')
```

### Custom Palette Registration

```python
from graphics_lib import Palette, Colour, PaletteRegistry, LinePlot
import numpy as np

# Create custom palette
my_palette = Palette(
    "Ocean Theme",
    {
        'primary': Colour("#006994"),
        'secondary': Colour("#52B2CF"),
        'accent': Colour("#FFD700"),
        'background': Colour("#F0F8FF"),
        'text_primary': Colour("#003D5C")
    }
)

# Register it
PaletteRegistry.register('ocean', my_palette)

# Use it with string shortcut
x = np.linspace(0, 2*np.pi, 100)
plot = LinePlot(x, np.sin(x), palette='ocean', title='Wave')
plot.show()
```

### Multiple Lines with Gradient

```python
from graphics_lib import LinePlot
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y_list = [np.sin(x), np.sin(2*x), np.sin(3*x)]

plot = LinePlot(
    x, y_list,
    title='Sine Waves',
    palette='qscience',
    labels=['sin(x)', 'sin(2x)', 'sin(3x)'],
    colors=['#FF0000', '#0000FF'],  # Red to Blue
    gradient=True                    # Interpolate colors
)
plot.show()
```

## Backward Compatibility

Legacy function-based API is still available but deprecated:

```python
from graphics_lib import plot_fit, plot

# Will show deprecation warning
fig, axes = plot_fit(data, model, model_params, palette='qscience')
plot(x, y, palette='qscience')
```

Users are encouraged to migrate to the class-based API.

## Dependencies

### Required
- `numpy>=1.24.0`
- `matplotlib>=3.7.0`

### Optional
- `plotly>=5.0.0` - For interactive plots (install with `pip install graphics-lib[interactive]`)
- `kaleido>=0.2.0` - For Plotly static image export

## Design Patterns Used

1. **Strategy Pattern**: Switchable backends (matplotlib/Plotly)
2. **Registry Pattern**: String-based lookup for palettes/typography
3. **Template Method Pattern**: BasePlot defines skeleton, subclasses implement details
4. **Factory Pattern**: Ready for factory functions using PlotRegistry
5. **Facade Pattern**: Simple high-level API hiding complexity

## Benefits of New Architecture

1. **Extensibility**: Easy to add new plot types by inheriting from backend classes
2. **Separation of Concerns**: Core logic, backends, and plots are clearly separated
3. **Type Safety**: Modern Python 3.12+ type annotations throughout
4. **User-Friendly**: String shortcuts eliminate boilerplate
5. **Backend Flexibility**: Same plot types can be implemented in different backends
6. **Consistent Styling**: Palette and typography integrate seamlessly across all plots
7. **Maintainability**: Modular structure makes code easier to understand and modify

## Future Enhancements

1. **Plotly Implementations**: Add interactive versions of FitPlot, LinePlot, etc.
2. **More Plot Types**: Scatter, histogram, heatmap, etc.
3. **Plot Factory**: Convenience functions using PlotRegistry
4. **Context Manager**: `with PlotContext(palette='qscience'):` for default styling
5. **Theme System**: Complete theme packages combining palette and typography
6. **Export Utilities**: Batch export, format conversion
7. **Animation Support**: Time-series and animated plots

## Migration Guide for Existing Code

### Old Code
```python
from graphics_lib.plots import plot_fit
fig, axes = plot_fit(data, model, params, palette=my_palette, ...)
```

### New Code
```python
from graphics_lib import FitPlot
plot = FitPlot(data, model, params, palette='qscience', ...)
plot.show()
# or
plot.save('output.png')
```

## Testing

Run the examples to verify the implementation:
```bash
python examples/basic_usage.py
python examples/custom_palette.py
```

## Notes

- All type annotations use modern Python 3.12+ syntax (`|` instead of `Union`, etc.)
- Import ordering follows PEP 8 and ruff standards
- Docstrings follow NumPy style as per project conventions
- Some linting warnings remain (mostly about TYPE_CHECKING forward references) but don't affect functionality

## Conclusion

The reorganization is complete and fully functional. The library now has a solid foundation for future growth while maintaining backward compatibility with existing code. Users can take advantage of the new string shortcut system immediately, and the modular architecture makes it easy to add new backends and plot types.
