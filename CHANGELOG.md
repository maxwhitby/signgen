# Changelog

All notable changes to SignGen will be documented in this file.

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