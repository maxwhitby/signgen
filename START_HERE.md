# 🚀 START HERE - Parametric Sign Generator GUI Project

Welcome Claude Code! This project needs a GUI application for easier sign generation.

## 🎯 NEW MISSION: Create GUI Application
Transform the working command-line sign generator into a user-friendly desktop application with graphical interface.

## 📋 GUI Requirements

### Essential Input Fields:
1. **Text to print** - Multi-line text area
2. **Label dimensions** - Width and Height in mm
3. **Text heaviness** - Control boldness (amount of black in characters)
4. **Bottom layer thickness** - In mm
5. **Top layer thickness** - In mm

### Key Feature: Text Heaviness
This is the unique requirement - users want to control how "heavy" or bold the text appears, essentially controlling the amount of black inside each character. This could be:
- Font weight variations (Light → Regular → Bold → Extra Bold)
- Stroke width adjustment
- Custom rendering control

## 📚 Documentation Package

### 1. GUI Specification (START WITH THIS!)
**→ [`GUI_SPECIFICATION.md`](GUI_SPECIFICATION.md)**
- Complete GUI requirements
- Layout designs
- Implementation approaches
- Text heaviness strategies

### 2. Primary Technical Document
**→ [`claude.md`](claude.md)**
- Updated with GUI architecture
- Backend integration notes
- Technology choices


### 3. Task Management
**→ [`TODO.md`](TODO.md)**
- GUI implementation priorities
- Text heaviness feature details
- Phase 1, 2, 3 breakdown

### 4. Testing & Validation
**→ [`TESTING.md`](TESTING.md)**
- GUI testing procedures
- Backend integration tests
- Validation requirements

## 🔨 Current Working Code (Backend)

### CLI Generator (Use as Backend Engine)
```python
# This works - adapt it for GUI backend
python cadquery_sign_generator.py "Your Text" --width 100 --height 25
```

The existing `cadquery_sign_generator.py` should be adapted as the backend engine for the GUI. It already handles STL generation correctly.

## 🎯 Your First Tasks

### 1. Create Basic GUI Window
```python
# sign_generator_gui.py
import tkinter as tk
from tkinter import ttk

class SignGeneratorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Parametric Sign Generator")
        self.setup_ui()
    
    def setup_ui(self):
        # Add 5 input fields
        # Add Generate button
        # Connect to backend
```

### 2. Implement Text Heaviness Control
This is the KEY FEATURE. Users want to control text boldness/weight:
```python
# Ideas for implementation:
# 1. Map slider (0-100) to font weights
# 2. Adjust stroke width
# 3. Use different font families
```

### 3. Test Generation
```bash
# Current CLI works - ensure GUI produces same quality
python cadquery_sign_generator.py "TEST" --width 100 --height 25
# Files should be: ~26KB (bottom) and >100KB (top with text cutout)
```

## 💡 Implementation Strategy

### Phase 1: Minimum Viable GUI
1. Create window with all 5 input fields
2. Generate button calls backend
3. Basic validation
4. Shows success/error messages

### Phase 2: Text Heaviness Feature
1. Research font weight control in CadQuery
2. Implement slider control
3. Test with different weights
4. Verify visible difference in output

### Phase 3: Polish
1. Add preview capability
2. Presets for common sizes
3. Better error handling
4. Progress feedback

## 🔧 Technology Recommendations

### GUI Framework
**Recommended: tkinter**
- Built into Python (no extra dependencies)
- Simple to implement
- Sufficient for this project

**Alternative: PyQt5**
- More modern appearance
- Better widgets
- Requires installation

### Backend Integration
```python
# Adapt existing generator
from cadquery_sign_generator import CadQuerySignGenerator

class SignBackend:
    def __init__(self):
        self.generator = CadQuerySignGenerator()
    
    def generate_with_heaviness(self, text, width, height, heaviness, ...):
        # Convert heaviness to font parameter
        # Call generator
        # Return file paths
```

## 📦 Expected GUI Output

```
User fills form → Click Generate → Backend creates:
├── output/
│   ├── sign_bottom_white.stl     # Base layer
│   ├── sign_top_yellow.stl       # Top with text cutout
│   └── sign_combined_preview.stl # Preview

Text heaviness should visibly affect the boldness of the cutout text.
```

## ⚡ Quick Test Commands

```bash
# Test current backend (works)
python cadquery_sign_generator.py "GUI TEST" --width 100 --height 25

# Your GUI should produce identical output
python sign_generator_gui.py  # Launch GUI
# Enter same parameters → Generate → Compare files
```

## 🏁 Success Criteria

Your GUI is complete when:
1. ✅ All 5 input fields working
2. ✅ Text heaviness slider affects output visibly
3. ✅ STL files generate correctly
4. ✅ Validation prevents errors
5. ✅ Clear user feedback
6. ✅ Files work in Bambu Studio

## 🚦 Ready to Build the GUI!

Focus on creating a simple, functional GUI that makes sign generation easier for users. The backend already works - you just need to wrap it in a nice interface with the text heaviness control as the key new feature.

Good luck, Claude Code! 🎉

---
*GUI Project Start: 2024-09-26*
*Backend Status: Working*
*GUI Status: To Be Created*
