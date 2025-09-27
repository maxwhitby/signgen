# Parametric Sign Generator for 3D Printing

## 🎯 NEW DIRECTION: GUI Application Development
**Note for Developers**: This project is being transformed into a GUI application. See `GUI_SPECIFICATION.md` and `START_HERE.md` for the new development direction. The command-line version below is fully functional and will serve as the backend for the GUI.

---

## Original CLI Version Documentation

A Python tool for generating customizable two-color signs/labels for 3D printing, optimized for the Bambu Lab P1S and similar printers.

## Features

- **Parametric Design**: Fully customizable text, dimensions, and styling
- **Two-Color Printing**: Designed for bi-color printing with stencil-cut text
- **Engineering-Focused**: Clean sans-serif fonts suitable for technical labels
- **STL Output**: Generates separate STL files for each color layer
- **Rounded Corners**: Optional rounded corners for professional appearance
- **Batch Generation**: Create multiple signs with different parameters

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Generate a simple sign with default parameters:
```bash
python parametric_sign_generator.py "YOUR TEXT"
```

### Command Line Options

```bash
python parametric_sign_generator.py "YOUR TEXT" [options]

Options:
  --width FLOAT          Sign width in mm (default: 100)
  --height FLOAT         Sign height in mm (default: 30)
  --font-size FLOAT      Font size in mm (default: 20)
  --top-thickness FLOAT  Top layer thickness in mm (default: 1.0)
  --bottom-thickness FLOAT  Bottom layer thickness in mm (default: 1.0)
  --corner-radius FLOAT  Corner radius in mm (default: 2.0)
  --output STRING        Base filename for output STL files (default: sign)
  --font STRING          Font name (default: Arial)
```

### Examples

1. **Simple Label**:
```bash
python parametric_sign_generator.py "MOTOR-01" --width 80 --height 25 --font-size 15
```

2. **Warning Sign**:
```bash
python parametric_sign_generator.py "HIGH VOLTAGE" --width 120 --height 40 --font-size 18
```

3. **Small Component Label**:
```bash
python parametric_sign_generator.py "PWR" --width 30 --height 15 --font-size 10 --top-thickness 0.8
```

4. **Department Sign**:
```bash
python parametric_sign_generator.py "ENGINEERING" --width 150 --height 50 --font-size 25
```

### Generate Example Signs

Run the example script to generate several sample signs:
```bash
python generate_examples.py
```

This will create various example signs in the `output` directory.

## Output Files

The generator creates three STL files for each sign:

1. `*_top_yellow.stl` - Top layer with text cut out (for yellow filament)
2. `*_bottom_black.stl` - Bottom solid layer (for black filament)
3. `*_combined_preview.stl` - Combined model for preview only

## Printing Instructions for Bambu Lab P1S

### Bambu Studio Setup

1. **Import Files**:
   - Click "Import" or drag both layer files into Bambu Studio
   - Import `*_bottom_black.stl` first
   - Import `*_top_yellow.stl` second

2. **Assign Filaments**:
   - Select the bottom layer object
   - Assign black filament (or your text color)
   - Select the top layer object
   - Assign yellow filament (or your background color)

3. **Alignment**:
   - The layers should auto-align at origin (0,0,0)
   - If not aligned, select both objects and use "Align" tool

### Recommended Print Settings

- **Layer Height**: 0.2mm (0.16mm for finer detail)
- **Initial Layer Height**: 0.2mm
- **Infill**: 15-20% (grid or gyroid pattern)
- **Wall Loops**: 2-3
- **Top/Bottom Layers**: 3
- **Support**: None needed
- **Bed Temperature**: 
  - PLA: 60°C
  - PETG: 80°C
  - ABS: 100°C
- **Nozzle Temperature**: As per filament specifications

### Multi-Color Printing Options

#### Option 1: Multi-Material (AMS)
- Load black filament in slot 1
- Load yellow filament in slot 2
- The AMS will handle automatic switching

#### Option 2: Manual Color Change
- Print bottom layer first as separate job
- Change filament
- Print top layer aligned on the bottom

#### Option 3: Single Print with Pause
- Combine both STLs in slicer
- Add filament change command at layer transition
- Manually swap filament when prompted

### Tips for Best Results

1. **Bed Adhesion**: Ensure good first layer adhesion with proper bed leveling
2. **Color Contrast**: Use high-contrast color combinations for best readability
3. **Text Size**: Keep font size at least 10mm for clear text
4. **Layer Thickness**: 1mm per layer provides good durability
5. **Post-Processing**: Light sanding can improve text clarity if needed

## Customization

### Using as a Python Module

```python
from parametric_sign_generator import ParametricSignGenerator

# Create generator instance
generator = ParametricSignGenerator()

# Generate custom sign
meshes = generator.generate_sign(
    text="CUSTOM TEXT",
    sign_width=100,
    sign_height=30,
    font_size=18,
    top_layer_thickness=1.0,
    bottom_layer_thickness=1.0,
    corner_radius=2.0,
    font_name="Arial"
)

# Save STL files
generator.save_stl(meshes, "custom_sign")
```

### Available Fonts

The generator will attempt to use these fonts in order:
1. Specified font (--font parameter)
2. DejaVu Sans
3. Liberation Sans
4. Helvetica
5. Arial
6. System default sans-serif

## Common Use Cases

- **Equipment Labels**: Mark 3D printers, tools, and machinery
- **Department Signs**: Office and workspace identification
- **Warning Labels**: Safety and hazard warnings
- **Component Marking**: Electronic enclosures and project boxes
- **Cable Management**: Wire and cable identifiers
- **Storage Labels**: Bins, drawers, and shelf marking
- **Prototype Identification**: Version and serial numbers

## Troubleshooting

### Missing Dependencies
If you get import errors, ensure all packages are installed:
```bash
pip install --upgrade -r requirements.txt
```

### Font Issues
If text doesn't render correctly, the system might be missing fonts:
- **Linux**: `sudo apt-get install fonts-liberation fonts-dejavu`
- **Windows**: Fonts should be available by default
- **macOS**: Install additional fonts through Font Book if needed

### STL File Issues
If STL files won't import into your slicer:
- Check that files are not empty (should be > 1KB)
- Try opening in a 3D viewer first to verify geometry
- Ensure your slicer supports ASCII STL format

### Text Not Centered
Adjust the font_size parameter if text appears too large or small for the sign

## License

MIT License - Feel free to modify and distribute

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests for:
- Additional font support
- More geometric options (shapes, borders)
- Multi-line text support
- Icon/symbol integration
- Alternative output formats

## Credits

Created for efficient label generation for 3D printing projects, optimized for the Bambu Lab P1S printer.
