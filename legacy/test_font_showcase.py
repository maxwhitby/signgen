#!/usr/bin/env python3
"""
Font Showcase - Demonstrates different sans-serif typefaces
"""

from gui_generator_backend import EnhancedSignGeneratorWithFonts
import os

def showcase_fonts():
    """Generate signs showcasing different fonts"""

    print("="*60)
    print("SANS-SERIF FONT SHOWCASE")
    print("="*60)

    generator = EnhancedSignGeneratorWithFonts()

    # Font samples with descriptions
    font_samples = [
        ("Arial", "Classic", "Most common, excellent readability"),
        ("Helvetica", "Professional", "Clean, neutral, Swiss design"),
        ("Impact", "Bold Statement", "Heavy, condensed, attention-grabbing"),
        ("Verdana", "Screen-Optimized", "Wide, open, great legibility"),
        ("Tahoma", "Technical", "Clear, modern, Windows standard"),
        ("Futura", "Geometric", "Bauhaus-inspired, geometric shapes"),
        ("Gill Sans", "Humanist", "British classic, friendly feel"),
        ("Trebuchet MS", "Playful", "Rounded, slightly informal"),
    ]

    print("\nGenerating sample signs with different fonts...")
    print("Text: 'STYLE' | Size: 80x25mm | Font size: 16mm")
    print("-" * 60)

    results = []

    for font, style, description in font_samples:
        print(f"\n{font:15s} ({style})")
        print(f"  {description}")

        try:
            models = generator.generate_sign_with_font(
                text="STYLE",
                font_family=font,
                sign_width=80,
                sign_height=25,
                font_size=16,
                heaviness=50,
                bottom_thickness=1.0,
                top_thickness=1.0,
                auto_size=False
            )

            output_name = f"showcase_{font.lower().replace(' ', '_')}"
            files = generator.save_with_metadata(models, output_name, 50, font)

            if files:
                results.append((font, style, "✓"))
                print(f"  ✓ Generated successfully")
            else:
                results.append((font, style, "✗"))
                print(f"  ✗ Failed to generate")

        except Exception as e:
            results.append((font, style, "✗"))
            print(f"  ✗ Error: {str(e)[:40]}")

    # Summary
    print("\n" + "="*60)
    print("FONT CHARACTERISTICS")
    print("="*60)

    print("\nCondensed (Narrow):")
    print("• Impact - Very condensed, allows more text")
    print("• Arial - Moderately condensed")

    print("\nWide/Open:")
    print("• Verdana - Extra wide for clarity")
    print("• Gill Sans - Comfortable spacing")

    print("\nGeometric:")
    print("• Futura - Perfect circles and triangles")
    print("• Trebuchet MS - Rounded geometry")

    print("\nNeutral/Professional:")
    print("• Helvetica - Swiss neutrality")
    print("• Arial - Universal standard")
    print("• Tahoma - Clean technical look")

    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)

    success_count = sum(1 for _, _, status in results if status == "✓")
    print(f"\nSuccessfully generated: {success_count}/{len(results)} fonts")

    print("\nFont Status:")
    for font, style, status in results:
        print(f"  {status} {font:15s} - {style}")

    print("\n💡 USAGE TIPS:")
    print("• Impact: Best for short, bold text")
    print("• Verdana: Great for maximum readability")
    print("• Helvetica: Professional, clean appearance")
    print("• Futura: Modern, architectural feel")
    print("• Gill Sans: Friendly, approachable")

def main():
    """Run the font showcase"""

    print("\n🔤 FONT SHOWCASE TEST\n")

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Run showcase
    showcase_fonts()

    print("\n✅ Showcase complete!")
    print("📂 Check the 'output' folder to compare different fonts")
    print("\n🖥️ To use the GUI with font selection:")
    print("   python sign_generator_gui_v3.py")
    print("\nThe GUI includes:")
    print("• Font dropdown menu")
    print("• Quick preset buttons (Classic, Modern, Rounded, Bold, Technical)")
    print("• Live preview showing selected font")

if __name__ == "__main__":
    main()