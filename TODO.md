# TODO - Parametric Sign Generator GUI Application

## 🎯 NEW DIRECTION: GUI Application Development

### Priority 1 - Core GUI Implementation ⭐⭐⭐
- [ ] **Create GUI Application Structure**
  ```python
  # sign_generator_gui.py
  - Main window setup
  - All 5 input fields (text, width, height, heaviness, thicknesses)
  - Generate button functionality
  - Status bar
  ```

- [ ] **Implement Text Heaviness Feature**
  ```python
  # This is the KEY FEATURE requested
  # "heaviness of text (amount of black inside each character)"
  - Research font weight control in CadQuery
  - Implement slider (0-100) to font weight mapping
  - Test with Light, Regular, Bold, Extra Bold
  - Visual feedback in UI
  ```

- [ ] **Input Field Implementation**
  - Text area for multi-line text
  - Width spinner (10-500mm)
  - Height spinner (5-200mm) 
  - Heaviness slider with radio button presets
  - Bottom thickness spinner (0.2-5.0mm)
  - Top thickness spinner (0.2-5.0mm)

- [ ] **Backend Integration**
  ```python
  # Adapt cadquery_sign_generator.py
  def generate_with_heaviness(text, width, height, heaviness, bottom_thick, top_thick):
      # Map heaviness to font weight/stroke
      # Generate STL files
      # Return status and file paths
  ```

- [ ] **Input Validation**
  - Non-empty text validation
  - Numeric range checking
  - Error message display
  - Highlight invalid fields


### Priority 2 - User Experience Enhancements ⭐⭐
- [ ] **GUI Framework Selection**
  ```python
  # Recommend: Start with tkinter (built-in)
  import tkinter as tk
  from tkinter import ttk
  
  # Alternative: PyQt5 for better appearance
  # from PyQt5 import QtWidgets
  ```

- [ ] **Live Preview Panel**
  - 2D representation of sign dimensions
  - Show text layout
  - Update in real-time
  - Display actual measurements

- [ ] **Progress Feedback**
  - Progress bar during generation
  - Disable buttons while processing
  - Success/error notifications
  - Time estimate

- [ ] **File Management**
  - Output directory selection
  - Show generated file locations
  - Open output folder button
  - Recent files list

- [ ] **Presets System**
  ```python
  PRESETS = {
      "Small Label": {"width": 50, "height": 20},
      "Standard": {"width": 100, "height": 25},
      "Large Sign": {"width": 200, "height": 50}
  }
  ```

### Priority 3 - Advanced Features ⭐
- [ ] **3D Preview Window**
  ```python
  # Using matplotlib or trimesh viewer
  def show_3d_preview(stl_file):
      mesh = trimesh.load(stl_file)
      mesh.show()  # Opens 3D viewer
  ```

- [ ] **Batch Processing Tab**
  - Import list from CSV
  - Generate multiple signs
  - Progress tracking
  - Error handling for failed items

- [ ] **Text Heaviness Variations**
  ```python
  # Advanced implementation ideas:
  - Stroke width adjustment
  - Font morphing between weights
  - Custom outline generation
  - Multiple font family support
  ```

- [ ] **Export Options**
  - Save settings to JSON
  - Export as project file
  - Generate Bambu Studio .3mf
  - Create print summary

## Priority 4 - Enhancements

### Batch Processing
```python
# CSV format:
# text,width,height,font_size,output_name
# "MOTOR-01",80,25,14,motor_1
# "MOTOR-02",80,25,14,motor_2

def batch_from_csv(csv_file):
    """Generate multiple signs from CSV"""
    pass
```

### Preview Generation
```python
def generate_preview_image(stl_file, output_png):
    """Create PNG preview of STL"""
    # Use trimesh + matplotlib
    # Render from top view
    # Save as PNG
```

### Web Interface
```python
# Flask app structure:
/web_app
  /static
    /css
    /js
    /downloads
  /templates
    index.html
    preview.html
  app.py
  generator.py
```

## Priority 5 - Code Quality

### Unit Tests
```python
# test_generator.py
def test_dimensions():
    """Test dimension validation"""
    
def test_text_cutout():
    """Verify text is properly cut"""
    
def test_file_output():
    """Check STL file validity"""
```

### Documentation
- [ ] Add docstrings to all methods
- [ ] Create API documentation
- [ ] Add inline comments for complex logic
- [ ] Create user guide with images

### Refactoring
- [ ] Extract constants to config file
- [ ] Separate geometry creation from file I/O
- [ ] Create abstract base class for generators
- [ ] Implement factory pattern for different generator types

## Priority 6 - Advanced Features

### Material Profiles
```json
{
  "profiles": {
    "indoor_pla": {
      "top_thickness": 1.0,
      "bottom_thickness": 1.0,
      "infill": 20
    },
    "outdoor_petg": {
      "top_thickness": 1.5,
      "bottom_thickness": 1.5,
      "infill": 40
    }
  }
}
```

### Template System
```yaml
templates:
  warning_sign:
    font_size: 18
    colors: ["red", "white"]
    border: true
    icon: "warning"
  
  asset_tag:
    font_size: 10
    include_qr: true
    mounting: "holes"
```

### Export Formats
- [ ] Support for STEP files
- [ ] OpenSCAD script generation
- [ ] SVG for laser cutting
- [ ] G-code direct generation

## Completed Tasks ✅
- [x] Basic sign generation
- [x] CadQuery implementation
- [x] Font size auto-adjustment
- [x] Two-layer STL output
- [x] Rounded corners
- [x] Example generators
- [x] Basic documentation

## Notes for Implementation
- Keep backward compatibility with existing CLI
- All new features should be optional
- Maintain fast generation times (<5 seconds)
- Ensure cross-platform compatibility
- Follow PEP 8 style guidelines

## Testing Checklist
Before marking any task complete:
- [ ] Feature works as expected
- [ ] Error cases handled
- [ ] Documentation updated
- [ ] Example added
- [ ] Tested on Windows/Linux/Mac
