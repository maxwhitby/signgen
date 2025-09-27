#!/usr/bin/env python3
"""
Launcher for the enhanced Parametric Sign Generator GUI v2
With font size control and 2D preview
"""

import sys
import os

def main():
    """Launch the enhanced GUI application"""

    print("🏷️ Launching Parametric Sign Generator v2...")
    print("   ✨ NEW: Manual font size control")
    print("   ✨ NEW: Live 2D preview panel")
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

    # Import and launch the GUI v2
    try:
        from sign_generator_gui_v2 import SignGeneratorGUIv2
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
        app = SignGeneratorGUIv2(root)

        print("✓ GUI v2 launched successfully")
        print("\n🎯 NEW FEATURES:")
        print("• Font Size Control - Manual control over text size (5-50mm)")
        print("• Auto-Size Toggle - Choose between manual and automatic sizing")
        print("• 2D Live Preview - See your sign design in real-time")
        print("• Text Heaviness - Adjust from light to extra bold")
        print("• Better Margins - Manual font size can use more of the sign area")
        print("\n📌 TIP: Increase font size to make text larger and use more space")
        print("📌 TIP: Disable auto-size for full control over text size")
        print("\nClose this terminal window or press Ctrl+C to exit")

        # Start the GUI event loop
        root.mainloop()

    except Exception as e:
        print(f"✗ Error launching GUI: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all files are in the same directory")
        print("2. Check that sign_generator_gui_v2.py exists")
        print("3. Verify CadQuery is installed: pip install cadquery")
        sys.exit(1)

if __name__ == "__main__":
    main()