# Known Issues & Bug Tracker

## 🔴 Critical Bugs

### BUG-001: Font Loading Error
**Status**: ⚠️ Workaround Available
**Severity**: Medium
**Description**: CadQuery throws "Fontconfig error: Cannot load default config file"
**Impact**: Warning message shown but generation continues
**Workaround**: Error can be safely ignored, doesn't affect output
**Fix**: Install fontconfig package or suppress warning
```bash
# Fix on Ubuntu/Debian:
sudo apt-get install fontconfig

# Or suppress in code:
import warnings
warnings.filterwarnings("ignore", message="Fontconfig")
```

## 🟡 Known Issues

### ISSUE-001: Original Generator Text Problems
**Status**: ✅ Resolved
**File**: `parametric_sign_generator.py`
**Problem**: Text not properly converted to polygons using matplotlib
**Solution**: Switched to CadQuery in `cadquery_sign_generator.py`
**Notes**: Keep old file for reference but mark as deprecated

### ISSUE-002: 3MF Import Failure
**Status**: 🔄 In Progress
**File**: `create_3mf.py`, `create_bambu_3mf.py`
**Problem**: Generated .3mf files don't import correctly in Bambu Studio
**Current Workaround**: Use two separate STL files
**Investigation Notes**:
- 3MF structure appears correct
- May be missing Bambu-specific metadata
- Need to analyze working 3MF file from Bambu Studio

### ISSUE-003: Text Width Calculation
**Status**: ✅ Fixed
**Problem**: Text extends too close to sign edges
**Solution**: Reduced font size to 8.5mm for 100mm signs
**Future**: Implement proper font metrics calculation

## 🟢 Minor Issues

### ISSUE-004: Memory Usage with Large Text
**Status**: 📝 Documented
**Impact**: Minimal
**Description**: Complex text with many characters increases memory usage
**Threshold**: >50 characters may slow generation
**Mitigation**: Implement text simplification for long strings

### ISSUE-005: Special Characters
**Status**: 🔄 Needs Testing
**Characters Affected**: 
- Emojis: Not supported
- Symbols: Limited support (-, _, ., /)
- Accented: Untested (é, ñ, ü, etc.)
**Workaround**: Stick to alphanumeric + basic punctuation

## 🔧 Platform-Specific Issues

### Windows
- Path separators need normalization
- Font paths may differ from Linux
- Unicode in filenames can cause issues

### macOS
- Untested (need feedback)
- Font locations different from Linux
- May need different CadQuery installation method

### Linux
- Working as expected on Ubuntu 24.04
- Requires additional font packages for full support

## 📊 Performance Issues

### PERF-001: Slow Generation for Complex Text
**Threshold**: >30 characters
**Time**: ~5-10 seconds
**Cause**: CadQuery text tessellation
**Optimization**: Cache font metrics

### PERF-002: Large STL Files
**Issue**: Top layer files can be >1MB
**Cause**: High mesh resolution for text
**Solution**: Add mesh decimation option

## 🐛 Bug Report Template

```markdown
### Bug Description
[Clear description of the issue]

### Steps to Reproduce
1. Run command: `python ...`
2. Enter text: "..."
3. Observe error

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Error Messages
```
[Paste any error messages]
```

### Environment
- OS: [Windows/Linux/Mac]
- Python version: 
- CadQuery version:
- Bambu Studio version:

### Additional Context
[Any other relevant information]
```

## ✅ Fixed Bugs Archive

### FIXED-001: Empty STL Files
**Date Fixed**: 2024-09-26
**Problem**: Boolean operations failing silently
**Solution**: Added fallback mesh generation
**Commit**: Added error handling in polygon_to_mesh()

### FIXED-002: Text Not Centered
**Date Fixed**: 2024-09-26  
**Problem**: Text alignment calculation incorrect
**Solution**: Fixed offset calculation in center_text()

## 🔍 Debugging Commands

### Check CadQuery Installation
```python
import cadquery as cq
print(cq.__version__)
```

### Validate STL File
```python
import trimesh
mesh = trimesh.load("file.stl")
print(f"Valid: {mesh.is_valid}")
print(f"Watertight: {mesh.is_watertight}")
print(f"Vertices: {len(mesh.vertices)}")
print(f"Faces: {len(mesh.faces)}")
```

### Test Font Availability
```python
from matplotlib import font_manager
fonts = font_manager.findSystemFonts()
print(f"Available fonts: {len(fonts)}")
print([f for f in fonts if 'arial' in f.lower()])
```

## 📝 Notes for Developers

1. Always test with both short ("TEST") and long ("ABCDEFGHIJKLMNOPQRSTUVWXYZ") text
2. Verify STL files open in multiple viewers (not just Bambu Studio)
3. Check file sizes - bottom should be ~26KB, top varies by text complexity
4. Run with different Python versions (3.8, 3.9, 3.10, 3.11)
5. Test special cases: empty text, single character, numbers only
