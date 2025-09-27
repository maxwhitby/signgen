#!/usr/bin/env python3
"""
Test script demonstrating font size control
Shows the difference between auto-size and manual font sizes
"""

from gui_generator_backend import EnhancedSignGenerator
import os

def test_font_size_variations():
    """Generate signs showing font size control"""

    print("="*60)
    print("FONT SIZE CONTROL DEMONSTRATION")
    print("="*60)

    generator = EnhancedSignGenerator()

    test_cases = [
        # (text, font_size, auto_size, description)
        ("AUTO", None, True, "Auto-sized to fit width with margin"),
        ("SMALL", 8, False, "Manual 8mm font - very small"),
        ("MEDIUM", 16, False, "Manual 16mm font - medium size"),
        ("LARGE", 25, False, "Manual 25mm font - large, uses more space"),
        ("HUGE", 35, False, "Manual 35mm font - very large, minimal margin"),
    ]

    print("\nGenerating signs with different font sizes...")
    print("Sign dimensions: 100mm x 25mm")
    print("-" * 60)

    for text, font_size, auto_size, description in test_cases:
        print(f"\n{text}: {description}")

        try:
            if auto_size:
                print(f"  Mode: Auto-size (will fit to width)")
                models = generator.generate_sign_with_heaviness(
                    text=text,
                    sign_width=100,
                    sign_height=25,
                    heaviness=50,
                    auto_size=True
                )
            else:
                print(f"  Mode: Manual font size = {font_size}mm")
                models = generator.generate_sign_with_heaviness(
                    text=text,
                    sign_width=100,
                    sign_height=25,
                    font_size=font_size,
                    heaviness=50,
                    auto_size=False
                )

            # Save files
            output_name = f"font_test_{text.lower()}"
            files = generator.save_with_heaviness_metadata(models, output_name, 50)

            if files:
                print(f"  ✓ Generated successfully")
                # Show file sizes as indicator of complexity
                top_file = [f for f in files if 'top' in f][0]
                size_kb = os.path.getsize(top_file) / 1024
                print(f"  📊 Top layer complexity: {size_kb:.1f} KB")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")

    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    print("\nAuto-Size Benefits:")
    print("• Always fits within the sign width")
    print("• Maintains consistent margins")
    print("• Good for unknown text lengths")

    print("\nManual Size Benefits:")
    print("• Full control over text appearance")
    print("• Can make text larger to fill more space")
    print("• Better for specific design requirements")
    print("• Can reduce margins for maximum impact")

    print("\n💡 TIP: Use manual font size when you want bigger text!")
    print("   The default auto-size leaves 25% margin.")
    print("   Manual sizing can use up to 90% of the width.")

def main():
    """Run the font size demonstration"""

    print("\n🔤 FONT SIZE CONTROL TEST\n")

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Run tests
    test_font_size_variations()

    print("\n✅ Test completed!")
    print("📂 Check the 'output' folder to compare the different font sizes")
    print("\n🖥️ To use the new GUI with font control:")
    print("   python sign_generator_gui_v2.py")
    print("   or")
    print("   python launch_gui_v2.py")

if __name__ == "__main__":
    main()