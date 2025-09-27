# CLI Reference - Parametric Sign Generator

## Basic Usage

```bash
python cadquery_sign_generator.py "TEXT" [OPTIONS]
```

## Current Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `text` | string | required | Text to display on sign |
| `--width` | float | 100 | Sign width in mm |
| `--height` | float | 25 | Sign height in mm |
| `--font-size` | float | 12 | Font size in mm (auto-adjusts if too large) |
| `--base-thickness` | float | 1.0 | Bottom layer thickness in mm |
| `--top-thickness` | float | 1.0 | Top layer thickness in mm |
| `--corner-radius` | float | 2.0 | Corner radius in mm (0 for square) |
| `--output` | string | "sign" | Base name for output files |

## Examples

### Simple Label
```bash
python cadquery_sign_generator.py "TOOLS"
```
Creates: `output/sign_bottom_black.stl`, `output/sign_top_yellow.stl`

### Custom Dimensions
```bash
python cadquery_sign_generator.py "MOTOR-01" --width 80 --height 30 --font-size 14
```

### Named Output
```bash
python cadquery_sign_generator.py "Threaded Inserts" --output threaded_inserts
```
Creates: `output/threaded_inserts_bottom_black.stl`, etc.

### Small Label
```bash
python cadquery_sign_generator.py "PWR" --width 30 --height 15 --font-size 10
```

### Large Sign
```bash
python cadquery_sign_generator.py "DANGER" --width 200 --height 60 --font-size 40
```

### Square Corners
```bash
python cadquery_sign_generator.py "BOX" --corner-radius 0
```

### Thin Layers
```bash
python cadquery_sign_generator.py "THIN" --base-thickness 0.6 --top-thickness 0.6
```

## Output Files

For each generation, three files are created:

1. `{output}_bottom_black.stl` - Bottom layer (solid base)
2. `{output}_top_yellow.stl` - Top layer (with text cutout)
3. `{output}_combined_preview.stl` - Both layers combined (preview only)

## Batch Processing

### Using the Example Generator
```bash
python generate_all_examples.py
```
Generates multiple predefined examples.

### Future: CSV Batch Mode (TODO)
```bash
python cadquery_sign_generator.py --batch signs.csv
```

CSV Format:
```csv
text,width,height,font_size,output
MOTOR-01,80,25,14,motor_1
MOTOR-02,80,25,14,motor_2
```

## Validation Commands (Future)

### Check Available Fonts (TODO)
```bash
python cadquery_sign_generator.py --list-fonts
```

### Validate Without Generating (TODO)
```bash
python cadquery_sign_generator.py "TEST" --validate-only
```

### Generate Preview Image (TODO)
```bash
python cadquery_sign_generator.py "TEST" --preview preview.png
```

## Error Handling

### Current Behavior
- Empty text: May crash (needs fix)
- Invalid dimensions: May produce unexpected results
- Missing font: Falls back to system default
- File write errors: Prints error message

### Planned Improvements
- Input validation before generation
- Graceful handling of edge cases
- Better error messages
- Validation mode

## Environment Variables (Future)

```bash
# Set default output directory
export SIGN_OUTPUT_DIR=/path/to/output

# Set default dimensions
export SIGN_DEFAULT_WIDTH=100
export SIGN_DEFAULT_HEIGHT=25

# Set default font
export SIGN_DEFAULT_FONT="Arial"
```

## Configuration File (Future)

`.signconfig.json`:
```json
{
  "defaults": {
    "width": 100,
    "height": 25,
    "font_size": 12,
    "font": "Arial"
  },
  "output": {
    "directory": "output",
    "prefix": "sign"
  }
}
```

## Return Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid arguments |
| 2 | File write error |
| 3 | Generation error |
| 4 | Validation error |

## Verbose Mode (Future)

```bash
# Show detailed progress
python cadquery_sign_generator.py "TEST" --verbose

# Quiet mode (errors only)
python cadquery_sign_generator.py "TEST" --quiet

# Debug mode (all output)
python cadquery_sign_generator.py "TEST" --debug
```

## Integration Examples

### Shell Script
```bash
#!/bin/bash
# generate_labels.sh

TEXTS=("MOTOR-01" "MOTOR-02" "MOTOR-03")
for text in "${TEXTS[@]}"; do
    python cadquery_sign_generator.py "$text" --output "${text,,}"
done
```

### Python Script
```python
#!/usr/bin/env python3
import subprocess

signs = [
    {"text": "TOOL BOX", "width": 80},
    {"text": "PARTS", "width": 60},
]

for sign in signs:
    cmd = ["python", "cadquery_sign_generator.py", sign["text"]]
    cmd.extend(["--width", str(sign["width"])])
    subprocess.run(cmd)
```

### Makefile
```makefile
all: motor_signs tool_signs

motor_signs:
	python cadquery_sign_generator.py "MOTOR-01" --output motor_01
	python cadquery_sign_generator.py "MOTOR-02" --output motor_02

tool_signs:
	python cadquery_sign_generator.py "DRILL" --output drill
	python cadquery_sign_generator.py "SAW" --output saw

clean:
	rm -f output/*.stl
```

## Tips & Tricks

1. **Auto Font Sizing**: Omit `--font-size` to let the generator auto-adjust
2. **Preview First**: Use combined preview STL to check appearance
3. **Standard Sizes**: 100×25mm works well for most labels
4. **Font Rule**: Keep font size at ~50% of sign height
5. **Thickness**: 1mm per layer prints quickly and is durable

## Common Issues

| Problem | Solution |
|---------|----------|
| Text too large | Reduce font size or increase width |
| Text cut off | Use auto-sizing (omit --font-size) |
| Files not created | Check write permissions in output/ |
| Import fails | Ensure both STL files are selected |
| Colors reversed | Swap material assignments in slicer |

---
*CLI Reference v1.0 - For cadquery_sign_generator.py*
