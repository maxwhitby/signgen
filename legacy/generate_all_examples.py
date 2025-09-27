#!/usr/bin/env python3
"""
Generate a batch of example signs for 3D printing
Uses the CadQuery-based sign generator for accurate text cutouts
"""

from cadquery_sign_generator import CadQuerySignGenerator


def generate_all_examples():
    """Generate a variety of example signs"""
    
    generator = CadQuerySignGenerator()
    
    examples = [
        # (text, width, height, font_size, output_name)
        ("THREADED INSERTS", 100, 25, 12, "threaded_inserts"),
        ("MOTOR-01", 80, 25, 14, "motor_label"),
        ("HIGH VOLTAGE", 120, 40, 18, "warning_sign"),
        ("3D PRINTER", 90, 30, 15, "printer_label"),
        ("TOOL BOX", 70, 25, 13, "toolbox_label"),
        ("SPARE PARTS", 100, 30, 14, "parts_bin"),
        ("ELECTRONICS", 110, 35, 15, "electronics_label"),
        ("PWR", 30, 15, 10, "power_label"),
    ]
    
    print("="*60)
    print("GENERATING EXAMPLE SIGNS FOR 3D PRINTING")
    print("="*60)
    
    for text, width, height, font_size, output_name in examples:
        print(f"\n{'='*60}")
        print(f"Creating: {output_name}")
        print(f"{'='*60}")
        
        try:
            # Generate the sign
            models = generator.generate_sign(
                text=text,
                sign_width=width,
                sign_height=height,
                font_size=font_size
            )
            
            # Save the STL files
            files = generator.save_stl(models, output_name)
            
            if files:
                print(f"✓ Successfully created {output_name}")
            else:
                print(f"✗ Failed to create {output_name}")
                
        except Exception as e:
            print(f"✗ Error creating {output_name}: {e}")
    
    print("\n" + "="*60)
    print("ALL EXAMPLES GENERATED!")
    print("="*60)
    print("\nFiles are saved in the 'output' directory")
    print("\nFor each sign, you have:")
    print("  • *_bottom_black.stl - Black base layer (1mm thick)")
    print("  • *_top_yellow.stl - Yellow top with text cutouts (1mm thick)")
    print("  • *_combined_preview.stl - Preview of assembled sign")
    print("\nImport both layer files into Bambu Studio and assign colors!")


if __name__ == "__main__":
    generate_all_examples()
