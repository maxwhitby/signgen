"""
Core sign generator module with improved architecture
Handles STL generation with proper validation and error handling
"""

import os
from pathlib import Path
from typing import Dict, Optional, Tuple, List
import cadquery as cq

from .exceptions import STLExportError, GeometryError, FontError
from .validators import SignValidator
from .logger import get_logger


class SignGenerator:
    """Main sign generator with modular architecture"""

    def __init__(self, output_dir: str = "output", debug: bool = False):
        """Initialize sign generator

        Args:
            output_dir: Directory for output files
            debug: Enable debug logging
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger(debug)
        self.validator = SignValidator()

        # Default parameters
        self.corner_radius = 2.0
        self.default_font = "Arial"

    def generate_sign(
        self,
        text: str,
        width: float,
        height: float,
        font_family: str = "Arial",
        font_size: Optional[float] = None,
        heaviness: int = 50,
        bottom_thickness: float = 1.0,
        top_thickness: float = 1.0,
        auto_size: bool = True,
        validate: bool = True
    ) -> Dict[str, any]:
        """Generate sign with comprehensive validation and error handling

        Args:
            text: Text to display on sign
            width: Sign width in mm
            height: Sign height in mm
            font_family: Font family name
            font_size: Font size in mm (None for auto)
            heaviness: Text weight (0-100)
            bottom_thickness: Base layer thickness
            top_thickness: Top layer thickness
            auto_size: Auto-calculate font size
            validate: Whether to pre-validate parameters

        Returns:
            Dictionary with 'base', 'top', and 'combined' CadQuery workplanes

        Raises:
            ValidationError: If parameters are invalid
            GeometryError: If geometry generation fails
        """
        self.logger.info(f"Generating sign: '{text}' ({width}x{height}mm)")

        # Pre-validation if enabled
        if validate:
            self._validate_parameters(
                text, width, height, font_size, heaviness,
                bottom_thickness, top_thickness, auto_size
            )

        # Calculate font size
        if auto_size or font_size is None:
            font_size = self._calculate_auto_font_size(
                text, width, height, font_family, heaviness
            )
            self.logger.debug(f"Auto-calculated font size: {font_size:.1f}mm")

        # Apply heaviness adjustments
        font_params = self._calculate_font_params(heaviness, font_family)
        adjusted_font_size = font_size * font_params['size_multiplier']

        try:
            # Generate base layer
            base_layer = self._create_base_layer(width, height, bottom_thickness)

            # Generate top layer with text cutout
            top_layer = self._create_top_layer(
                width, height, bottom_thickness, top_thickness,
                text, font_family, adjusted_font_size, font_params
            )

            # Create combined preview
            combined = self._create_combined_preview(base_layer, top_layer)

            self.logger.info("Sign generation successful")
            return {
                'base': base_layer,
                'top': top_layer,
                'combined': combined
            }

        except Exception as e:
            self.logger.error(f"Sign generation failed: {e}")
            raise GeometryError("sign generation", str(e))

    def _validate_parameters(
        self,
        text: str,
        width: float,
        height: float,
        font_size: Optional[float],
        heaviness: int,
        bottom_thickness: float,
        top_thickness: float,
        auto_size: bool
    ):
        """Validate all parameters before generation"""
        is_valid, errors, warnings = self.validator.pre_validate_all(
            text, width, height, font_size or 12, heaviness,
            bottom_thickness, top_thickness, auto_size
        )

        # Log warnings
        for warning in warnings:
            self.logger.warning(warning)

        # Raise exception for errors
        if not is_valid:
            from .exceptions import ValidationError
            raise ValidationError("parameters", "; ".join(errors))

        # Check if text will cut through
        if font_size:
            will_cut, confidence = self.validator.will_text_cut_through(
                text, font_size, heaviness, width, height, top_thickness
            )
            if will_cut and confidence > 70:
                self.logger.warning(
                    f"Text may cut through top layer (confidence: {confidence}%). "
                    "Consider reducing font size or heaviness."
                )

    def _calculate_auto_font_size(
        self,
        text: str,
        width: float,
        height: float,
        font_family: str,
        heaviness: int
    ) -> float:
        """Calculate optimal font size for text to fit within dimensions"""
        # Font-specific width factors
        font_widths = {
            'Impact': 0.45,
            'Arial': 0.55,
            'Arial Black': 0.65,
            'Helvetica': 0.55,
            'Verdana': 0.65,
            'Tahoma': 0.60,
            'Trebuchet MS': 0.58,
            'Gill Sans': 0.52,
            'Futura': 0.60,
        }

        width_factor = font_widths.get(font_family, 0.55)
        width_factor += (heaviness / 100) * 0.15  # Adjust for heaviness

        # Calculate based on width constraint
        max_text_width = width * 0.75  # Leave 25% margin
        font_size_width = max_text_width / (len(text) * width_factor)

        # Calculate based on height constraint
        font_size_height = height * 0.6  # Leave 40% margin

        # Use the smaller to ensure fit
        font_size = min(font_size_width, font_size_height)

        # Clamp to reasonable range
        return max(5.0, min(font_size, 50.0))

    def _calculate_font_params(self, heaviness: int, font_family: str) -> dict:
        """Calculate font parameters based on heaviness and family"""
        params = {
            'font_family': font_family,
            'size_multiplier': 1.0,
            'stroke_offset': 0.0,
            'cut_depth_multiplier': 1.0,
            'style': 'Regular'
        }

        if heaviness <= 25:
            params.update({
                'size_multiplier': 0.90,  # Thin text
                'stroke_offset': 0.0,
                'style': 'Light'
            })
        elif heaviness <= 50:
            params.update({
                'size_multiplier': 1.00,  # Normal size
                'stroke_offset': 0.0,
                'style': 'Regular'
            })
        elif heaviness <= 75:
            params.update({
                'size_multiplier': 1.15,  # Noticeably bolder
                'stroke_offset': 0.0,
                'style': 'Bold'
            })
        else:
            params.update({
                'size_multiplier': 1.30,  # Very bold
                'stroke_offset': 0.0,
                'style': 'ExtraBold'
            })

        # Fine-tune within range
        range_position = (heaviness % 25) / 25.0
        params['size_multiplier'] += range_position * 0.05

        return params

    def _create_base_layer(
        self,
        width: float,
        height: float,
        thickness: float
    ) -> cq.Workplane:
        """Create the base layer geometry"""
        base = (
            cq.Workplane("XY")
            .rect(width, height)
            .extrude(thickness)
        )

        if self.corner_radius > 0:
            base = base.edges("|Z").fillet(self.corner_radius)

        return base

    def _create_top_layer(
        self,
        width: float,
        height: float,
        bottom_thickness: float,
        top_thickness: float,
        text: str,
        font_family: str,
        font_size: float,
        font_params: dict
    ) -> cq.Workplane:
        """Create the top layer with text cutout"""
        # Create top layer base
        top = (
            cq.Workplane("XY")
            .workplane(offset=bottom_thickness)
            .rect(width, height)
            .extrude(top_thickness)
        )

        if self.corner_radius > 0:
            top = top.edges("|Z").fillet(self.corner_radius)

        # Apply text cutout
        top = self._apply_text_cutout(
            top, text, font_family, font_size, font_params, top_thickness
        )

        # Validate result
        if not self._validate_geometry(top):
            raise GeometryError(
                "top layer creation",
                "Text cutout may have removed all material"
            )

        return top

    def _apply_text_cutout(
        self,
        workpiece: cq.Workplane,
        text: str,
        font_family: str,
        font_size: float,
        font_params: dict,
        thickness: float
    ) -> cq.Workplane:
        """Apply text cutout with heaviness effects"""
        cut_depth = thickness * font_params['cut_depth_multiplier'] * 1.1

        # Use single cut for all styles - rely on size multiplier for thickness
        # Multi-cut patterns were causing geometry issues
        workpiece = (
            workpiece
            .faces(">Z")
            .workplane()
            .text(
                text,
                font_size,
                -cut_depth,
                font=font_family,
                halign="center",
                valign="center"
            )
        )

        return workpiece

    def _get_offset_pattern(self, style: str, offset: float) -> List[Tuple[float, float]]:
        """Get offset pattern for text effects"""
        if style == 'Light':
            # No offset for Light text
            return [(0, 0)]
        elif style == 'Regular':
            # No offset for Regular text to keep it clean
            return [(0, 0)]
        elif style == 'Bold':
            # 5-point pattern for Bold
            return [
                (0, 0),
                (offset, 0),
                (-offset, 0),
                (0, offset),
                (0, -offset)
            ]
        else:  # ExtraBold
            # 7-point pattern for ExtraBold (reduced from 9 to prevent over-cutting)
            return [
                (0, 0),
                (offset, 0),
                (-offset, 0),
                (0, offset),
                (0, -offset),
                (offset * 0.7, offset * 0.7),
                (-offset * 0.7, -offset * 0.7)
            ]

    def _create_combined_preview(
        self,
        base: cq.Workplane,
        top: cq.Workplane
    ) -> cq.Workplane:
        """Create combined preview model"""
        try:
            combined = base.union(top)
            return combined
        except Exception as e:
            self.logger.warning(f"Union operation failed: {e}")
            return base  # Return base as fallback

    def _validate_geometry(self, workpiece: cq.Workplane) -> bool:
        """Validate that geometry has valid solids"""
        try:
            if hasattr(workpiece, 'val'):
                result = workpiece.val()
                return result is not None
            return True
        except:
            return False

    def export_stl(
        self,
        models: Dict[str, cq.Workplane],
        base_filename: str,
        metadata: Optional[Dict[str, any]] = None
    ) -> List[str]:
        """Export models to STL files with validation

        Args:
            models: Dictionary of CadQuery models
            base_filename: Base name for output files
            metadata: Optional metadata for file naming

        Returns:
            List of successfully created file paths

        Raises:
            STLExportError: If export fails
        """
        created_files = []
        metadata = metadata or {}

        # Determine weight label
        heaviness = metadata.get('heaviness', 50)
        weight_label = self._get_weight_label(heaviness)

        # Clean filename
        safe_name = self._sanitize_filename(base_filename)

        # Export each model
        for layer_name, model in models.items():
            if model is None:
                continue

            # Generate filename
            if layer_name == 'base':
                filename = f"{safe_name}_{weight_label}_bottom_black.stl"
            elif layer_name == 'top':
                filename = f"{safe_name}_{weight_label}_top_yellow.stl"
            elif layer_name == 'combined':
                filename = f"{safe_name}_{weight_label}_combined_preview.stl"
            else:
                continue

            filepath = self.output_dir / filename

            # Export with validation
            success = self._export_single_stl(model, filepath, layer_name)
            if success:
                created_files.append(str(filepath))

        return created_files

    def _export_single_stl(
        self,
        model: cq.Workplane,
        filepath: Path,
        layer_name: str
    ) -> bool:
        """Export a single STL file with comprehensive validation"""
        try:
            # Validate geometry first
            if not self._validate_geometry(model):
                self.logger.error(f"{layer_name} has invalid geometry")
                raise STLExportError(
                    layer_name,
                    "Invalid geometry",
                    ["Check text size", "Reduce heaviness", "Increase layer thickness"]
                )

            # Attempt export
            cq.exporters.export(model, str(filepath))

            # Verify file was created and has content
            if not filepath.exists():
                raise STLExportError(
                    layer_name,
                    "File not created",
                    ["Try different parameters", "Check disk space"]
                )

            if filepath.stat().st_size == 0:
                filepath.unlink()  # Remove empty file
                raise STLExportError(
                    layer_name,
                    "Empty file created",
                    ["Text may have cut through entirely", "Adjust parameters"]
                )

            self.logger.info(f"Successfully exported: {filepath.name}")
            return True

        except STLExportError:
            raise
        except Exception as e:
            self.logger.error(f"Export failed for {layer_name}: {e}")
            raise STLExportError(
                layer_name,
                str(e),
                ["Check parameters", "Try simpler text"]
            )

    def _get_weight_label(self, heaviness: int) -> str:
        """Get weight label from heaviness value"""
        if heaviness <= 25:
            return "light"
        elif heaviness <= 50:
            return "regular"
        elif heaviness <= 75:
            return "bold"
        else:
            return "extrabold"

    def _sanitize_filename(self, text: str) -> str:
        """Sanitize text for use in filename"""
        # Remove or replace problematic characters
        safe_chars = "".join(
            c if c.isalnum() or c in (' ', '-', '_') else '_'
            for c in text
        )
        # Limit length and clean up
        return safe_chars[:30].strip().replace(' ', '_') or 'sign'