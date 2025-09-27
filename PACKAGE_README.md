# Parametric Sign Generator - GUI Development Package

## 🎯 Project Goal
Transform the working command-line sign generator into a Python GUI application with specific focus on **text heaviness control** (boldness/weight adjustment).

## 📋 Quick Start for Claude Code

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test Current Backend
```bash
python cadquery_sign_generator.py "TEST" --width 100 --height 25
# This should generate STL files in output/ directory
```

### Step 3: Run GUI Template
```bash
python sign_generator_gui_template.py
# This opens the GUI window with all required fields
```

### Step 4: Start Development
Begin implementing the backend integration in `sign_generator_gui_template.py`

## 📁 Package Contents

### 🔴 START HERE - Main Documentation
- **`START_HERE.md`** - Entry point, read this first!
- **`GUI_SPECIFICATION.md`** - Complete GUI requirements and design
- **`GUI_PROJECT_SUMMARY.md`** - Project direction overview

### 🟡 Core Files - Essential Code
- **`cadquery_sign_generator.py`** - Working backend engine (CLI version)
- **`sign_generator_gui_template.py`** - GUI starter template with all UI elements
- **`requirements.txt`** - Python dependencies

### 🟢 Technical Documentation
- **`claude.md`** - Technical architecture and implementation details
- **`TODO.md`** - Prioritized task list for GUI development
- **`HANDOVER.md`** - Development handover checklist
- **`project.json`** - Project configuration and metadata

### 🔵 Reference Documentation
- **`BUGS.md`** - Known issues and workarounds
- **`TESTING.md`** - Testing procedures and validation
- **`CLI_REFERENCE.md`** - Backend command reference
- **`PRINT_INSTRUCTIONS.md`** - How to use STL files in Bambu Studio
- **`README.md`** - Original project documentation

### ⚪ Utility Scripts
- **`generate_all_examples.py`** - Batch generation for testing

## 🎯 Key Requirements

### GUI Input Fields (MUST HAVE):
1. **Text to print** - Multi-line text area
2. **Label dimensions** - Width (10-500mm) and Height (5-200mm)
3. **Text heaviness** - Slider (0-100) to control boldness
4. **Bottom layer thickness** - Spinbox (0.2-5.0mm)
5. **Top layer thickness** - Spinbox (0.2-5.0mm)

### Text Heaviness Feature (PRIORITY):
The unique requirement - control how bold/heavy text appears:
- 0-25: Light weight
- 26-50: Regular weight
- 51-75: Bold weight
- 76-100: Extra Bold weight

## 💻 Implementation Path

### Phase 1: Basic GUI ⭐⭐⭐
1. Connect GUI to backend
2. Implement text heaviness mapping
3. Add input validation
4. Show status messages

### Phase 2: Enhanced UX ⭐⭐
1. Add live preview
2. Create presets
3. Progress feedback
4. File management

### Phase 3: Advanced ⭐
1. 3D preview
2. Batch processing
3. Extended options

## 🔧 Technical Stack
- **GUI Framework**: tkinter (recommended) or PyQt5
- **Backend Engine**: CadQuery (working)
- **3D Operations**: trimesh
- **Output Format**: STL files (two-layer for bi-color printing)

## ✅ Success Criteria
The GUI is complete when:
1. All 5 input fields functional
2. Text heaviness visibly affects output
3. STL files generate correctly
4. Validation prevents errors
5. Clear user feedback
6. Cross-platform operation

## 🚀 Quick Commands

### Test Backend
```bash
# Generate simple sign
python cadquery_sign_generator.py "LABEL"

# Custom parameters
python cadquery_sign_generator.py "TEST" --width 80 --height 30 --font-size 12

# Generate examples
python generate_all_examples.py
```

### Run GUI
```bash
# Launch GUI application
python sign_generator_gui_template.py
```

## 📝 Notes
- Backend is fully functional - just needs GUI wrapper
- Text heaviness is the key new feature
- Start with tkinter for simplicity
- Focus on functionality over aesthetics initially
- All documentation is in Markdown format
- STL files work with Bambu Lab P1S printer

## 🆘 Getting Help
1. Read `GUI_SPECIFICATION.md` for detailed requirements
2. Check `BUGS.md` for known issues
3. Review `TESTING.md` for validation procedures
4. See `CLI_REFERENCE.md` for backend capabilities

---
**Package Date**: 2024-09-26  
**Backend Status**: ✅ Working  
**GUI Status**: 🚧 Template Ready, Implementation Needed  
**Priority Feature**: Text Heaviness Control
