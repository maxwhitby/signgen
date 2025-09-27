#!/usr/bin/env python3
"""
Test script to verify Bold and Extra Bold improvements
Shows the visual difference between all weight settings
"""

from gui_generator_backend import EnhancedSignGenerator
import os

def test_all_weights():
    """Generate signs showing all weight differences"""

    print("="*60)
    print("BOLD & EXTRA BOLD IMPROVEMENTS TEST")
    print("="*60)

    generator = EnhancedSignGenerator()

    # Test with consistent text and size to see weight differences
    test_text = "BOLD"
    test_cases = [
        (10, "Light", "Thinnest strokes"),
        (25, "Light+", "Light with slight weight"),
        (50, "Regular", "Standard weight"),
        (75, "Bold", "Noticeably thicker strokes"),
        (90, "Bold+", "Very bold"),
        (100, "Extra Bold", "Maximum thickness")
    ]

    print(f"\nGenerating '{test_text}' with different weights...")
    print("Sign dimensions: 80mm x 25mm")
    print("Font size: Fixed at 16mm for comparison")
    print("-" * 60)

    results = []

    for heaviness, label, description in test_cases:
        print(f"\n{heaviness:3d}%: {label:12s} - {description}")

        try:
            models = generator.generate_sign_with_heaviness(
                text=test_text,
                sign_width=80,
                sign_height=25,
                font_size=16,  # Fixed size to see weight difference
                heaviness=heaviness,
                bottom_thickness=1.0,
                top_thickness=1.0,
                auto_size=False
            )

            output_name = f"weight_{heaviness:03d}_{label.lower().replace(' ', '_').replace('+', 'plus')}"
            files = generator.save_with_heaviness_metadata(models, output_name, heaviness)

            if files:
                # Check file size as indicator of complexity
                top_file = [f for f in files if 'top' in f][0]
                size_kb = os.path.getsize(top_file) / 1024
                results.append((heaviness, label, size_kb))
                print(f"  ✓ Generated successfully")
                print(f"  📊 Complexity: {size_kb:.1f} KB")
            else:
                print(f"  ✗ Failed to generate")

        except Exception as e:
            print(f"  ✗ Error: {str(e)[:50]}")

    # Analysis
    print("\n" + "="*60)
    print("WEIGHT COMPARISON RESULTS")
    print("="*60)

    if results:
        print("\nFile complexity by weight (larger = more complex cuts):")
        for heaviness, label, size in results:
            bar = "█" * int(size / 5)  # Visual bar chart
            print(f"{heaviness:3d}% {label:12s}: {bar} {size:.1f} KB")

    print("\n" + "="*60)
    print("IMPROVEMENTS IMPLEMENTED")
    print("="*60)
    print("✓ Bold (75%): Increased size multiplier to 1.12 (was 1.08)")
    print("✓ Bold (75%): Increased stroke offset to 0.3 (was 0.1)")
    print("✓ Bold (75%): Now uses 5-way offset pattern for thicker strokes")
    print()
    print("✓ Extra Bold (100%): Increased size multiplier to 1.25 (was 1.15)")
    print("✓ Extra Bold (100%): Increased stroke offset to 0.5 (was 0.2)")
    print("✓ Extra Bold (100%): Now uses 9-way grid pattern for maximum thickness")
    print()
    print("✓ Preview: Bold text rendered with multiple overlays")
    print("✓ Preview: Extra Bold uses 3x3 grid of overlays for visual thickness")

    print("\n💡 TIP: The differences are most visible when comparing:")
    print("   - Regular (50%) vs Bold (75%)")
    print("   - Bold (75%) vs Extra Bold (100%)")

def main():
    """Run the bold improvements test"""

    print("\n🔤 BOLD TEXT IMPROVEMENTS TEST\n")

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Run tests
    test_all_weights()

    print("\n✅ Test completed!")
    print("📂 Check the 'output' folder to compare the STL files")
    print("\n🖥️ To see the improved preview in action:")
    print("   python sign_generator_gui_v2.py")
    print("   - Try moving the heaviness slider from 50% to 75% to 100%")
    print("   - The preview should show visible differences")

if __name__ == "__main__":
    main()