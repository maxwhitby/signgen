#!/usr/bin/env python3
"""
Professional Sign Generator using CadQuery
Creates proper two-layer signs with accurate text cutouts for 3D printing
Optimized for Bambu Lab P1S bi-color printing
"""

import cadquery as cq
import argparse
import os


class CadQuerySignGenerator:
    def __init__(self):
        self.text = "LABEL"
        self.sign_width = 100  # mm
        self.sign_height = 25  # mm
        self.font_size = 12  # mm
        self.base_thickness = 1.0  # mm (black layer)
        self.top_thickness = 1.0  # mm (yellow layer)
        self.corner_radius = 2.0  # mm
        self.font_name = "Arial"  # Font to use
        
    def generate_sign(self, text=None, sign_width=None, sign_height=None, font_size=None, auto_size=True):
        """Generate the sign with proper text cutouts"""
        
        # Update parameters if provided
        if text:
            self.text = text
        if sign_width:
            self.sign_width = sign_width
        if sign_height:
            self.sign_height = sign_height
        if font_size:
            self.font_size = font_size
        
        # Auto-adjust font size if text is too wide
        if auto_size and font_size is None:
            # Estimate text width (roughly 0.55 * font_size per character for Arial)
            estimated_width = len(self.text) * self.font_size * 0.55
            max_text_width = self.sign_width * 0.80  # Leave 20% margin (10% each side)
            
            if estimated_width > max_text_width:
                # Reduce font size to fit
                self.font_size = max_text_width / (len(self.text) * 0.55)
                print(f"Auto-adjusted font size to {self.font_size:.1f}mm to fit width")
        
        print(f"Generating sign: '{self.text}'")
        print(f"Sign dimensions: {self.sign_width}mm x {self.sign_height}mm")
        
        # Auto-adjust font size based on text length and sign width
        if auto_size:
            # More accurate character width estimation for Arial
            # Capital letters are about 0.7 * font_size, lowercase about 0.5
            char_widths = {
                'I': 0.3, 'i': 0.25, 'l': 0.25, '1': 0.5,
                'W': 0.9, 'M': 0.85, 'w': 0.75, 'm': 0.75,
                ' ': 0.3, '-': 0.4, '.': 0.3,
            }
            
            # Calculate estimated width
            estimated_width = 0
            for char in self.text:
                width_factor = char_widths.get(char, 0.6 if char.isupper() else 0.5)
                estimated_width += self.font_size * width_factor
            
            max_text_width = self.sign_width * 0.75  # Leave 25% total margin
            
            if estimated_width > max_text_width:
                # Calculate scaling factor
                scale = max_text_width / estimated_width
                self.font_size = self.font_size * scale
                print(f"Auto-adjusted font size to {self.font_size:.1f}mm to fit width")
        
        print(f"Font size: {self.font_size:.1f}mm")
        print(f"Layer thicknesses: Base={self.base_thickness}mm, Top={self.top_thickness}mm")
        
        # Create the base layer (black) - simple rounded rectangle
        base_layer = (
            cq.Workplane("XY")
            .rect(self.sign_width, self.sign_height)
            .extrude(self.base_thickness)
        )
        
        # Add rounded corners if specified
        if self.corner_radius > 0:
            base_layer = base_layer.edges("|Z").fillet(self.corner_radius)
        
        # Create the top layer (yellow) with text cutout
        top_layer = (
            cq.Workplane("XY")
            .workplane(offset=self.base_thickness)  # Start at top of base layer
            .rect(self.sign_width, self.sign_height)
            .extrude(self.top_thickness)
        )
        
        # Add rounded corners to top layer
        if self.corner_radius > 0:
            top_layer = top_layer.edges("|Z").fillet(self.corner_radius)
        
        # Cut out the text from the top layer
        # Position text in center of the top surface
        top_layer = (
            top_layer
            .faces(">Z")
            .workplane()
            .text(
                self.text,
                self.font_size,
                -self.top_thickness * 1.1,  # Cut all the way through
                font="Arial",
                halign="center",
                valign="center",
                fontPath=None  # Will use system fonts
            )
        )
        
        # Create combined model for preview
        combined = base_layer.union(top_layer)
        
        return {
            'base': base_layer,
            'top': top_layer,
            'combined': combined
        }
    
    def save_stl(self, models, output_name="sign"):
        """Export the models as STL files"""
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        files_created = []
        
        try:
            # Export base layer (black)
            if 'base' in models:
                filename = f"output/{output_name}_bottom_black.stl"
                cq.exporters.export(models['base'], filename)
                print(f"✓ Saved: {filename}")
                files_created.append(filename)
            
            # Export top layer (yellow)
            if 'top' in models:
                filename = f"output/{output_name}_top_yellow.stl"
                cq.exporters.export(models['top'], filename)
                print(f"✓ Saved: {filename}")
                files_created.append(filename)
            
            # Export combined preview
            if 'combined' in models:
                filename = f"output/{output_name}_combined_preview.stl"
                cq.exporters.export(models['combined'], filename)
                print(f"✓ Saved: {filename}")
                files_created.append(filename)
                
        except Exception as e:
            print(f"Error exporting STL files: {e}")
        
        return files_created


def main():
    parser = argparse.ArgumentParser(
        description='Professional sign generator for bi-color 3D printing'
    )
    parser.add_argument('text', help='Text to display on the sign')
    parser.add_argument('--width', type=float, default=100, 
                       help='Sign width in mm (default: 100)')
    parser.add_argument('--height', type=float, default=25,
                       help='Sign height in mm (default: 25)')
    parser.add_argument('--font-size', type=float, default=12,
                       help='Font size in mm (default: 12)')
    parser.add_argument('--base-thickness', type=float, default=1.0,
                       help='Base layer thickness in mm (default: 1.0)')
    parser.add_argument('--top-thickness', type=float, default=1.0,
                       help='Top layer thickness in mm (default: 1.0)')
    parser.add_argument('--corner-radius', type=float, default=2.0,
                       help='Corner radius in mm (default: 2.0)')
    parser.add_argument('--output', default='sign',
                       help='Base filename for output files')
    
    args = parser.parse_args()
    
    # Create generator
    generator = CadQuerySignGenerator()
    
    # Set parameters
    generator.base_thickness = args.base_thickness
    generator.top_thickness = args.top_thickness
    generator.corner_radius = args.corner_radius
    
    # Generate the sign
    models = generator.generate_sign(
        text=args.text,
        sign_width=args.width,
        sign_height=args.height,
        font_size=args.font_size
    )
    
    # Save STL files
    files = generator.save_stl(models, args.output)
    
    if files:
        print("\n" + "="*60)
        print("SUCCESS! Sign files generated")
        print("="*60)
        print("\nBambu Lab P1S Printing Instructions:")
        print("-------------------------------------")
        print("1. Open Bambu Studio")
        print("2. Import the two layer files:")
        print(f"   - {args.output}_bottom_black.stl → Black filament")
        print(f"   - {args.output}_top_yellow.stl → Yellow filament")
        print("3. Ensure both objects are aligned (use 'Assemble' if needed)")
        print("4. Slice with these recommended settings:")
        print("   • Layer height: 0.2mm")
        print("   • Initial layer: 0.2mm")
        print("   • Infill: 20% (Grid or Gyroid)")
        print("   • Print speed: Standard")
        print("   • No supports needed")
        print("5. Start print!")
        print("\nThe text will appear as black (bottom layer)")
        print("showing through yellow (top layer with cutouts)")
    else:
        print("\nError: No files were generated")


if __name__ == "__main__":
    main()
