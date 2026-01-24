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

3. Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

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

```python
import graphics_lib

# Add your usage examples here once implemented
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
