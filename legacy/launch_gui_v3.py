#!/usr/bin/env python3
"""
Launcher for Parametric Sign Generator GUI v3
With font selection, manual font size control, and 2D preview
"""

import sys
import os

def main():
    """Launch the GUI v3 application with font support"""

    print("🏷️ Launching Parametric Sign Generator v3...")
    print("   ✨ NEW: Sans-serif font selection")
    print("   ✨ Manual font size control")
    print("   ✨ Live 2D preview panel")
    print()

    # Check for required dependencies
    try:
        import tkinter
        import cadquery
        print("✓ All dependencies found")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease install required packages:")
        print("  pip install cadquery")
        sys.exit(1)

    # Import and launch the GUI v3
    try:
        from sign_generator_gui_v3 import SignGeneratorGUIv3
        import tkinter as tk

        # Create the main window
        root = tk.Tk()

        # Configure appearance
        try:
            from tkinter import ttk
            style = ttk.Style()
            style.theme_use('clam')  # Modern theme
            style.configure('Accent.TButton', foreground='white', background='#4CAF50')
        except:
            pass

        # Create and run the application
        app = SignGeneratorGUIv3(root)

        print("✓ GUI v3 launched successfully")
        print("\n🎯 FEATURES:")
        print("\n📝 Font Selection:")
        print("• Dropdown with multiple sans-serif typefaces")
        print("• Quick preset buttons: Classic, Modern, Rounded, Bold, Technical")
        print("• Font-specific width calculations for auto-sizing")
        print("• Live preview updates with selected font")

        print("\n🔤 Available Fonts:")
        print("• Arial - Classic, universal")
        print("• Helvetica - Professional, Swiss")
        print("• Impact - Bold, condensed")
        print("• Verdana - Wide, readable")
        print("• Tahoma - Technical, clear")
        print("• Futura - Geometric, modern")
        print("• Gill Sans - Humanist, friendly")
        print("• Trebuchet MS - Rounded, playful")
        print("• And more depending on your system!")

        print("\n📏 Size Controls:")
        print("• Manual font size: 5-50mm range")
        print("• Auto-size toggle for fitting to width")
        print("• Text heaviness: Light to Extra Bold")

        print("\n💡 TIPS:")
        print("• Impact: Great for bold, short text")
        print("• Verdana: Best for maximum readability")
        print("• Helvetica: Professional appearance")
        print("• Futura: Modern, architectural feel")

        print("\nClose this terminal window or press Ctrl+C to exit")

        # Start the GUI event loop
        root.mainloop()

    except Exception as e:
        print(f"✗ Error launching GUI: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all files are in the same directory")
        print("2. Check that sign_generator_gui_v3.py exists")
        print("3. Verify CadQuery is installed: pip install cadquery")
        sys.exit(1)

if __name__ == "__main__":
    main()