# 🏷️ Parametric Sign Generator GUI

## Overview
A desktop application for generating two-color 3D printable signs with **adjustable text heaviness control**. Perfect for creating custom labels and signs for Bambu Lab P1S bi-color printing.

## ✨ Key Features

### 1. **Text Heaviness Control** (Unique Feature!)
- Adjust the boldness/weight of text from light to extra bold
- Slider control (0-100) for fine-tuning
- Preset buttons for quick selection:
  - Light (25%)
  - Regular (50%)
  - Bold (75%)
  - Extra Bold (100%)

### 2. **Customizable Dimensions**
- Width: 10-500mm
- Height: 5-200mm
- Layer thickness: 0.2-5.0mm (both layers)

### 3. **Smart Text Sizing**
- Automatically adjusts font size to fit width
- Accounts for text heaviness in sizing calculations

### 4. **Validation & Safety**
- Input validation prevents errors
- Warnings for unusual dimensions
- Clear error messages

## 🚀 Quick Start

### Installation
```bash
# Install CadQuery (required)
pip install cadquery

# Note: tkinter is included with Python
```

### Running the GUI
```bash
# Option 1: Direct launch
python sign_generator_gui.py

# Option 2: Use launcher script
python launch_gui.py

# Option 3: Test features
python test_gui_features.py
```

## 📝 How to Use

### Step 1: Enter Your Text
- Type your label text in the text area
- Supports single or multi-line text
- Max 100 characters recommended

### Step 2: Set Dimensions
- Adjust width and height in millimeters
- Default: 100mm x 25mm (standard label size)

### Step 3: Choose Text Heaviness
- **This is the key feature!**
- Use preset buttons or slider
- Light = thin, delicate text
- Regular = standard weight
- Bold = thicker, more prominent
- Extra Bold = maximum thickness

### Step 4: Adjust Layer Thickness
- Bottom layer (black): Default 1.0mm
- Top layer (yellow): Default 1.0mm

### Step 5: Generate STL Files
- Click "Generate STL ✓"
- Wait for progress to complete
- Files saved to `output/` folder

## 📂 Output Files

Each generation creates 3 files:
```
output/
├── [name]_[weight]_bottom_black.stl    # Base layer
├── [name]_[weight]_top_yellow.stl      # Top with text cutout
└── [name]_[weight]_combined_preview.stl # Preview model
```

Weight labels: `light`, `regular`, `bold`, or `extrabold`

## 🖨️ Printing Instructions

### Bambu Studio Setup
1. Import both layer STL files
2. Assign materials:
   - Bottom layer → Black filament
   - Top layer → Yellow filament
3. Ensure alignment (use "Assemble" if needed)
4. Recommended settings:
   - Layer height: 0.2mm
   - Infill: 20% (Grid or Gyroid)
   - No supports needed

## 🎨 Text Heaviness Examples

| Heaviness | Effect | Use Case |
|-----------|--------|----------|
| 0-25% | Light, delicate | Elegant labels, fine text |
| 26-50% | Regular weight | Standard labels |
| 51-75% | Bold, prominent | Important signs |
| 76-100% | Extra bold | Maximum visibility |

## 🔧 Technical Details

### How Text Heaviness Works
The GUI adjusts multiple parameters to achieve different text weights:
1. **Font size multiplier** - Slightly scales text size
2. **Stroke adjustments** - Modifies cut patterns
3. **Multiple cuts** - For extra bold, applies offset cuts

### File Structure
```
SignGen_v1/
├── sign_generator_gui.py        # Main GUI application
├── gui_generator_backend.py     # Enhanced backend with heaviness
├── cadquery_sign_generator.py   # Original backend
├── launch_gui.py               # Simple launcher script
├── test_gui_features.py        # Test/demo script
└── output/                     # Generated STL files
```

## 🐛 Troubleshooting

### GUI Won't Launch
- Check Python version (3.7+ required)
- Verify CadQuery installed: `pip install cadquery`
- Run test script: `python test_gui_features.py`

### Generation Fails
- Check text isn't empty
- Verify dimensions are within valid ranges
- Try reducing text heaviness if cuts fail

### Files Not Appearing
- Check `output/` folder exists
- Verify write permissions
- Look for error messages in status bar

## 📊 Performance

- Generation time: 2-5 seconds per sign
- File sizes:
  - Bottom layer: ~26KB (constant)
  - Top layer: 80-300KB (varies with text complexity)
- Memory usage: ~100MB

## 🎯 Future Enhancements

### Planned for Phase 2
- [ ] Live 2D preview panel
- [ ] Preset sizes (Small/Medium/Large)
- [ ] Save/load settings
- [ ] Recent files list

### Planned for Phase 3
- [ ] 3D preview with rotation
- [ ] Font selection
- [ ] Batch processing
- [ ] Direct Bambu Studio integration

## 📜 License
Open source - use freely for personal and commercial projects.

## 🤝 Contributing
Suggestions and improvements welcome! The text heaviness feature is unique and we'd love to hear how you use it.

---

**Created: September 26, 2024**
**Status: ✅ Phase 1 Complete - GUI with Text Heaviness Control**