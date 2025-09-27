# Threaded Inserts Sign - Print Instructions

## Your STL Files Are Ready!

### Files to Download:
1. **ThreadedInserts_Bottom_White.stl** - Bottom layer (1mm thick)
2. **ThreadedInserts_Top_Yellow.stl** - Top layer with text cutout (1mm thick)

## Sign Specifications:
- **Text**: "Threaded Inserts" (with space)
- **Dimensions**: 100mm × 25mm × 2mm total
- **Font Size**: 8.5mm (properly sized with good margins)
- **Layer Thickness**: 1mm each layer

## Bambu Studio Setup Instructions:

### Step 1: Import Files
1. Open Bambu Studio
2. Click "Import" (or press Ctrl+I)
3. Select **both STL files** at once (hold Ctrl while selecting)
4. Click "Open"

### Step 2: Assign Materials
1. Click on the **bottom layer** object (solid rectangle)
   - In the right panel, set "Filament" to **Spool 1** (White)
   
2. Click on the **top layer** object (rectangle with text cutout)
   - In the right panel, set "Filament" to **Spool 4** (Yellow)

### Step 3: Align Objects (Important!)
1. Select both objects (Ctrl+A)
2. Right-click → "Assemble" 
   OR
3. Use the "Assembly" tool in the toolbar
   - This ensures perfect alignment at (0,0,0)

### Step 4: Recommended Print Settings
- **Layer Height**: 0.2mm
- **Initial Layer**: 0.2mm
- **Infill Density**: 20%
- **Infill Pattern**: Grid or Gyroid
- **Print Speed**: Standard or Quality preset
- **Support**: None needed
- **Bed Temperature**: 60°C (PLA)
- **Nozzle Temperature**: 220°C (PLA)

### Step 5: Slice and Print
1. Click "Slice plate"
2. Review the preview (should show color changes)
3. Click "Print" to send to printer

## AMS (Automatic Material System) Setup:
- **Slot 1**: White PLA
- **Slot 4**: Yellow PLA

The AMS will automatically handle the filament changes.

## Manual Color Change Option:
If not using AMS:
1. Import only the bottom layer first
2. Print in white
3. Then import and print the top layer in yellow
4. OR use the "Change filament" pause in the slicer

## Expected Result:
- White text showing through yellow background
- Clean, professional appearance
- Perfect for labeling bins, tools, or equipment

## Troubleshooting:
- **If objects don't align**: Use "Assembly" or manually set both to position (0,0,0)
- **If colors are reversed**: Swap the filament assignments
- **If text is too thin**: Check that you're using the correct files (8.5mm font version)

---
Files generated with CadQuery-based Parametric Sign Generator
Ready for Bambu Lab P1S 3D Printer
