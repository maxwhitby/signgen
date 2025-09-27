#!/usr/bin/env python3
"""
Enhanced backend for GUI sign generator with text heaviness control
Extends the CadQuery sign generator to support variable text weight/boldness
"""

import cadquery as cq
import os
from cadquery_sign_generator import CadQuerySignGenerator


class EnhancedSignGenerator(CadQuerySignGenerator):
    """Extended sign generator with text heaviness control"""

    def __init__(self):
        super().__init__()
        self.text_heaviness = 50  # Default regular weight (0-100 scale)
        self.stroke_width = 0  # Additional stroke width for bold effect
        self.font_family = "Arial"  # Default font


class EnhancedSignGeneratorWithFonts(EnhancedSignGenerator):
    """Extended sign generator with font selection and text heaviness control"""

    def __init__(self):
        super().__init__()

    def generate_sign_with_font(self, text=None, font_family="Arial", sign_width=None,
                                sign_height=None, font_size=None, heaviness=50,
                                bottom_thickness=1.0, top_thickness=1.0, auto_size=True):
        """
        Generate sign with font selection and text heaviness control

        Args:
            text: Text to display
            font_family: Font name (e.g., "Arial", "Helvetica", "Impact")
            sign_width: Width in mm
            sign_height: Height in mm
            font_size: Base font size in mm
            heaviness: Text weight (0-100)
            bottom_thickness: Bottom layer thickness in mm
            top_thickness: Top layer thickness in mm
            auto_size: Auto-adjust font size to fit
        """

        # Store font family
        self.font_family = font_family

        # Update parameters
        if text:
            self.text = text
        if sign_width:
            self.sign_width = sign_width
        if sign_height:
            self.sign_height = sign_height
        if font_size:
            self.font_size = font_size

        self.base_thickness = bottom_thickness
        self.top_thickness = top_thickness
        self.text_heaviness = heaviness

        # Calculate font adjustments based on heaviness
        font_params = self.calculate_font_params_with_font(heaviness, font_family)

        # Handle font size based on auto_size setting
        if not auto_size and font_size is not None:
            # Manual font size mode
            adjusted_font_size = font_size * font_params['size_multiplier']
            print(f"Using manual font size: {font_size:.1f}mm with {font_family}")
        else:
            # Auto-size mode
            base_font_size = font_size if font_size else self.font_size
            adjusted_font_size = base_font_size * font_params['size_multiplier']

            if auto_size:
                # Account for font-specific widths
                width_factor = font_params['width_factor'] + (heaviness / 100) * 0.15
                estimated_width = len(self.text) * adjusted_font_size * width_factor

                if font_size is not None:
                    max_text_width = self.sign_width * 0.90
                else:
                    max_text_width = self.sign_width * 0.75

                if estimated_width > max_text_width:
                    adjusted_font_size = max_text_width / (len(self.text) * width_factor)
                    print(f"Auto-adjusted {font_family} font size to {adjusted_font_size:.1f}mm")

        print(f"Generating sign: '{self.text}'")
        print(f"Font: {font_family}, Size: {adjusted_font_size:.1f}mm, Heaviness: {heaviness}")
        print(f"Sign dimensions: {self.sign_width}mm x {self.sign_height}mm")

        # Create the base layer
        base_layer = (
            cq.Workplane("XY")
            .rect(self.sign_width, self.sign_height)
            .extrude(self.base_thickness)
        )

        # Add rounded corners
        if self.corner_radius > 0:
            base_layer = base_layer.edges("|Z").fillet(self.corner_radius)

        # Create the top layer
        top_layer = (
            cq.Workplane("XY")
            .workplane(offset=self.base_thickness)
            .rect(self.sign_width, self.sign_height)
            .extrude(self.top_thickness)
        )

        # Add rounded corners to top layer
        if self.corner_radius > 0:
            top_layer = top_layer.edges("|Z").fillet(self.corner_radius)

        # Apply text with selected font and heaviness
        top_layer = self.apply_text_with_font_and_heaviness(
            top_layer,
            self.text,
            adjusted_font_size,
            font_params,
            font_family
        )

        # Verify top layer still has geometry
        try:
            if not top_layer.val():
                print("Warning: Top layer has no geometry after text cutting")
        except:
            pass

        # Create combined model
        try:
            combined = base_layer.union(top_layer)
        except Exception as e:
            print(f"Warning: Union operation failed: {e}")
            print("Using base layer as combined preview")
            combined = base_layer

        return {
            'base': base_layer,
            'top': top_layer,
            'combined': combined
        }

    def calculate_font_params_with_font(self, heaviness, font_family):
        """Calculate font parameters based on heaviness and font family"""

        # Get base parameters from heaviness
        params = self.calculate_font_params(heaviness)

        # Font-specific width factors
        font_widths = {
            'Impact': 0.45,
            'Arial': 0.55,
            'Arial Black': 0.65,
            'Helvetica': 0.55,
            'Helvetica Neue': 0.52,
            'Verdana': 0.65,
            'Tahoma': 0.60,
            'Calibri': 0.52,
            'Trebuchet MS': 0.58,
            'Comic Sans MS': 0.60,
            'Gill Sans': 0.52,
            'Avenir': 0.58,
            'Futura': 0.60,
            'SF Pro Display': 0.55,
            'Roboto': 0.56,
            'Open Sans': 0.58,
            'Montserrat': 0.62,
        }

        params['width_factor'] = font_widths.get(font_family, 0.55)
        params['font_family'] = font_family

        return params

    def apply_text_with_font_and_heaviness(self, workpiece, text, font_size, font_params, font_family):
        """Apply text cutout with specific font and heaviness"""

        cut_depth = self.top_thickness * font_params['cut_depth_multiplier'] * 1.1

        # Multi-cut technique for bold text
        if font_params['style'] in ['Bold', 'ExtraBold']:
            base_offset = font_params['stroke_offset']

            if font_params['style'] == 'Bold':
                offset_patterns = [
                    (0, 0),
                    (base_offset, 0),
                    (-base_offset, 0),
                    (0, base_offset),
                    (0, -base_offset),
                ]
            else:  # ExtraBold
                offset_patterns = []
                for dx in [-base_offset, 0, base_offset]:
                    for dy in [-base_offset, 0, base_offset]:
                        offset_patterns.append((dx, dy))

            # Apply all offset cuts with selected font
            for dx, dy in offset_patterns:
                try:
                    workpiece = (
                        workpiece
                        .faces(">Z")
                        .workplane()
                        .center(dx, dy)
                        .text(
                            text,
                            font_size,
                            -cut_depth,
                            font=font_family,  # Use selected font
                            halign="center",
                            valign="center",
                            fontPath=None
                        )
                        .center(-dx, -dy)
                    )
                except:
                    pass

        else:
            # Regular or light text - single cut
            workpiece = (
                workpiece
                .faces(">Z")
                .workplane()
                .text(
                    text,
                    font_size,
                    -cut_depth,
                    font=font_family,  # Use selected font
                    halign="center",
                    valign="center",
                    fontPath=None
                )
            )

        return workpiece

    def save_with_metadata(self, models, output_name, heaviness, font_family):
        """Save STL files with font and heaviness metadata"""

        os.makedirs("output", exist_ok=True)

        # Determine weight label
        if heaviness <= 25:
            weight_label = "light"
        elif heaviness <= 50:
            weight_label = "regular"
        elif heaviness <= 75:
            weight_label = "bold"
        else:
            weight_label = "extrabold"

        # Clean font name for filename
        font_label = font_family.lower().replace(' ', '_')

        files_created = []

        # Export base layer
        if 'base' in models and models['base'] is not None:
            filename = f"output/{output_name}_{weight_label}_bottom_black.stl"
            try:
                cq.exporters.export(models['base'], filename)
                print(f"✓ Saved: {filename}")
                files_created.append(filename)
            except Exception as e:
                print(f"✗ Failed to save base layer: {e}")

        # Export top layer
        if 'top' in models and models['top'] is not None:
            filename = f"output/{output_name}_{weight_label}_top_yellow.stl"
            try:
                # Check if top layer has valid solids before attempting export
                if hasattr(models['top'], 'val'):
                    result = models['top'].val()
                    if result is None:
                        print(f"✗ Top layer has no valid geometry - text may have cut through entirely")
                    else:
                        cq.exporters.export(models['top'], filename)
                        # Verify file was actually created
                        if os.path.exists(filename):
                            size = os.path.getsize(filename)
                            if size > 0:
                                print(f"✓ Saved: {filename}")
                                files_created.append(filename)
                            else:
                                print(f"✗ Top layer file is empty (0 bytes): {filename}")
                                os.remove(filename)  # Remove empty file
                        else:
                            print(f"✗ Top layer export silently failed - no file created")
                            print(f"  This usually happens when text cuts completely through the layer")
                            print(f"  Try: reducing font size, reducing text heaviness, or increasing top thickness")
                else:
                    cq.exporters.export(models['top'], filename)
                    if os.path.exists(filename):
                        print(f"✓ Saved: {filename}")
                        files_created.append(filename)
            except Exception as e:
                print(f"✗ Failed to save top layer: {e}")
                print(f"  This usually means the text cut through the entire layer")

        # Export combined preview
        if 'combined' in models and models['combined'] is not None:
            filename = f"output/{output_name}_{weight_label}_combined_preview.stl"
            try:
                cq.exporters.export(models['combined'], filename)
                print(f"✓ Saved: {filename}")
                files_created.append(filename)
            except Exception as e:
                print(f"✗ Failed to save combined preview: {e}")

        return files_created

    def generate_sign_with_heaviness(self, text=None, sign_width=None, sign_height=None,
                                     font_size=None, heaviness=50, bottom_thickness=1.0,
                                     top_thickness=1.0, auto_size=True):
        """
        Generate sign with text heaviness control

        Args:
            text: Text to display
            sign_width: Width in mm
            sign_height: Height in mm
            font_size: Base font size in mm
            heaviness: Text weight (0-100, where 0=light, 50=regular, 100=extra bold)
            bottom_thickness: Bottom layer thickness in mm
            top_thickness: Top layer thickness in mm
            auto_size: Auto-adjust font size to fit
        """

        # Update parameters
        if text:
            self.text = text
        if sign_width:
            self.sign_width = sign_width
        if sign_height:
            self.sign_height = sign_height
        if font_size:
            self.font_size = font_size

        self.base_thickness = bottom_thickness
        self.top_thickness = top_thickness
        self.text_heaviness = heaviness

        # Calculate font adjustments based on heaviness
        font_params = self.calculate_font_params(heaviness)

        # Handle font size based on auto_size setting
        if not auto_size and font_size is not None:
            # Manual font size mode - use the provided font size directly
            adjusted_font_size = font_size * font_params['size_multiplier']
            print(f"Using manual font size: {font_size:.1f}mm (adjusted to {adjusted_font_size:.1f}mm for heaviness)")
        else:
            # Auto-size mode or no font size provided
            base_font_size = font_size if font_size else self.font_size
            adjusted_font_size = base_font_size * font_params['size_multiplier']

            # Auto-adjust to fit width
            if auto_size:
                # Account for heavier text taking more space
                width_factor = 0.55 + (heaviness / 100) * 0.15  # Heavier text is wider
                estimated_width = len(self.text) * adjusted_font_size * width_factor

                # Use more of the available width when manual control is desired
                if font_size is not None:
                    max_text_width = self.sign_width * 0.90  # Use 90% when font size is specified
                else:
                    max_text_width = self.sign_width * 0.75  # Default 75% margin

                if estimated_width > max_text_width:
                    adjusted_font_size = max_text_width / (len(self.text) * width_factor)
                    print(f"Auto-adjusted font size to {adjusted_font_size:.1f}mm for heaviness {heaviness}")

        print(f"Generating sign: '{self.text}'")
        print(f"Sign dimensions: {self.sign_width}mm x {self.sign_height}mm")
        print(f"Font size: {adjusted_font_size:.1f}mm, Heaviness: {heaviness}")
        print(f"Layer thicknesses: Bottom={self.base_thickness}mm, Top={self.top_thickness}mm")

        # Create the base layer
        base_layer = (
            cq.Workplane("XY")
            .rect(self.sign_width, self.sign_height)
            .extrude(self.base_thickness)
        )

        # Add rounded corners
        if self.corner_radius > 0:
            base_layer = base_layer.edges("|Z").fillet(self.corner_radius)

        # Create the top layer
        top_layer = (
            cq.Workplane("XY")
            .workplane(offset=self.base_thickness)
            .rect(self.sign_width, self.sign_height)
            .extrude(self.top_thickness)
        )

        # Add rounded corners to top layer
        if self.corner_radius > 0:
            top_layer = top_layer.edges("|Z").fillet(self.corner_radius)

        # Apply text with heaviness adjustments
        top_layer = self.apply_text_with_heaviness(
            top_layer,
            self.text,
            adjusted_font_size,
            font_params
        )

        # Create combined model for preview
        # Note: union might fail if text cuts through entire layer
        try:
            combined = base_layer.union(top_layer)
        except:
            # If union fails, just use base layer as combined
            combined = base_layer

        return {
            'base': base_layer,
            'top': top_layer,
            'combined': combined
        }

    def calculate_font_params(self, heaviness):
        """
        Calculate font parameters based on heaviness value

        Args:
            heaviness: 0-100 value (0=lightest, 100=heaviest)

        Returns:
            dict with font parameters
        """
        params = {}

        if heaviness <= 25:
            # Light weight
            params['font_name'] = 'Arial'
            params['size_multiplier'] = 0.95
            params['stroke_offset'] = -0.05  # Negative makes thinner
            params['cut_depth_multiplier'] = 1.0
            params['style'] = 'Light'

        elif heaviness <= 50:
            # Regular weight
            params['font_name'] = 'Arial'
            params['size_multiplier'] = 1.0
            params['stroke_offset'] = 0.0
            params['cut_depth_multiplier'] = 1.0
            params['style'] = 'Regular'

        elif heaviness <= 75:
            # Bold weight
            params['font_name'] = 'Arial'
            params['size_multiplier'] = 1.12  # Increased from 1.08
            params['stroke_offset'] = 0.3  # Increased from 0.1
            params['cut_depth_multiplier'] = 1.05
            params['style'] = 'Bold'

        else:
            # Extra bold weight
            params['font_name'] = 'Arial'
            params['size_multiplier'] = 1.25  # Increased from 1.15
            params['stroke_offset'] = 0.5  # Increased from 0.2
            params['cut_depth_multiplier'] = 1.1
            params['style'] = 'ExtraBold'

        # Continuous adjustment within ranges
        range_position = (heaviness % 25) / 25.0  # 0 to 1 within each range

        # Fine-tune the multiplier based on exact position
        fine_adjust = range_position * 0.05
        params['size_multiplier'] += fine_adjust

        return params

    def apply_text_with_heaviness(self, workpiece, text, font_size, font_params):
        """
        Apply text cutout with heaviness adjustments

        This method attempts to simulate text weight by:
        1. Adjusting the font size
        2. Using multiple cuts with slight offsets for bold effect
        3. Adjusting cut depth
        """

        cut_depth = self.top_thickness * font_params['cut_depth_multiplier'] * 1.1

        # For heavy text, we can try a multi-cut technique
        if font_params['style'] in ['Bold', 'ExtraBold']:
            # Calculate offset based on stroke_offset parameter
            base_offset = font_params['stroke_offset']

            if font_params['style'] == 'Bold':
                # Bold: 4-way offset pattern
                offset_patterns = [
                    (0, 0),  # Center
                    (base_offset, 0),  # Right
                    (-base_offset, 0),  # Left
                    (0, base_offset),  # Up
                    (0, -base_offset),  # Down
                ]
            else:  # ExtraBold
                # Extra Bold: 9-way grid pattern for maximum thickness
                offset_patterns = []
                for dx in [-base_offset, 0, base_offset]:
                    for dy in [-base_offset, 0, base_offset]:
                        offset_patterns.append((dx, dy))

            # Apply all offset cuts
            for dx, dy in offset_patterns:
                try:
                    workpiece = (
                        workpiece
                        .faces(">Z")
                        .workplane()
                        .center(dx, dy)
                        .text(
                            text,
                            font_size,  # Use full size for all cuts
                            -cut_depth,
                            font="Arial",
                            halign="center",
                            valign="center",
                            fontPath=None
                        )
                        .center(-dx, -dy)  # Reset center
                    )
                except:
                    # If offset cut fails, continue with other cuts
                    pass

        else:
            # Regular or light text - single cut
            workpiece = (
                workpiece
                .faces(">Z")
                .workplane()
                .text(
                    text,
                    font_size,
                    -cut_depth,
                    font="Arial",
                    halign="center",
                    valign="center",
                    fontPath=None
                )
            )

        return workpiece

    def save_with_heaviness_metadata(self, models, output_name, heaviness):
        """
        Save STL files with heaviness information in filename

        Args:
            models: Dictionary of CadQuery models
            output_name: Base output filename
            heaviness: Heaviness value for metadata
        """

        # Create output directory
        os.makedirs("output", exist_ok=True)

        # Determine weight label
        if heaviness <= 25:
            weight_label = "light"
        elif heaviness <= 50:
            weight_label = "regular"
        elif heaviness <= 75:
            weight_label = "bold"
        else:
            weight_label = "extrabold"

        files_created = []

        try:
            # Export base layer
            if 'base' in models:
                filename = f"output/{output_name}_{weight_label}_bottom_black.stl"
                cq.exporters.export(models['base'], filename)
                print(f"✓ Saved: {filename}")
                files_created.append(filename)

            # Export top layer
            if 'top' in models:
                filename = f"output/{output_name}_{weight_label}_top_yellow.stl"
                cq.exporters.export(models['top'], filename)
                print(f"✓ Saved: {filename}")
                files_created.append(filename)

            # Export combined preview
            if 'combined' in models:
                filename = f"output/{output_name}_{weight_label}_combined_preview.stl"
                cq.exporters.export(models['combined'], filename)
                print(f"✓ Saved: {filename}")
                files_created.append(filename)

        except Exception as e:
            print(f"Error exporting STL files: {e}")

        return files_created


def test_heaviness_variations():
    """Test function to generate signs with different heaviness values"""

    generator = EnhancedSignGenerator()

    test_cases = [
        ("LIGHT", 25),
        ("REGULAR", 50),
        ("BOLD", 75),
        ("HEAVY", 100),
    ]

    for text, heaviness in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {text} with heaviness {heaviness}")
        print('='*60)

        models = generator.generate_sign_with_heaviness(
            text=text,
            sign_width=80,
            sign_height=20,
            heaviness=heaviness,
            bottom_thickness=1.0,
            top_thickness=1.0
        )

        files = generator.save_with_heaviness_metadata(models, text.lower(), heaviness)

        if files:
            print(f"✓ Generated {len(files)} files for {text}")
        else:
            print(f"✗ Failed to generate files for {text}")


if __name__ == "__main__":
    # Run test to demonstrate heaviness variations
    test_heaviness_variations()