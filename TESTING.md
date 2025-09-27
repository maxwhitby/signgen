# Testing Guide - Parametric Sign Generator

## Quick Test Suite

### 1. Basic Functionality Test
```bash
# Test basic generation
python cadquery_sign_generator.py "TEST" --width 60 --height 20 --font-size 14 --output test_basic

# Verify files exist
ls -lh output/test_basic*.stl

# Expected: 3 files created
# - test_basic_bottom_black.stl (~26KB)
# - test_basic_top_yellow.stl (>100KB)
# - test_basic_combined_preview.stl
```

### 2. Edge Cases Test
```bash
# Single character
python cadquery_sign_generator.py "A" --width 30 --height 30 --font-size 20

# Long text
python cadquery_sign_generator.py "ABCDEFGHIJKLMNOPQRSTUVWXYZ" --width 200 --height 30

# Numbers and symbols
python cadquery_sign_generator.py "123-456" --width 80 --height 25

# Empty text (should fail gracefully)
python cadquery_sign_generator.py "" --width 100 --height 25
```

### 3. Dimension Tests
```bash
# Minimum practical size
python cadquery_sign_generator.py "MIN" --width 20 --height 10 --font-size 5

# Large size
python cadquery_sign_generator.py "LARGE" --width 300 --height 100 --font-size 50

# Aspect ratios
python cadquery_sign_generator.py "WIDE" --width 150 --height 20
python cadquery_sign_generator.py "TALL" --width 30 --height 80
```

## Validation Tests

### STL File Validation
```python
#!/usr/bin/env python3
"""validate_stl.py - Validate generated STL files"""

import trimesh
import sys

def validate_stl(filename):
    """Check if STL file is valid for 3D printing"""
    try:
        mesh = trimesh.load(filename)
        
        print(f"File: {filename}")
        print(f"  Valid: {mesh.is_valid}")
        print(f"  Watertight: {mesh.is_watertight}")
        print(f"  Vertices: {len(mesh.vertices)}")
        print(f"  Faces: {len(mesh.faces)}")
        print(f"  Volume: {mesh.volume:.2f} mm³")
        print(f"  Bounds: {mesh.bounds.tolist()}")
        
        # Check for common issues
        if not mesh.is_watertight:
            print("  ⚠️ WARNING: Mesh is not watertight!")
        
        if mesh.volume < 1:
            print("  ⚠️ WARNING: Volume suspiciously small!")
            
        if len(mesh.vertices) < 4:
            print("  ❌ ERROR: Not enough vertices!")
            return False
            
        return mesh.is_valid
        
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_stl(sys.argv[1])
    else:
        # Validate all STL files in output directory
        import glob
        for stl in glob.glob("output/*.stl"):
            validate_stl(stl)
            print("-" * 40)
```

### Visual Inspection Test
```python
#!/usr/bin/env python3
"""preview_stl.py - Generate preview images of STL files"""

import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def preview_stl(filename, output_image=None):
    """Create a preview image of the STL file"""
    mesh = trimesh.load(filename)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the mesh
    ax.add_collection3d(mesh.as_open3d())
    
    # Set the aspect ratio
    ax.set_box_aspect(aspect=mesh.extents)
    
    # Labels
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title(f'STL Preview: {filename}')
    
    if output_image:
        plt.savefig(output_image)
        print(f"Saved preview: {output_image}")
    else:
        plt.show()

# Usage
preview_stl("output/test_basic_combined_preview.stl", "preview.png")
```

## Performance Tests

### Benchmark Script
```python
#!/usr/bin/env python3
"""benchmark.py - Test generation performance"""

import time
import subprocess
import statistics

def benchmark_generation(text, runs=5):
    """Measure generation time"""
    times = []
    
    for i in range(runs):
        start = time.time()
        subprocess.run([
            "python", "cadquery_sign_generator.py",
            text, "--output", f"bench_{i}"
        ], capture_output=True)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"Run {i+1}: {elapsed:.2f}s")
    
    print(f"\nResults for '{text}':")
    print(f"  Average: {statistics.mean(times):.2f}s")
    print(f"  Min: {min(times):.2f}s")
    print(f"  Max: {max(times):.2f}s")
    print(f"  Std Dev: {statistics.stdev(times):.2f}s")

# Test different text lengths
benchmark_generation("TEST")
benchmark_generation("MOTOR-01")
benchmark_generation("THREADED INSERTS")
benchmark_generation("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
```

## Integration Tests

### Bambu Studio Import Test
1. Generate test files:
   ```bash
   python cadquery_sign_generator.py "IMPORT TEST" --output import_test
   ```

2. Manual steps in Bambu Studio:
   - [ ] File → Import → Select both STL files
   - [ ] Check objects appear correctly
   - [ ] Verify objects can be selected individually
   - [ ] Test "Assemble" function works
   - [ ] Assign different colors
   - [ ] Slice successfully
   - [ ] Preview shows color changes

### Print Test Checklist
- [ ] Files slice without errors
- [ ] Print time estimate reasonable (<30 minutes)
- [ ] Material usage reasonable (<5g total)
- [ ] First layer adheres properly
- [ ] Color change occurs at correct layer
- [ ] Text is legible
- [ ] Dimensions match specifications
- [ ] No warping or separation

## Regression Tests

### Test Historical Bugs Don't Reappear
```bash
#!/bin/bash
# regression_test.sh

echo "Running regression tests..."

# Test 1: Empty text handling (used to crash)
python cadquery_sign_generator.py "" --output regression_1 2>/dev/null
if [ $? -eq 0 ]; then
    echo "❌ FAIL: Empty text should be rejected"
else
    echo "✅ PASS: Empty text properly rejected"
fi

# Test 2: Text cutout exists (original bug)
python cadquery_sign_generator.py "TEST" --output regression_2
SIZE_BOTTOM=$(stat -c%s output/regression_2_bottom_black.stl 2>/dev/null || stat -f%z output/regression_2_bottom_black.stl 2>/dev/null)
SIZE_TOP=$(stat -c%s output/regression_2_top_yellow.stl 2>/dev/null || stat -f%z output/regression_2_top_yellow.stl 2>/dev/null)

if [ $SIZE_TOP -gt $SIZE_BOTTOM ]; then
    echo "✅ PASS: Text cutout present (top layer larger)"
else
    echo "❌ FAIL: Text cutout missing"
fi

# Test 3: Auto font sizing works
python cadquery_sign_generator.py "VERYLONGTEXTTHATWOULDOVERFLOW" --width 100 --output regression_3
if [ -f "output/regression_3_top_yellow.stl" ]; then
    echo "✅ PASS: Long text handled"
else
    echo "❌ FAIL: Long text generation failed"
fi
```

## Unit Tests

### test_generator.py
```python
#!/usr/bin/env python3
"""Unit tests for sign generator"""

import unittest
import os
import sys
sys.path.append('..')
from cadquery_sign_generator import CadQuerySignGenerator

class TestSignGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = CadQuerySignGenerator()
        
    def test_default_parameters(self):
        """Test default initialization"""
        self.assertEqual(self.generator.sign_width, 100)
        self.assertEqual(self.generator.sign_height, 25)
        self.assertEqual(self.generator.font_size, 12)
        
    def test_dimension_update(self):
        """Test parameter updates"""
        models = self.generator.generate_sign(
            text="TEST",
            sign_width=80,
            sign_height=30
        )
        self.assertIsNotNone(models)
        
    def test_file_creation(self):
        """Test STL file generation"""
        models = self.generator.generate_sign("TEST")
        files = self.generator.save_stl(models, "unittest")
        
        for file in files:
            self.assertTrue(os.path.exists(file))
            self.assertGreater(os.path.getsize(file), 0)
            
    def test_text_validation(self):
        """Test text input validation"""
        # Should handle empty text gracefully
        models = self.generator.generate_sign("")
        self.assertIsNotNone(models)
        
    def test_auto_sizing(self):
        """Test automatic font sizing"""
        self.generator.sign_width = 50
        models = self.generator.generate_sign(
            "VERY LONG TEXT",
            auto_size=True
        )
        # Font should be reduced
        self.assertLess(self.generator.font_size, 12)

if __name__ == '__main__':
    unittest.main()
```

## Continuous Testing

### GitHub Actions Workflow (future)
```yaml
name: Test Sign Generator

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        
    - name: Run unit tests
      run: |
        python -m pytest tests/
        
    - name: Run integration tests
      run: |
        ./regression_test.sh
        
    - name: Check code quality
      run: |
        flake8 *.py
        black --check *.py
```

## Test Data

### Standard Test Cases
| Text | Width | Height | Font | Expected Result |
|------|-------|--------|------|-----------------|
| TEST | 60 | 20 | 14 | Success |
| A | 20 | 20 | 15 | Success |
| 123-456 | 80 | 25 | 12 | Success |
| "" | 100 | 25 | 12 | Graceful failure |
| "ABC DEF" | 100 | 25 | 12 | Success with space |
| MOTOR-01 | 80 | 25 | 14 | Success |
| Ñoño | 60 | 20 | 12 | Check special chars |

### Stress Test Cases
- Text with 100+ characters
- Width < 10mm
- Height < 5mm
- Font size > height
- Negative dimensions (should fail)
- Non-ASCII characters
- Very large dimensions (>500mm)

## Testing Schedule
- **Before each commit**: Run quick test suite
- **Before release**: Full test suite + manual Bambu Studio test
- **Weekly**: Performance benchmarks
- **Monthly**: Print physical test samples
