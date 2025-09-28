# Changelog

All notable changes to SignGen will be documented in this file.

## [1.0.4] - 2024-09-28

### Fixed
- **Preview vs. Generation Text Thickness Discrepancy**: Text now renders with consistent thickness between preview and generated STL files
  - Generator now utilizes CadQuery's `kind` parameter to use bold fonts for heaviness > 50
  - Preview rendering updated to match generator's exact font weights
  - Eliminated unnecessary overlay effects in preview

### Changed
- **Text Weight System Overhaul**: Refined size multipliers to account for bold font thickness
  - Light (0-25): 0.95x with regular font (increased from 0.90x)
  - Regular (26-50): 1.05x with regular font (increased from 1.00x)
  - Bold (51-75): 1.00x with bold font (reduced from 1.15x)
  - Extra Bold (76-100): 1.10x with bold font (reduced from 1.30x)
- **CadQuery Text Generation**: Added font `kind` parameter support
  - Regular font kind for weights ≤ 50
  - Bold font kind for weights > 50
  - Provides native font weight rendering

### Technical Improvements
- Added `font_kind` parameter to font params dictionary
- Generator's `_apply_text_cutout` method now passes `kind` parameter to CadQuery
- Preview font rendering simplified to rely on actual font weights
- Better consistency between preview and 3D generation through native font support

## [1.0.3] - 2024-09-27

### Fixed
- **GUI Controls Responsiveness**: All spinboxes now have command callbacks for instant updates
  - Width/Height spinboxes update preview immediately
  - Thickness spinboxes trigger preview refresh
  - Font dropdown properly bound to update events
- **Preview Text Rendering**: Better consistency between preview and generated models
  - Preview uses normal weight + size adjustment (matching generator approach)
  - Bold font weight applied for heaviness > 50
  - Subtle overlays only for extra heavy text (>80)
- **Window Layout**: Fixed preview panel cropping
  - Window width increased to 1400px
  - Canvas reduced to 400x400px
  - Proper padding on all sides (left: 10px, right: 25px)
  - Preview panel now displays symmetrically
- **Preset Buttons**: Fixed radio buttons to properly control slider
  - Corrected lambda to pass text names instead of numeric values
  - Preset values: Light=15, Regular=50, Bold=75, Extra Bold=90

### Changed
- **Slider Sensitivity**: Reduced fine-tuning effect for smoother transitions
  - Range adjustment reduced from 0.05 to 0.02 per 25-point segment
  - More gradual weight changes when moving slider
- **Grid Layout Weights**: Controls panel gets 2x weight vs preview panel
  - Better space distribution for complex controls

### Technical Improvements
- Added explicit command callbacks to all spinbox widgets
- Improved event binding for combobox selection
- Better layout padding management
- Consistent canvas dimensions throughout codebase

## [1.0.2] - 2024-09-27

### Fixed
- **Real-Time Preview Updates**: All parameter controls now trigger instant preview updates
  - Added variable tracing for width, height, font, thickness controls
  - Improved text widget handler with proper StringVar synchronization
- **Text Generation Stability**: Simplified text cutting for improved reliability
  - Removed problematic multi-cut patterns that caused geometry errors
  - All weight levels (Light/Regular/Bold/Extra Bold) now generate successfully

### Changed
- **Text Weight System**: Refined size multipliers for better visual differentiation
  - Light: 0.90x (thinner text)
  - Regular: 1.00x (normal baseline)
  - Bold: 1.15x (noticeably bolder)
  - Extra Bold: 1.30x (very bold)
- **Generation Method**: Switched to single-cut approach for all text weights
  - More reliable geometry generation
  - Eliminated "empty workpiece" errors
  - Consistent results across all heaviness settings

### Technical Improvements
- Variable tracing implementation for responsive GUI
- Simplified offset pattern system (removed complex 9-point grid)
- Better text change event handling
- Improved consistency between preview and generated models

## [1.0.1] - 2024-09-27

### Fixed
- **GUI Text Preview**: Fixed text preview not updating when typing in the text field
- **Font Size Updates**: Font size spinbox now triggers immediate preview updates
- **Text Thickness Consistency**: Regular weight text (heaviness=50) now generates with proper thickness to match preview
- **Method References**: Fixed all GUI method name mismatches that were causing startup errors
- **Preset Management**: Added missing preset management methods (load, save, delete, rename)

### Changed
- Text input now reads directly from Text widget instead of StringVar for real-time updates
- Regular weight text now uses 1.05x size multiplier for better visual consistency
- Improved offset patterns for different text weights

### Technical Improvements
- Better separation between GUI text widget and backend text processing
- More consistent text rendering between preview and generated STL files
- Enhanced event binding for all interactive controls

## [1.0.0] - 2024-09-27

### Added
- **Complete Refactored Architecture**
  - Modular design with separated concerns
  - Comprehensive validation system
  - Configuration management with JSON persistence
  - Custom exception hierarchy
  - Centralized logging system

- **Consolidated GUI Application**
  - Real-time 2D preview with accurate text rendering
  - Text weight control (0-100 slider with Light/Regular/Bold/Extra Bold presets)
  - Manual and automatic font sizing
  - Multiple sans-serif font support (platform-specific)
  - Preset management system
  - Full menu system (File, Edit, View, Help)
  - Validation feedback area
  - Debug mode toggle

- **Command-Line Interface**
  - Full parameter control via CLI
  - Batch processing support
  - Debug logging option

- **Testing Framework**
  - Unit tests for validators and config manager
  - Test structure ready for expansion

### Features
- Pre-validation to predict and prevent generation failures
- Detection of text cutting completely through layers
- Suggested parameters based on text and dimensions
- Comprehensive error messages with solutions
- Support for different text weights with multi-cut patterns
- Platform-specific font detection

### Documentation
- Comprehensive README with usage instructions
- User guide and troubleshooting in GUI
- MIT License
- Setup.py for pip installation

## [0.9.0] - 2024-09-26 (Pre-refactor)

### Initial Features
- Basic GUI with three versions (v1, v2, v3)
- CadQuery-based STL generation
- Two-layer sign design (bottom + top with text cutout)
- Basic text weight control
- Font selection
- Auto-sizing capability