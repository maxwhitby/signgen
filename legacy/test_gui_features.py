#!/usr/bin/env python3
"""
Test script to demonstrate GUI features and text heaviness control
Run this to generate sample signs with different text weights
"""

from gui_generator_backend import EnhancedSignGenerator
import os

def test_heaviness_variations():
    """Generate sample signs with different heaviness values"""

    print("="*60)
    print("TESTING TEXT HEAVINESS FEATURE")
    print("="*60)

    generator = EnhancedSignGenerator()

    # Test cases showing the progression from light to extra bold
    test_cases = [
        ("LIGHT", 10, "Minimal stroke weight - very thin text"),
        ("REGULAR", 50, "Standard text weight - default appearance"),
        ("BOLD", 75, "Bold text - thicker strokes"),
        ("EXTRA", 100, "Extra bold - maximum thickness"),
    ]

    print("\nGenerating sample signs with varying text heaviness...")
    print("-" * 60)

    successful = []
    failed = []

    for text, heaviness, description in test_cases:
        print(f"\n{heaviness:3d}% Heaviness: {description}")
        print(f"Text: '{text}'")

        try:
            # Generate sign
            models = generator.generate_sign_with_heaviness(
                text=text,
                sign_width=80,
                sign_height=25,
                heaviness=heaviness,
                bottom_thickness=1.0,
                top_thickness=1.0
            )

            # Save with descriptive name
            output_name = f"demo_{heaviness:03d}_{text.lower()}"
            files = generator.save_with_heaviness_metadata(models, output_name, heaviness)

            if files:
                successful.append((text, heaviness))
                print(f"✓ Success: Created {len(files)} files")
                for f in files:
                    file_size = os.path.getsize(f) / 1024  # Size in KB
                    print(f"  - {os.path.basename(f)} ({file_size:.1f} KB)")
            else:
                failed.append((text, heaviness))
                print(f"✗ Failed: No files created")

        except Exception as e:
            failed.append((text, heaviness))
            print(f"✗ Error: {str(e)}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Successful: {len(successful)} signs")
    print(f"Failed: {len(failed)} signs")

    if successful:
        print("\nSuccessfully generated signs:")
        for text, heaviness in successful:
            weight_label = "light" if heaviness <= 25 else "regular" if heaviness <= 50 else "bold" if heaviness <= 75 else "extrabold"
            print(f"  • {text:8s} (heaviness: {heaviness:3d}%, style: {weight_label})")

    print("\n" + "="*60)
    print("FILE SIZE ANALYSIS")
    print("="*60)
    print("Notice how file sizes vary with text heaviness:")
    print("- Lighter text = smaller top layer file (less material removed)")
    print("- Bolder text = larger top layer file (more complex cuts)")
    print("\nCheck the 'output' folder to see the generated STL files.")

    return len(successful), len(failed)

def main():
    """Run the test"""
    print("\n🏷️ PARAMETRIC SIGN GENERATOR - TEXT HEAVINESS TEST\n")

    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Run tests
    success_count, fail_count = test_heaviness_variations()

    if success_count > 0:
        print("\n✅ Test completed successfully!")
        print(f"   Generated {success_count} different sign variations")
        print("\n📂 Next steps:")
        print("   1. Open the 'output' folder to see STL files")
        print("   2. Import into Bambu Studio for 3D printing")
        print("   3. Compare the visual differences in text weight")
        print("\n🖥️ To use the GUI, run: python sign_generator_gui.py")
    else:
        print("\n❌ Test failed - no signs were generated")
        print("   Check error messages above for details")

if __name__ == "__main__":
    main()