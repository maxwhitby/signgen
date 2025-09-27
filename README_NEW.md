# SignGen - Parametric Sign Generator for 3D Printing

![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A powerful tool for creating customizable two-color signs and labels for 3D printing, optimized for Bambu Lab P1S printers with bi-color printing capability.

## Features

- **Intuitive GUI**: User-friendly interface with real-time 2D preview
- **Text Customization**: Adjustable text weight/heaviness from light to extra bold
- **Smart Font Sizing**: Automatic or manual font size control
- **Multiple Fonts**: Support for various sans-serif typefaces
- **Validation System**: Pre-generation validation to prevent failures
- **Preset Management**: Save and load custom presets
- **Command-Line Interface**: Full CLI support for automation
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/maxwhitby/signgen.git
cd signgen

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Using pip (coming soon)

```bash
pip install signgen
```

## Quick Start

### GUI Application

Launch the GUI application:

```bash
python -m src.gui
# or after installation:
signgen-gui
```

### Command Line

Generate a sign from the command line:

```bash
python -m src.cli "YOUR TEXT" --width 100 --height 25 --heaviness 50
# or after installation:
signgen "YOUR TEXT" --width 100 --height 25 --heaviness 50
```

## Usage Guide

### GUI Controls

1. **Text Input**: Enter the text for your sign
2. **Dimensions**: Set width and height in millimeters
3. **Font Selection**: Choose from available fonts or use preset buttons
4. **Text Weight**: Adjust the slider (0-100) to control text heaviness
   - Light (0-25): Thin, delicate text
   - Regular (26-50): Standard text weight
   - Bold (51-75): Heavier, prominent text
   - Extra Bold (76-100): Maximum text weight
5. **Font Size**: Enable auto-size or set manually (5-50mm)
6. **Layer Thickness**: Set bottom and top layer thickness (typically 1mm each)

### CLI Options

```bash
signgen "TEXT" [options]

Options:
  --width WIDTH             Sign width in mm (default: 100)
  --height HEIGHT           Sign height in mm (default: 25)
  --font FONT              Font family (default: Arial)
  --font-size SIZE         Font size in mm (auto if not specified)
  --heaviness WEIGHT       Text weight 0-100 (default: 50)
  --bottom-thickness MM    Bottom layer thickness (default: 1.0)
  --top-thickness MM       Top layer thickness (default: 1.0)
  --output-dir DIR         Output directory (default: output)
  --debug                  Enable debug logging
```

## How It Works

The generator creates two-layer signs using a stencil-cut technique:

1. **Bottom Layer**: A solid base layer (typically printed in black)
2. **Top Layer**: A layer with text cut out (typically printed in yellow)

When assembled, the bottom layer shows through the text cutouts, creating high-contrast, professional-looking labels.

## Printing Instructions

1. **Slicer Setup**:
   - Import both STL files into your slicer
   - Assign different colors to each file
   - Ensure proper layer alignment

2. **Recommended Settings**:
   - Layer height: 0.2mm
   - Infill: 20-30%
   - No supports needed
   - Print speed: Standard

3. **Bambu Studio**:
   - Use the AMS for automatic color switching
   - Files are pre-named with color hints (_bottom_black, _top_yellow)

## Troubleshooting

### Top layer STL file not generated

**Cause**: Text has cut completely through the layer

**Solutions**:
- Reduce font size
- Reduce text heaviness
- Increase top layer thickness
- Use shorter text

### Text appears too small

**Solutions**:
- Disable "Auto-size font" checkbox
- Manually increase font size
- Reduce sign dimensions

### Generation fails with validation error

**Solutions**:
- Check all numeric inputs are valid
- Ensure text is not empty
- Verify dimensions are within limits (10-500mm width, 5-200mm height)

## Development

### Project Structure

```
signgen/
├── src/
│   ├── __init__.py
│   ├── sign_generator.py    # Core generation engine
│   ├── gui.py               # GUI application
│   ├── cli.py               # CLI interface
│   ├── validators.py        # Input validation
│   ├── config_manager.py    # Settings management
│   ├── exceptions.py        # Custom exceptions
│   └── logger.py            # Logging configuration
├── tests/
│   ├── test_validators.py
│   └── test_config.py
├── output/                  # Generated STL files
├── requirements.txt
├── setup.py
└── README.md
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Requirements

- Python 3.7+
- CadQuery 2.0+
- NumPy
- Trimesh
- Tkinter (usually included with Python)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [CadQuery](https://github.com/CadQuery/cadquery) for robust CAD operations
- Optimized for [Bambu Lab](https://bambulab.com) printers
- Inspired by the need for better workshop organization

## Support

For issues, questions, or suggestions, please [open an issue](https://github.com/maxwhitby/signgen/issues) on GitHub.

---

**Happy Printing! 🎯🖨️**