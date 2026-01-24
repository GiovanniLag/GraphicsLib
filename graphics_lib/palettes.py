"""
Predefined color palettes for GraphicsLib.

This module provides example palettes that can be used out of the box
and demonstrates how to register palettes for use with string shortcuts.
"""

from graphics_lib.colours import Colour, Palette
from graphics_lib.core.registry import PaletteRegistry


# Example Palette: Quantum Science
QSciencePalette = Palette(
    "Quantum Science",
    {
        'primary': Colour("#046A3A"),
        'secondary': Colour("#2A9D8F"),
        'accent': Colour("#E9C46A"),
        'accent2': Colour("#F4A261"),
        'background': Colour("#F5F5F5"),
        'background2': Colour("#FFFFFF"),
        'text_primary': Colour("#1C1C1C"),
        'text_secondary': Colour("#3E3E3E"),
        'text_accent': Colour("#046A3A"),
        'neutral_dark': Colour("#264653"),
        'neutral_light': Colour("#F5F5F5"),
        'status_success': Colour("#2A9D8F"),
        'status_warning': Colour("#F4A261"),
        'status_error': Colour("#E76F51"),
        'status_info': Colour("#46B5D1")
    }
)

# Register the example palette
PaletteRegistry.register('qscience', QSciencePalette)


# Example: Create a simple palette from a Coolors.co-style string
def create_simple_palette(
    name: str,
    color_string: str
) -> Palette:
    """
    Create a simple palette from a color string.

    Parameters
    ----------
    name : str
        The name of the palette.
    color_string : str
        A string of hex colors separated by hyphens (e.g.,
        "264653-2a9d8f-e9c46a-f4a261-e76f51").

    Returns
    -------
    Palette
        A new palette with the specified colors.

    Examples
    --------
    >>> palette = create_simple_palette(
    ...     "MyPalette",
    ...     "264653-2a9d8f-e9c46a-f4a261-e76f51"
    ... )
    >>> PaletteRegistry.register('mypalette', palette)
    """
    return Palette(name, color_string)


__all__ = [
    'QSciencePalette',
    'create_simple_palette'
]
