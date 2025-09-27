#!/usr/bin/env python3
"""
Parametric Sign Generator GUI
Desktop application for generating two-color 3D printable signs with text heaviness control
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import threading
from pathlib import Path

# Import the enhanced backend generator with heaviness support
try:
    from gui_generator_backend import EnhancedSignGenerator
except ImportError:
    # Fallback to basic generator if enhanced not available
    from cadquery_sign_generator import CadQuerySignGenerator as EnhancedSignGenerator


class SignGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏷️ Parametric Sign Generator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # Initialize enhanced backend
        self.generator = EnhancedSignGenerator()

        # Variables for inputs
        self.text_var = tk.StringVar(value="LABEL")
        self.width_var = tk.DoubleVar(value=100.0)
        self.height_var = tk.DoubleVar(value=25.0)
        self.heaviness_var = tk.IntVar(value=50)
        self.heaviness_preset = tk.StringVar(value="Regular")
        self.bottom_thickness_var = tk.DoubleVar(value=1.0)
        self.top_thickness_var = tk.DoubleVar(value=1.0)
        self.status_var = tk.StringVar(value="Ready")
        self.output_path_var = tk.StringVar(value="")

        # Create the GUI
        self.create_widgets()

    def create_widgets(self):
        """Build the GUI interface"""

        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        row = 0

        # Title
        title_label = ttk.Label(main_frame, text="Parametric Sign Generator",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=row, column=0, columnspan=3, pady=10)
        row += 1

        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0,
                                                            columnspan=3, sticky='ew', pady=5)
        row += 1

        # Text input section
        ttk.Label(main_frame, text="Text to Print:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        self.text_input = tk.Text(main_frame, height=3, width=50, font=('Arial', 10))
        self.text_input.grid(row=row, column=0, columnspan=3, pady=5)
        self.text_input.insert('1.0', "LABEL")
        row += 1

        # Label Dimensions section
        ttk.Label(main_frame, text="Label Dimensions (mm):",
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        dims_frame = ttk.Frame(main_frame)
        dims_frame.grid(row=row, column=0, columnspan=3)

        ttk.Label(dims_frame, text="Width:").pack(side=tk.LEFT, padx=5)
        width_spin = ttk.Spinbox(dims_frame, from_=10, to=500, textvariable=self.width_var,
                                 width=10, increment=5)
        width_spin.pack(side=tk.LEFT, padx=5)

        ttk.Label(dims_frame, text="Height:").pack(side=tk.LEFT, padx=20)
        height_spin = ttk.Spinbox(dims_frame, from_=5, to=200, textvariable=self.height_var,
                                  width=10, increment=5)
        height_spin.pack(side=tk.LEFT, padx=5)
        row += 1

        # Text Heaviness section
        ttk.Label(main_frame, text="Text Heaviness:",
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        # Radio buttons for presets
        presets_frame = ttk.Frame(main_frame)
        presets_frame.grid(row=row, column=0, columnspan=3, pady=5)

        presets = [("Light", 25), ("Regular", 50), ("Bold", 75), ("Extra Bold", 100)]
        for text, value in presets:
            rb = ttk.Radiobutton(presets_frame, text=text, variable=self.heaviness_preset,
                                value=text, command=lambda v=value: self.set_heaviness_preset(v))
            rb.pack(side=tk.LEFT, padx=10)
        row += 1

        # Slider for fine control
        slider_frame = ttk.Frame(main_frame)
        slider_frame.grid(row=row, column=0, columnspan=3, pady=5)

        ttk.Label(slider_frame, text="Fine Control:").pack(side=tk.LEFT, padx=5)
        self.heaviness_slider = ttk.Scale(slider_frame, from_=0, to=100,
                                          variable=self.heaviness_var,
                                          orient=tk.HORIZONTAL, length=250,
                                          command=self.update_heaviness_display)
        self.heaviness_slider.pack(side=tk.LEFT, padx=5)

        self.heaviness_label = ttk.Label(slider_frame, text="50")
        self.heaviness_label.pack(side=tk.LEFT, padx=5)
        row += 1

        # Layer Thickness section
        ttk.Label(main_frame, text="Layer Thickness (mm):",
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        thickness_frame = ttk.Frame(main_frame)
        thickness_frame.grid(row=row, column=0, columnspan=3)

        ttk.Label(thickness_frame, text="Bottom:").pack(side=tk.LEFT, padx=5)
        bottom_spin = ttk.Spinbox(thickness_frame, from_=0.2, to=5.0,
                                  textvariable=self.bottom_thickness_var,
                                  width=8, increment=0.1, format="%.1f")
        bottom_spin.pack(side=tk.LEFT, padx=5)

        ttk.Label(thickness_frame, text="Top:").pack(side=tk.LEFT, padx=20)
        top_spin = ttk.Spinbox(thickness_frame, from_=0.2, to=5.0,
                              textvariable=self.top_thickness_var,
                              width=8, increment=0.1, format="%.1f")
        top_spin.pack(side=tk.LEFT, padx=5)
        row += 1

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)

        generate_btn = ttk.Button(button_frame, text="Generate STL ✓",
                                 command=self.generate_sign,
                                 style='Accent.TButton')
        generate_btn.pack(side=tk.LEFT, padx=5)

        preview_btn = ttk.Button(button_frame, text="Preview",
                                command=self.preview_sign,
                                state=tk.DISABLED)  # Disabled for Phase 1
        preview_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = ttk.Button(button_frame, text="Reset",
                              command=self.reset_fields)
        reset_btn.pack(side=tk.LEFT, padx=5)
        row += 1

        # Status section
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0,
                                                            columnspan=3, sticky='ew', pady=10)
        row += 1

        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=row, column=0, columnspan=3, sticky='ew')

        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                     font=('Arial', 10, 'italic'))
        self.status_label.pack(side=tk.LEFT, padx=5)
        row += 1

        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=row, column=0, columnspan=3, sticky='ew')

        ttk.Label(output_frame, text="Output:").pack(side=tk.LEFT, padx=5)
        self.output_label = ttk.Label(output_frame, textvariable=self.output_path_var,
                                     font=('Arial', 9), foreground='blue')
        self.output_label.pack(side=tk.LEFT, padx=5)

        # Progress bar (hidden initially)
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')

    def set_heaviness_preset(self, value):
        """Update slider when preset is selected"""
        self.heaviness_var.set(value)
        self.update_heaviness_display(value)

    def update_heaviness_display(self, value=None):
        """Update the heaviness value display"""
        val = int(float(value if value else self.heaviness_var.get()))
        self.heaviness_label.config(text=str(val))

        # Update radio button selection based on slider
        if val <= 37:
            self.heaviness_preset.set("Light")
        elif val <= 62:
            self.heaviness_preset.set("Regular")
        elif val <= 87:
            self.heaviness_preset.set("Bold")
        else:
            self.heaviness_preset.set("Extra Bold")

    def validate_inputs(self):
        """Validate all input fields"""
        errors = []

        # Check text
        text = self.text_input.get('1.0', 'end-1c').strip()
        if not text:
            errors.append("Text cannot be empty")
        elif len(text) > 100:
            errors.append("Text too long (max 100 characters)")

        # Check dimensions
        width = self.width_var.get()
        height = self.height_var.get()

        if width < 10 or width > 500:
            errors.append("Width must be between 10-500mm")
        if height < 5 or height > 200:
            errors.append("Height must be between 5-200mm")

        # Check thicknesses
        bottom = self.bottom_thickness_var.get()
        top = self.top_thickness_var.get()

        if bottom < 0.2 or bottom > 5.0:
            errors.append("Bottom thickness must be between 0.2-5.0mm")
        if top < 0.2 or top > 5.0:
            errors.append("Top thickness must be between 0.2-5.0mm")

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False

        # Warnings
        warnings = []
        if len(text) > 50:
            warnings.append("Long text may be hard to read")
        if (width / height) > 10 or (width / height) < 0.1:
            warnings.append("Unusual aspect ratio")
        if bottom + top > 10:
            warnings.append("Total thickness > 10mm may be excessive")

        if warnings:
            result = messagebox.askokcancel("Warning",
                                           "\n".join(warnings) + "\n\nContinue anyway?")
            return result

        return True

    def heaviness_to_font_params(self, heaviness):
        """Convert heaviness value (0-100) to font parameters"""
        # Map heaviness to font size multiplier and stroke adjustments
        # This affects the boldness of the text in the CadQuery generation

        if heaviness <= 25:
            # Light text - smaller stroke, thinner appearance
            font_style = "Light"
            size_multiplier = 0.95
            stroke_adjustment = -0.1
        elif heaviness <= 50:
            # Regular text
            font_style = "Regular"
            size_multiplier = 1.0
            stroke_adjustment = 0.0
        elif heaviness <= 75:
            # Bold text
            font_style = "Bold"
            size_multiplier = 1.05
            stroke_adjustment = 0.1
        else:
            # Extra bold text
            font_style = "ExtraBold"
            size_multiplier = 1.1
            stroke_adjustment = 0.2

        return {
            'style': font_style,
            'size_multiplier': size_multiplier,
            'stroke_adjustment': stroke_adjustment
        }

    def generate_sign(self):
        """Generate the STL files"""
        if not self.validate_inputs():
            return

        # Get all parameters
        text = self.text_input.get('1.0', 'end-1c').strip()
        width = self.width_var.get()
        height = self.height_var.get()
        heaviness = self.heaviness_var.get()
        bottom_thickness = self.bottom_thickness_var.get()
        top_thickness = self.top_thickness_var.get()

        # Show progress
        self.status_var.set("Generating STL files...")
        self.progress_bar.grid(row=12, column=0, columnspan=3, pady=5)
        self.progress_bar.start(10)

        # Run generation in thread to avoid blocking GUI
        def generate_thread():
            try:
                # Use enhanced generator with heaviness support
                if hasattr(self.generator, 'generate_sign_with_heaviness'):
                    # Use enhanced backend
                    models = self.generator.generate_sign_with_heaviness(
                        text=text,
                        sign_width=width,
                        sign_height=height,
                        heaviness=heaviness,
                        bottom_thickness=bottom_thickness,
                        top_thickness=top_thickness,
                        auto_size=True
                    )
                else:
                    # Fallback to basic generator with font size adjustment
                    font_params = self.heaviness_to_font_params(heaviness)
                    self.generator.base_thickness = bottom_thickness
                    self.generator.top_thickness = top_thickness
                    base_font_size = 12
                    adjusted_font_size = base_font_size * font_params['size_multiplier']

                    models = self.generator.generate_sign(
                        text=text,
                        sign_width=width,
                        sign_height=height,
                        font_size=adjusted_font_size,
                        auto_size=True
                    )

                # Create output name based on text (sanitized)
                safe_text = "".join(c for c in text if c.isalnum() or c in (' ', '-', '_'))[:20]
                output_name = safe_text.replace(' ', '_') or 'sign'

                # Save files with heaviness metadata if supported
                if hasattr(self.generator, 'save_with_heaviness_metadata'):
                    files = self.generator.save_with_heaviness_metadata(models, output_name, heaviness)
                else:
                    files = self.generator.save_stl(models, output_name)

                # Update GUI in main thread
                self.root.after(0, self.generation_complete, files, output_name)

            except Exception as e:
                self.root.after(0, self.generation_error, str(e))

        # Start generation thread
        thread = threading.Thread(target=generate_thread)
        thread.daemon = True
        thread.start()

    def generation_complete(self, files, output_name):
        """Handle successful generation"""
        self.progress_bar.stop()
        self.progress_bar.grid_forget()

        if files:
            self.status_var.set("Files generated successfully!")
            output_dir = os.path.abspath("output")
            self.output_path_var.set(output_dir)

            # Show success dialog with instructions
            msg = f"Sign files generated successfully!\n\n"
            msg += "Files created:\n"
            msg += f"• {output_name}_bottom_black.stl\n"
            msg += f"• {output_name}_top_yellow.stl\n"
            msg += f"• {output_name}_combined_preview.stl\n\n"
            msg += "Bambu Studio Instructions:\n"
            msg += "1. Import both layer files\n"
            msg += "2. Assign materials (black/yellow)\n"
            msg += "3. Ensure alignment\n"
            msg += "4. Slice and print!"

            messagebox.showinfo("Success", msg)

            # Offer to open output folder
            if messagebox.askyesno("Open Folder", "Open output folder?"):
                self.open_output_folder()
        else:
            self.status_var.set("Generation failed")
            messagebox.showerror("Error", "Failed to generate files")

    def generation_error(self, error_msg):
        """Handle generation error"""
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        self.status_var.set("Generation failed")
        messagebox.showerror("Generation Error", f"Failed to generate sign:\n{error_msg}")

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        output_dir = os.path.abspath("output")
        if os.path.exists(output_dir):
            if sys.platform == 'win32':
                os.startfile(output_dir)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{output_dir}"')
            else:  # Linux
                os.system(f'xdg-open "{output_dir}"')

    def preview_sign(self):
        """Preview the sign (Phase 2 feature)"""
        messagebox.showinfo("Preview", "Preview feature coming in Phase 2!")

    def reset_fields(self):
        """Reset all fields to defaults"""
        self.text_input.delete('1.0', tk.END)
        self.text_input.insert('1.0', "LABEL")
        self.width_var.set(100.0)
        self.height_var.set(25.0)
        self.heaviness_var.set(50)
        self.heaviness_preset.set("Regular")
        self.bottom_thickness_var.set(1.0)
        self.top_thickness_var.set(1.0)
        self.status_var.set("Ready")
        self.output_path_var.set("")
        self.update_heaviness_display(50)


def main():
    """Main entry point"""
    root = tk.Tk()

    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme

    # Create custom button style
    style.configure('Accent.TButton', foreground='white', background='#4CAF50')

    # Create and run the GUI
    app = SignGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()