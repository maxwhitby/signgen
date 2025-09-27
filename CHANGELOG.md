# Changelog

All notable changes to SignGen will be documented in this file.

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