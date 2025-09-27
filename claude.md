# Parametric Sign Generator for 3D Printing - GUI Version

## Project Overview
This project creates customizable two-color signs/labels for 3D printing, specifically optimized for Bambu Lab P1S printers with bi-color printing capability. The signs use a stencil-cut technique where text is cut out from the top layer, allowing the bottom layer color to show through.

## Current Status
✅ **CLI VERSION COMPLETE** - The CadQuery-based command-line generator is fully functional
🎯 **NEW DIRECTION** - Create a Python GUI application for easier sign generation

## New GUI Requirements

### Core Functionality
Create a desktop GUI application with the following input fields:
1. **Text to print** - The label text (single or multi-line)
2. **Label dimensions** - Height and Width in mm
3. **Text heaviness** - Control the boldness/weight of text (amount of black inside each character)
4. **Bottom layer thickness** - Thickness in mm for the base layer
5. **Top layer thickness** - Thickness in mm for the top layer with text cutout

### Key Files

#### Current CLI Implementation (Reference)
- `cadquery_sign_generator.py` - Working CLI generator to be adapted for GUI backend
  - Properly cuts text from top layer
  - Generates two separate STL files for bi-color printing
  - Use as the core engine for GUI

#### New GUI Implementation (To Create)
- `sign_generator_gui.py` - Main GUI application
- `gui_generator_backend.py` - Backend engine (adapted from cadquery_sign_generator.py)
- `gui_config.json` - GUI settings and defaults


### GUI Technologies to Use
- **tkinter** - Built-in Python GUI framework (no extra dependencies)
- **Alternative**: PyQt5/PySide2 for more modern look
- **CadQuery** - Keep for CAD operations and text handling
- **trimesh** - For mesh operations and STL export
- **Threading** - For non-blocking STL generation

### Dependencies
```txt
cadquery
trimesh
numpy
shapely
# GUI options (choose one):
# tkinter (built-in)
# PyQt5 (pip install PyQt5)
# PySide2 (pip install PySide2)
```

### Installation
```bash
pip install cadquery trimesh numpy shapely
# For PyQt5 option:
pip install PyQt5
```

## GUI Design Specifications

### Main Window Layout
```
┌─────────────────────────────────────────────┐
│  Parametric Sign Generator                  │
├─────────────────────────────────────────────┤
│                                             │
│  Text to Print:                            │
│  ┌─────────────────────────────────────┐   │
│  │ [Text input field]                  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  Label Dimensions:                         │
│  Width (mm):  [100]  Height (mm): [25]     │
│                                             │
│  Text Heaviness:                           │
│  Light ○ ● Regular ○ Bold ○ Extra Bold    │
│  [Slider: 0 ──────●────── 100]             │
│                                             │
│  Layer Thickness:                          │
│  Bottom (mm): [1.0]  Top (mm): [1.0]       │
│                                             │
│  [Generate STL Files]  [Preview]  [Reset]  │
│                                             │
│  Status: Ready                             │
│  ─────────────────────────────────────     │
│  Output: Files saved to output/            │
└─────────────────────────────────────────────┘
```

### Input Field Specifications

#### 1. Text to Print
- **Type**: Text area (multi-line capable)
- **Default**: "LABEL"
- **Validation**: Non-empty
- **Max length**: 100 characters recommended

#### 2. Label Dimensions
- **Width**: Spinbox, 10-500mm, default 100mm
- **Height**: Spinbox, 5-200mm, default 25mm
- **Validation**: Positive numbers only

#### 3. Text Heaviness
- **Type**: Radio buttons + Slider
- **Options**: 
  - Light (font-weight: 300)
  - Regular (font-weight: 400)
  - Bold (font-weight: 700)
  - Extra Bold (font-weight: 900)
- **Slider**: 0-100 for fine control
- **Implementation**: Adjust stroke width or use different font weights

#### 4. Layer Thickness
- **Bottom**: Spinbox, 0.2-5.0mm, default 1.0mm
- **Top**: Spinbox, 0.2-5.0mm, default 1.0mm
- **Step**: 0.1mm increments

### GUI Features to Implement

#### Phase 1 - Basic GUI
- [ ] Window with all input fields
- [ ] Generate button functionality
- [ ] Basic validation
- [ ] Status messages
- [ ] File save dialog

#### Phase 2 - Enhanced Features
- [ ] Live preview panel
- [ ] Drag & drop text files
- [ ] Recent files list
- [ ] Save/load presets
- [ ] Progress bar for generation

#### Phase 3 - Advanced Features
- [ ] 3D preview using matplotlib
- [ ] Font selection dropdown
- [ ] Batch processing tab
- [ ] Export settings (STL, 3MF, etc.)


## Project Structure
```
/mnt/user-data/outputs/
├── cadquery_sign_generator.py     # Main working generator
├── working_sign_generator.py      # Alternative simpler version
├── simple_sign_generator.py       # Basic block letter version (deprecated)
├── parametric_sign_generator.py   # Original version (has text issues)
├── create_3mf.py                  # 3MF file creator (experimental)
├── create_bambu_3mf.py           # Bambu Studio project creator
├── generate_all_examples.py       # Batch example generator
├── requirements.txt               # Python dependencies
├── output/                        # Generated STL files
│   ├── ThreadedInserts_Final_bottom_black.stl
│   ├── ThreadedInserts_Final_top_yellow.stl
│   └── [various example STL files]
├── PRINT_INSTRUCTIONS.md         # Printing guide for end users
├── QUICK_START_GUIDE.md         # Quick reference guide
└── README.md                     # Original comprehensive documentation
```

## Known Issues & Solutions

### Issue 1: Text Generation in Original Version
**Problem**: The original `parametric_sign_generator.py` using matplotlib had issues with font rendering and text polygon creation.
**Solution**: Switched to CadQuery which has robust built-in text handling for CAD operations.

### Issue 2: Text Width/Margins
**Problem**: Text was too wide for the sign, extending too close to edges.
**Solution**: Implemented auto-sizing in `cadquery_sign_generator.py` and reduced default font size to 8.5mm for 100mm wide signs.

### Issue 3: 3MF File Compatibility
**Problem**: Generated .3mf files weren't importing correctly into Bambu Studio.
**Status**: Reverted to two separate STL files for maximum compatibility.

## Tasks for Claude Code - GUI Development

### Priority 1: Core GUI Implementation
1. **Create Main GUI Application**
   - Choose GUI framework (tkinter recommended for simplicity)
   - Implement main window with all input fields
   - Add buttons: Generate STL, Preview, Reset
   - Status bar for feedback

2. **Implement Text Heaviness Feature**
   - Research font weight implementation in CadQuery
   - Map slider values (0-100) to font weights
   - Alternative: Implement stroke width adjustment
   - Provide visual feedback

3. **Connect Backend Engine**
   - Adapt cadquery_sign_generator.py as backend
   - Pass GUI parameters to generator
   - Handle file generation in separate thread
   - Show progress during generation

4. **Input Validation**
   - Validate numeric ranges
   - Check text not empty
   - Prevent invalid dimension combinations
   - Show clear error messages

### Priority 2: User Experience Enhancements
1. **Add Live Preview Panel**
   - 2D representation of sign dimensions
   - Show text layout in real-time
   - Update on parameter changes
   - Display measurements

2. **Preset System**
   - Common label sizes (small, medium, large)
   - Save custom presets
   - Load last used settings
   - Quick templates

3. **File Management**
   - Choose output directory
   - Auto-naming system
   - Show recent files
   - Open output folder button

### Priority 3: Advanced Features
1. **3D Preview**
   - Real-time 3D view
   - Show both layers
   - Rotation controls
   - Export preview image

2. **Batch Processing**
   - Multiple signs from list
   - Import from CSV/Excel
   - Queue management
   - Bulk export

3. **Extended Options**
   - Font selection
   - Multi-line text with alignment
   - Border styles
   - Icon library
   - Support multi-level designs

2. **Border/Frame Options**
   - Add optional raised borders
   - Decorative corner elements

3. **Mounting Features**
   - Add screw holes option
   - Magnetic insert pockets
   - Adhesive backing guides

4. **Text Effects**
   - Beveled edges on text
   - Outlined text (double cut)
   - Embossed option (raised instead of cut)

### Testing Needed
1. Test with various text lengths and special characters
2. Verify STL validity with different CAD software
3. Test actual printing on Bambu Lab P1S
4. Benchmark generation speed for large batches

## API Design for Future Development

### Proposed Class Structure
```python
class SignGenerator:
    def __init__(self, preset="standard"):
        # Load preset configurations
        
    def set_dimensions(self, width, height, thickness):
        # Set sign dimensions
        
    def set_text(self, text, font="Arial", size="auto"):
        # Configure text with auto-sizing option
        
    def add_icon(self, icon_type, position="left"):
        # Add predefined icons
        
    def add_mounting(self, type="holes", spacing=None):
        # Add mounting features
        
    def generate(self, output_format="stl"):
        # Generate files in specified format
        
    def batch_generate(self, csv_file):
        # Generate multiple signs from CSV data
```

## Deployment Considerations

### Web Interface (Future)
- Flask/FastAPI backend
- Real-time STL preview
- Direct download or email delivery
- Preset templates gallery

### Command Line Tool
- Current implementation works well
- Could add config file support
- Batch processing from CSV/JSON

### Integration Points
- Bambu Studio plugin potential
- OctoPrint integration
- Thingiverse Customizer compatible

## Code Quality Notes

### What's Working Well
- CadQuery implementation is stable
- STL generation is reliable
- File sizes indicate proper geometry

### Areas for Improvement
- Error handling could be more robust
- Need input validation for dimensions
- Should add logging for debugging
- Code could use more comments

### Performance Metrics
- Current generation time: ~2-3 seconds per sign
- File sizes: 26KB (base) + 300-1200KB (top with text)
- Memory usage: Minimal (~50MB)

## Testing Commands

### Basic Test
```bash
python cadquery_sign_generator.py "TEST" --width 60 --height 20 --font-size 14
```

### Production Example
```bash
python cadquery_sign_generator.py "Threaded Inserts" --width 100 --height 25 --font-size 8.5
```

### Batch Generation
```bash
python generate_all_examples.py
```

## User Feedback Integration
- Users want simpler material assignment in Bambu Studio
- Need better handling of long text strings
- Request for preview images alongside STL files
- Want QR code support for asset tracking

## Next Session Goals
1. Fix any immediate bugs
2. Add requested features
3. Improve error handling
4. Create web interface prototype
5. Add comprehensive unit tests

## Contact & Context
- Target printer: Bambu Lab P1S
- Primary use case: Workshop/equipment labeling
- Color scheme: Typically black text on yellow background
- User skill level: Intermediate 3D printing experience

---
*This project is ready for continued development. The core functionality is working, and the architecture supports easy extension.*
