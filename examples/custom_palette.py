"""
Custom palette registration example.

This script demonstrates how to create and register custom palettes
and typography sets for use with string shortcuts.
"""

import numpy as np
from graphics_lib import (
    Palette,
    Colour,
    Typography,
    Font,
    PaletteRegistry,
    TypographyRegistry,
    LinePlot,
    create_simple_palette
)
from pathlib import Path

# Create output directory
OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)


def create_custom_palette():
    """
    Create and register a custom palette.
    """
    print("Creating Custom Palette")
    print("-" * 50)

    # Method 1: From individual colors
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

    # Register the palette
    PaletteRegistry.register('ocean', my_palette)
    print("✓ Custom 'ocean' palette registered")

    # Method 2: From a color string (Coolors.co style)
    simple_palette = create_simple_palette(
        "Sunset",
        "ff6b6b-ee5a6f-c44569-5f2c82-0e4c92"
    )

    PaletteRegistry.register('sunset', simple_palette)
    print("✓ Simple 'sunset' palette registered")

    # List all available palettes
    print(f"\nAvailable palettes: {PaletteRegistry.list_available()}")
    print()


def create_custom_typography():
    """
    Create and register a custom typography set.
    """
    print("Creating Custom Typography")
    print("-" * 50)

    # Create custom typography
    modern_typography = Typography(
        title=Font('Arial', 24, 'sans-serif'),
        subtitle=Font('Arial', 18, 'sans-serif'),
        body=Font('Arial', 14, 'sans-serif'),
        caption=Font('Arial', 11, 'sans-serif')
    )

    # Register the typography
    TypographyRegistry.register('modern', modern_typography)
    print("✓ Custom 'modern' typography registered")

    # List all available typography sets
    print(f"\nAvailable typography sets: {TypographyRegistry.list_available()}")
    print()


def use_custom_styles():
    """
    Use the custom palette and typography in a plot.
    """
    print("Using Custom Palette and Typography")
    print("-" * 50)

    # Generate sample data
    x = np.linspace(0, 4 * np.pi, 200)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # Create plot with custom palette and typography
    plot = LinePlot(
        x, [y1, y2],
        title='Trigonometric Functions',
        xlabel='Angle (radians)',
        ylabel='Value',
        palette='ocean',       # Our custom palette!
        typography='modern',   # Our custom typography!
        labels=['sin(x)', 'cos(x)']
    )

    plot.save(OUTPUT_DIR / 'custom_style_plot.png')
    print("✓ Plot with custom styles saved to 'custom_style_plot.png'")
    print()


def demonstrate_palette_methods():
    """
    Demonstrate useful Palette methods.
    """
    print("Palette Methods Demonstration")
    print("-" * 50)

    # Get a registered palette
    ocean = PaletteRegistry.get('ocean')

    # Visualize the palette
    ocean.visualize_palette(save_path=OUTPUT_DIR / 'ocean_palette.png')
    print("✓ Palette visualization saved to 'ocean_palette.png'")

    # Save palette to JSON
    ocean.save_palette(OUTPUT_DIR / 'ocean_palette.json')
    print("✓ Palette saved to 'ocean_palette.json'")

    # Load palette from JSON
    loaded_palette = Palette.load_palette(OUTPUT_DIR / 'ocean_palette.json')
    PaletteRegistry.register('ocean_loaded', loaded_palette)
    print("✓ Palette loaded from JSON and registered as 'ocean_loaded'")
    print()


def demonstrate_color_manipulation():
    """
    Demonstrate color manipulation features.
    """
    print("Color Manipulation Demonstration")
    print("-" * 50)

    from graphics_lib import COLOURS

    # Use predefined colors
    red = COLOURS['red']
    print(f"Original red: {red.hex}")

    # Darken the color
    dark_red = red.darken(30)
    print(f"Darkened red: {dark_red.hex}")

    # Lighten the color
    light_red = red.lighten(30)
    print(f"Lightened red: {light_red.hex}")

    # Create custom colors
    custom = Colour("#FF5733")
    print(f"\nCustom color RGB: {custom.rgb}")
    print(f"Custom color hex: {custom.hex}")
    print(f"Custom color RGBA: {custom.rgba}")
    print()


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("GraphicsLib Custom Palette and Typography Examples")
    print("=" * 50 + "\n")

    create_custom_palette()
    create_custom_typography()
    use_custom_styles()
    demonstrate_palette_methods()
    demonstrate_color_manipulation()

    print("=" * 50)
    print("All custom style examples completed successfully!")
    print("=" * 50)
