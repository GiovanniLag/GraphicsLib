# Graphics Library

A simple graphics library for Python.

## Installation

This project uses [UV](https://github.com/astral-sh/uv) for dependency management.

### Prerequisites

- Python >= 3.12
- UV (install with `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/GiovanniLag/GraphicsLib.git
cd GraphicsLib
```

2. Create a virtual environment and install dependencies using UV:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. Install optional dependencies:
```bash
# For interactive Plotly plots
uv pip install -e ".[interactive]"

# For Dash-based interactive plots with click details
uv pip install -e ".[dash]"

# For development
uv pip install -e ".[dev]"
```

## Features

### Core Plotting

- **Matplotlib Backend**: Static, publication-quality plots
  - Line plots with multiple series
  - Scatter plots with point-wise control
  - Fit plots with residuals
  
- **Plotly Backend**: Interactive plots for exploration
  - Interactive scatter plots with zoom/pan
  - Advanced hover features
  - **NEW!** Dash-based scatter with click-triggered detail plots

### Color Management

- **Palette System**: Pre-defined and custom color palettes
- **Typography System**: Consistent font styling across plots
- **Color Helpers**: Interpolation, manipulation utilities

### Interactive Features (Dash)

The new `DashScatterPlot` class provides advanced click-based detail views:

- **Click Detail Plots**: Display secondary plots when clicking on points
- **Flexible Data Structures**: 
  - List (all points have details)
  - Dictionary (sparse detail data)
  - Callable (dynamic generation)
- **Multiple Plot Types**: Line, scatter, bar, histogram
- **Universal Compatibility**: Works in browser and Jupyter notebooks
- **Auto-Detection**: Automatically chooses inline (Jupyter) or browser mode
- **Auto-Port Discovery**: Finds free ports automatically

## Development

### Project Structure

```
GraphicsLib/
├── graphics_lib/          # Main package directory
│   ├── __init__.py       # Package initialization
│   └── py.typed          # PEP 561 type marker
├── tests/                # Test directory
│   ├── __init__.py
│   └── test_placeholder.py
├── .github/              # GitHub specific files
│   └── instructions/     # Coding instructions
├── pyproject.toml        # Project configuration
├── README.md             # This file
├── LICENSE               # License file
└── .gitignore           # Git ignore rules
```

### Running Tests

```bash
pytest
```

### Code Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking
- **Pytest**: Testing framework

Run all checks:
```bash
# Format code
black graphics_lib tests

# Lint code
ruff check graphics_lib tests

# Type check
mypy graphics_lib

# Run tests with coverage
pytest --cov=graphics_lib --cov-report=term-missing
```

## Usage

### Basic Scatter Plot

```python
import numpy as np
from graphics_lib.plots.plotly import ScatterPlot

# Generate data
x = np.random.rand(50)
y = np.random.rand(50)

# Create scatter plot
plot = ScatterPlot(
    x, y,
    title='My Scatter Plot',
    palette='qscience',
    colors='#FF6B6B'
)

plot.show()  # Opens in browser
plot.save('scatter.html')  # Save as interactive HTML
```

### Interactive Scatter with Click Details

```python
import numpy as np
from graphics_lib.plots.plotly import DashScatterPlot

# Generate main scatter data
n_points = 20
x = np.linspace(0, 10, n_points)
y = 2 * x + np.random.normal(0, 2, n_points)

# Create time series data for each point
time_series_data = []
for i in range(n_points):
    t = np.linspace(0, 2 * np.pi, 100)
    signal = np.sin((1 + i * 0.1) * t) * y[i]
    
    time_series_data.append({
        'x': t,
        'y': signal,
        'title': f'Time Series for Point {i}'
    })

# Create interactive plot
plot = DashScatterPlot(
    x, y,
    detail_plot_data=time_series_data,
    detail_plot_type='line',
    title='Interactive Scatter - Click Points for Details',
    palette='qscience'
)

plot.show()  # Opens Dash app (browser or Jupyter inline)
```

**Usage:**
- Click on any point to see its detail plot
- Detail plots appear alongside the main scatter
- Works in both standalone Python scripts and Jupyter notebooks
- Automatically detects environment and uses appropriate display mode

### Alternative Data Structures

**Dictionary (Sparse Data):**
```python
# Only specific points have detail data
sparse_data = {
    0: {'x': [1, 2, 3], 'y': [4, 5, 6], 'title': 'Point 0'},
    5: {'x': [1, 2, 3], 'y': [7, 8, 9], 'title': 'Point 5'},
    10: {'x': [1, 2, 3], 'y': [2, 3, 4], 'title': 'Point 10'}
}

plot = DashScatterPlot(
    x, y,
    detail_plot_data=sparse_data,
    palette='qscience'
)
```

**Callable (Dynamic Generation):**
```python
def generate_plot_data(idx):
    """Generate plot data on-demand."""
    t = np.linspace(0, 10, 50)
    return {
        'x': t,
        'y': np.sin(t * idx),
        'title': f'Dynamic Plot {idx}'
    }

plot = DashScatterPlot(
    x, y,
    detail_plot_data=generate_plot_data,
    palette='qscience'
)
```

## Examples

See the `examples/` directory for comprehensive demonstrations:

- `dash_scatter_demo.py` - Interactive scatter with all data structures
- `basic_usage.py` - Basic plotting examples
- `custom_palette.py` - Custom color palettes
- `plotly_scatter_basic.py` - Basic Plotly scatter plots
- `plotly_scatter_demo.py` - Advanced Plotly features

Run examples:
```bash
python examples/dash_scatter_demo.py
python examples/basic_usage.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Giovanni Laganà - [GitHub](https://github.com/GiovanniLag)

## Acknowledgments

- Add acknowledgments here
