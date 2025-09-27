#!/usr/bin/env python3
"""
Simple launcher for the Parametric Sign Generator GUI
"""

import sys
import os

def main():
    """Launch the GUI application"""

    print("🏷️ Launching Parametric Sign Generator GUI...")

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

    # Import and launch the GUI
    try:
        from sign_generator_gui import SignGeneratorGUI
        import tkinter as tk

        # Create the main window
        root = tk.Tk()

        # Configure appearance
        try:
            from tkinter import ttk
            style = ttk.Style()
            style.theme_use('clam')  # Modern theme
        except:
            pass

        # Create and run the application
        app = SignGeneratorGUI(root)

        print("✓ GUI launched successfully")
        print("\nFeatures:")
        print("• Adjustable text heaviness (light to extra bold)")
        print("• Custom dimensions and layer thickness")
        print("• Auto-sizing for text to fit width")
        print("• Generates STL files for Bambu Lab bi-color printing")
        print("\nClose this terminal window or press Ctrl+C to exit")

        # Start the GUI event loop
        root.mainloop()

    except Exception as e:
        print(f"✗ Error launching GUI: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all files are in the same directory")
        print("2. Check that sign_generator_gui.py exists")
        print("3. Verify CadQuery is installed: pip install cadquery")
        sys.exit(1)

if __name__ == "__main__":
    main()