# GUI Specification - Parametric Sign Generator

## Overview
Create a Python desktop application with a graphical user interface for generating two-color 3D printable sign STL files.

## Core Requirements

### Input Fields (MUST HAVE)
1. **Text to Print**
   - Multi-line text area
   - Support for single and multi-line text
   - Character limit: 100 chars recommended

2. **Label Dimensions**
   - Width in mm (10-500mm range)
   - Height in mm (5-200mm range)
   - Linked aspect ratio option (future)

3. **Text Heaviness**
   - Control boldness/weight of characters
   - "Amount of black inside each character"
   - Slider from 0-100 or preset options
   - Implementation options:
     - Font weight variations (light to extra bold)
     - Stroke width adjustment
     - Custom font rendering

4. **Bottom Layer Thickness**
   - Input in mm (0.2-5.0mm)
   - Default: 1.0mm
   - Step: 0.1mm

5. **Top Layer Thickness**  
   - Input in mm (0.2-5.0mm)
   - Default: 1.0mm
   - Step: 0.1mm

### Buttons
- **Generate STL Files** - Creates both layer files
- **Preview** - Shows 2D/3D preview (Phase 2)
- **Reset** - Resets all fields to defaults

## GUI Layout Design

### Option 1: Simple Vertical Layout (Recommended for Phase 1)
```
┌──────────────────────────────────────────────────┐
│  🏷️ Parametric Sign Generator                    │
├──────────────────────────────────────────────────┤
│                                                  │
│  Text to Print:                                 │
│  ┌──────────────────────────────────────────┐   │
│  │                                          │   │
│  │  [Multi-line text area]                  │   │
│  │                                          │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  Label Dimensions (mm):                         │
│  Width:  [100.0 ▼]    Height: [25.0 ▼]         │
│                                                  │
│  Text Heaviness:                                │
│  Light ○  Regular ●  Bold ○  Extra Bold ○      │
│  Fine Control: [━━━━━●━━━━━━━━━] 50            │
│                                                  │
│  Layer Thickness (mm):                          │
│  Bottom: [1.0 ▼]      Top: [1.0 ▼]             │
│                                                  │
│  ┌────────────────┐ ┌─────────┐ ┌──────────┐   │
│  │ Generate STL ✓ │ │ Preview │ │  Reset   │   │
│  └────────────────┘ └─────────┘ └──────────┘   │
│                                                  │
│  ──────────────────────────────────────────     │
│  Status: Ready                                  │
│  Output: C:\Users\...\output\sign_*.stl         │
└──────────────────────────────────────────────────┘
```

### Option 2: Tabbed Interface (For Future Phases)
```
┌──────────────────────────────────────────────────┐
│  Parametric Sign Generator                      │
├──────────────────────────────────────────────────┤
│ [Basic] [Advanced] [Batch] [Settings]           │
├──────────────────────────────────────────────────┤
│  Basic Tab Content (as above)                   │
└──────────────────────────────────────────────────┘
```

## Implementation Details

### Text Heaviness Implementation

#### Approach 1: Font Weight Mapping (Simpler)
```python
heaviness_map = {
    0-25: "Light",      # font-weight: 300
    26-50: "Regular",   # font-weight: 400
    51-75: "Bold",      # font-weight: 700
    76-100: "Extra Bold" # font-weight: 900
}
```

#### Approach 2: Stroke Width Adjustment (More Control)
```python
def calculate_stroke_width(heaviness_value):
    # Map 0-100 to stroke width multiplier
    # 0 = 0.8x normal, 100 = 1.5x normal
    return 0.8 + (heaviness_value / 100) * 0.7
```

#### Approach 3: Custom Font Morphing (Advanced)
- Interpolate between font weights
- Adjust character outlines
- Requires advanced font manipulation

### GUI Framework Options

#### Option 1: Tkinter (Recommended)
**Pros:**
- Built into Python (no extra install)
- Simple to learn and use
- Cross-platform
- Sufficient for our needs

**Cons:**
- Dated appearance
- Limited widgets

**Example Structure:**
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class SignGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parametric Sign Generator")
        self.create_widgets()
    
    def create_widgets(self):
        # Text input
        tk.Label(self.root, text="Text to Print:").pack()
        self.text_input = tk.Text(self.root, height=3)
        self.text_input.pack()
        
        # Dimensions
        dims_frame = tk.Frame(self.root)
        tk.Label(dims_frame, text="Width (mm):").pack(side=tk.LEFT)
        self.width_input = tk.Spinbox(dims_frame, from_=10, to=500)
        self.width_input.pack(side=tk.LEFT)
        # ... etc
```

#### Option 2: PyQt5/PySide2
**Pros:**
- Modern, professional appearance
- Rich widget set
- Excellent documentation
- Native look on each OS

**Cons:**
- Requires installation
- Larger learning curve
- Larger application size

#### Option 3: Kivy
**Pros:**
- Modern, customizable
- Touch-friendly
- Good for future mobile port

**Cons:**
- Different paradigm
- Requires installation
- Overkill for this project

### Backend Integration

```python
class SignGeneratorBackend:
    """Adapted from cadquery_sign_generator.py"""
    
    def generate_sign(self, 
                     text, 
                     width, 
                     height, 
                     heaviness,
                     bottom_thickness,
                     top_thickness):
        """
        Generate STL files with given parameters
        Returns: tuple of (success, message, file_paths)
        """
        # Convert heaviness to font weight
        font_weight = self.heaviness_to_font_weight(heaviness)
        
        # Use existing CadQuery code
        # ... generation logic ...
        
        return True, "Files generated", [bottom_path, top_path]
```

## User Experience Flow

1. **Launch Application**
   - Window opens with default values
   - Focus on text input field

2. **Enter Parameters**
   - Type text
   - Adjust dimensions if needed
   - Set text heaviness via radio or slider
   - Modify layer thicknesses if desired

3. **Generate Files**
   - Click "Generate STL Files"
   - Progress indicator shows
   - Success message displays
   - Output location shown

4. **Optional Preview** (Phase 2)
   - Click "Preview" 
   - 2D or 3D view opens
   - Verify appearance

5. **Use Files**
   - Navigate to output folder
   - Import into Bambu Studio
   - Print sign

## Validation Rules

### Text Input
- Not empty
- Length > 0
- Warn if > 50 characters
- Handle special characters gracefully

### Dimensions
- Width: 10mm ≤ w ≤ 500mm
- Height: 5mm ≤ h ≤ 200mm
- Warn if aspect ratio unusual (w/h > 10 or < 0.1)

### Text Heaviness
- Value: 0 ≤ v ≤ 100
- Default: 50 (Regular)

### Layer Thickness
- Range: 0.2mm ≤ t ≤ 5.0mm
- Warn if total > 10mm
- Warn if bottom < top (unusual)

## Error Handling

### User Errors
- Empty text → Show message: "Please enter text"
- Invalid dimensions → Highlight field, show range
- Generation fails → Show error dialog with details

### System Errors
- CadQuery not installed → Installation instructions
- Output directory not writable → Choose new location
- Memory error → Suggest smaller text/dimensions

## Future Enhancements

### Phase 2
- [ ] Live 2D preview panel
- [ ] Preset dropdown (Small/Medium/Large/Custom)
- [ ] Recent files list
- [ ] Tooltips for all fields

### Phase 3
- [ ] 3D preview with rotation
- [ ] Font selection dropdown
- [ ] Multi-line text alignment options
- [ ] Batch processing tab

### Phase 4
- [ ] Icon library integration
- [ ] QR code support
- [ ] Cloud save/load
- [ ] Direct printer integration

## Testing Requirements

### Unit Tests
- All validation functions
- Backend generation with various parameters
- File I/O operations

### Integration Tests
- GUI to backend communication
- File generation from GUI
- Error handling paths

### User Acceptance Tests
- Generate simple sign
- Generate complex multi-line sign
- Use extreme values
- Error recovery

## Success Criteria

The GUI is considered complete when:
1. ✓ All 5 input fields functional
2. ✓ STL files generate correctly
3. ✓ Validation prevents errors
4. ✓ Clear status messages
5. ✓ Files work in Bambu Studio
6. ✓ Text heaviness visibly affects output
7. ✓ Cross-platform operation (Windows/Mac/Linux)

## Example Test Cases

| Test | Text | Width | Height | Heaviness | Bottom | Top | Expected |
|------|------|-------|--------|-----------|--------|-----|----------|
| 1 | "TEST" | 60 | 20 | 50 | 1.0 | 1.0 | Success |
| 2 | "BOLD" | 80 | 30 | 100 | 1.0 | 1.0 | Extra bold text |
| 3 | "thin" | 100 | 25 | 0 | 0.5 | 0.5 | Light text |
| 4 | "" | 100 | 25 | 50 | 1.0 | 1.0 | Error: empty |
| 5 | "TEST" | 5 | 200 | 50 | 1.0 | 1.0 | Error: width too small |

---
*GUI Specification v1.0 - Ready for Implementation*