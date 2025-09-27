#!/usr/bin/env python3
"""
Parametric Sign Generator GUI v2
Enhanced with manual font size control and 2D preview
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Canvas
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


class SignGeneratorGUIv2:
    def __init__(self, root):
        self.root = root
        self.root.title("🏷️ Parametric Sign Generator v2")
        self.root.geometry("900x750")
        self.root.resizable(False, False)

        # Initialize enhanced backend
        self.generator = EnhancedSignGenerator()

        # Variables for inputs
        self.text_var = tk.StringVar(value="LABEL")
        self.width_var = tk.DoubleVar(value=100.0)
        self.height_var = tk.DoubleVar(value=25.0)
        self.font_size_var = tk.DoubleVar(value=16.0)  # NEW: Manual font size
        self.auto_size_var = tk.BooleanVar(value=False)  # NEW: Auto-size toggle
        self.heaviness_var = tk.IntVar(value=50)
        self.heaviness_preset = tk.StringVar(value="Regular")
        self.bottom_thickness_var = tk.DoubleVar(value=1.0)
        self.top_thickness_var = tk.DoubleVar(value=1.0)
        self.status_var = tk.StringVar(value="Ready")
        self.output_path_var = tk.StringVar(value="")

        # Preview canvas dimensions
        self.preview_scale = 3  # pixels per mm

        # Set up variable traces for live preview
        self.setup_variable_traces()

        # Create the GUI
        self.create_widgets()

        # Initial preview
        self.update_preview()

    def setup_variable_traces(self):
        """Set up variable traces for live preview updates"""
        # Update preview when any parameter changes
        self.width_var.trace_add('write', lambda *args: self.update_preview())
        self.height_var.trace_add('write', lambda *args: self.update_preview())
        self.font_size_var.trace_add('write', lambda *args: self.update_preview())
        self.heaviness_var.trace_add('write', lambda *args: self.update_preview())
        self.auto_size_var.trace_add('write', lambda *args: self.update_preview())

    def create_widgets(self):
        """Build the GUI interface with preview panel"""

        # Create main container with two columns
        container = ttk.Frame(self.root, padding="10")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # LEFT COLUMN - Controls
        left_frame = ttk.Frame(container)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        row = 0

        # Title
        title_label = ttk.Label(left_frame, text="Sign Generator Controls",
                                font=('Arial', 14, 'bold'))
        title_label.grid(row=row, column=0, columnspan=3, pady=5)
        row += 1

        # Separator
        ttk.Separator(left_frame, orient='horizontal').grid(row=row, column=0,
                                                            columnspan=3, sticky='ew', pady=5)
        row += 1

        # Text input section
        ttk.Label(left_frame, text="Text to Print:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        self.text_input = tk.Text(left_frame, height=3, width=40, font=('Arial', 10))
        self.text_input.grid(row=row, column=0, columnspan=3, pady=5)
        self.text_input.insert('1.0', "LABEL")
        self.text_input.bind('<KeyRelease>', lambda e: self.update_preview())
        row += 1

        # Label Dimensions section
        ttk.Label(left_frame, text="Label Dimensions (mm):",
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        dims_frame = ttk.Frame(left_frame)
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

        # NEW: Font Size Control section
        ttk.Label(left_frame, text="Font Size Control:",
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        font_frame = ttk.Frame(left_frame)
        font_frame.grid(row=row, column=0, columnspan=3, pady=5)

        ttk.Label(font_frame, text="Size (mm):").pack(side=tk.LEFT, padx=5)
        font_size_spin = ttk.Spinbox(font_frame, from_=5, to=50, textvariable=self.font_size_var,
                                     width=10, increment=1, format="%.1f")
        font_size_spin.pack(side=tk.LEFT, padx=5)

        auto_check = ttk.Checkbutton(font_frame, text="Auto-size to fit",
                                     variable=self.auto_size_var,
                                     command=self.toggle_auto_size)
        auto_check.pack(side=tk.LEFT, padx=20)
        row += 1

        # Font size slider for fine control
        font_slider_frame = ttk.Frame(left_frame)
        font_slider_frame.grid(row=row, column=0, columnspan=3, pady=5)

        ttk.Label(font_slider_frame, text="Size:").pack(side=tk.LEFT, padx=5)
        self.font_size_slider = ttk.Scale(font_slider_frame, from_=5, to=50,
                                          variable=self.font_size_var,
                                          orient=tk.HORIZONTAL, length=200)
        self.font_size_slider.pack(side=tk.LEFT, padx=5)

        self.font_size_label = ttk.Label(font_slider_frame, text="16.0mm")
        self.font_size_label.pack(side=tk.LEFT, padx=5)

        # Update font size label when slider moves
        self.font_size_var.trace_add('write', lambda *args: self.update_font_size_label())
        row += 1

        # Text Heaviness section
        ttk.Label(left_frame, text="Text Heaviness:",
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        # Radio buttons for presets
        presets_frame = ttk.Frame(left_frame)
        presets_frame.grid(row=row, column=0, columnspan=3, pady=5)

        presets = [("Light", 25), ("Regular", 50), ("Bold", 75), ("Extra Bold", 100)]
        for text, value in presets:
            rb = ttk.Radiobutton(presets_frame, text=text, variable=self.heaviness_preset,
                                value=text, command=lambda v=value: self.set_heaviness_preset(v))
            rb.pack(side=tk.LEFT, padx=10)
        row += 1

        # Slider for fine control
        slider_frame = ttk.Frame(left_frame)
        slider_frame.grid(row=row, column=0, columnspan=3, pady=5)

        ttk.Label(slider_frame, text="Fine Control:").pack(side=tk.LEFT, padx=5)
        self.heaviness_slider = ttk.Scale(slider_frame, from_=0, to=100,
                                          variable=self.heaviness_var,
                                          orient=tk.HORIZONTAL, length=200,
                                          command=self.update_heaviness_display)
        self.heaviness_slider.pack(side=tk.LEFT, padx=5)

        self.heaviness_label = ttk.Label(slider_frame, text="50")
        self.heaviness_label.pack(side=tk.LEFT, padx=5)
        row += 1

        # Layer Thickness section
        ttk.Label(left_frame, text="Layer Thickness (mm):",
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        thickness_frame = ttk.Frame(left_frame)
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
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)

        generate_btn = ttk.Button(button_frame, text="Generate STL ✓",
                                 command=self.generate_sign,
                                 style='Accent.TButton')
        generate_btn.pack(side=tk.LEFT, padx=5)

        update_preview_btn = ttk.Button(button_frame, text="Update Preview",
                                       command=self.update_preview)
        update_preview_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = ttk.Button(button_frame, text="Reset",
                              command=self.reset_fields)
        reset_btn.pack(side=tk.LEFT, padx=5)
        row += 1

        # Status section
        ttk.Separator(left_frame, orient='horizontal').grid(row=row, column=0,
                                                            columnspan=3, sticky='ew', pady=10)
        row += 1

        status_frame = ttk.Frame(left_frame)
        status_frame.grid(row=row, column=0, columnspan=3, sticky='ew')

        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                     font=('Arial', 10, 'italic'))
        self.status_label.pack(side=tk.LEFT, padx=5)
        row += 1

        output_frame = ttk.Frame(left_frame)
        output_frame.grid(row=row, column=0, columnspan=3, sticky='ew')

        ttk.Label(output_frame, text="Output:").pack(side=tk.LEFT, padx=5)
        self.output_label = ttk.Label(output_frame, textvariable=self.output_path_var,
                                     font=('Arial', 9), foreground='blue')
        self.output_label.pack(side=tk.LEFT, padx=5)

        # Progress bar (hidden initially)
        self.progress_bar = ttk.Progressbar(left_frame, mode='indeterminate')

        # RIGHT COLUMN - Preview
        right_frame = ttk.Frame(container)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Preview title
        preview_title = ttk.Label(right_frame, text="2D Preview",
                                 font=('Arial', 14, 'bold'))
        preview_title.grid(row=0, column=0, pady=5)

        # Preview canvas frame with border
        canvas_frame = ttk.LabelFrame(right_frame, text="Top View", padding="10")
        canvas_frame.grid(row=1, column=0, pady=10)

        # Create preview canvas
        self.preview_canvas = Canvas(canvas_frame, width=350, height=350,
                                    bg='white', relief='sunken', borderwidth=2)
        self.preview_canvas.grid(row=0, column=0)

        # Preview info
        self.preview_info = ttk.Label(right_frame, text="", font=('Arial', 9))
        self.preview_info.grid(row=2, column=0, pady=5)

    def update_font_size_label(self):
        """Update the font size display label"""
        self.font_size_label.config(text=f"{self.font_size_var.get():.1f}mm")

    def toggle_auto_size(self):
        """Toggle between manual and auto font sizing"""
        if self.auto_size_var.get():
            self.font_size_slider.config(state='disabled')
            self.status_var.set("Auto-size enabled - font will fit to width")
        else:
            self.font_size_slider.config(state='normal')
            self.status_var.set("Manual font size enabled")
        self.update_preview()

    def update_preview(self):
        """Update the 2D preview canvas"""
        # Clear canvas
        self.preview_canvas.delete('all')

        # Get current parameters
        text = self.text_input.get('1.0', 'end-1c').strip()
        width = self.width_var.get()
        height = self.height_var.get()
        font_size = self.font_size_var.get()
        heaviness = self.heaviness_var.get()
        auto_size = self.auto_size_var.get()

        # Calculate display dimensions
        canvas_width = 350
        canvas_height = 350

        # Scale to fit canvas while maintaining aspect ratio
        scale_x = (canvas_width - 40) / width
        scale_y = (canvas_height - 40) / height
        scale = min(scale_x, scale_y)

        # Calculate scaled dimensions
        display_width = width * scale
        display_height = height * scale

        # Center the preview
        x_offset = (canvas_width - display_width) / 2
        y_offset = (canvas_height - display_height) / 2

        # Draw sign background (yellow/top layer)
        self.preview_canvas.create_rectangle(
            x_offset, y_offset,
            x_offset + display_width, y_offset + display_height,
            fill='#FFD700', outline='black', width=2
        )

        # Calculate text size for preview
        if auto_size:
            # Estimate auto-sized font
            estimated_font_size = self.calculate_auto_font_size(text, width, heaviness)
        else:
            estimated_font_size = font_size

        # Scale font for display
        display_font_size = int(estimated_font_size * scale)
        display_font_size = max(8, min(display_font_size, 72))  # Clamp to reasonable range

        # Determine font weight and simulate boldness with multiple renders
        if heaviness <= 25:
            font_weight = 'normal'
            stroke_width = 0
        elif heaviness <= 50:
            font_weight = 'normal'
            stroke_width = 1
        elif heaviness <= 75:
            font_weight = 'bold'
            stroke_width = 2
        else:
            font_weight = 'bold'
            stroke_width = 3

        # Draw text (as cutout - shown in black)
        # For bolder text, draw multiple times with slight offsets to simulate thickness
        try:
            font = ('Arial', display_font_size, font_weight)
            text_x = x_offset + display_width / 2
            text_y = y_offset + display_height / 2

            if stroke_width > 0:
                # Draw text multiple times with offsets for bold effect
                offsets = []
                if stroke_width == 1:  # Regular
                    offsets = [(0, 0)]
                elif stroke_width == 2:  # Bold
                    offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
                else:  # Extra Bold
                    offsets = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2)]

                for dx, dy in offsets:
                    self.preview_canvas.create_text(
                        text_x + dx,
                        text_y + dy,
                        text=text,
                        font=font,
                        fill='black',
                        anchor='center'
                    )
            else:
                # Light weight - single render
                self.preview_canvas.create_text(
                    text_x,
                    text_y,
                    text=text,
                    font=font,
                    fill='black',
                    anchor='center'
                )
        except:
            # Fallback if font fails
            self.preview_canvas.create_text(
                x_offset + display_width / 2,
                y_offset + display_height / 2,
                text=text,
                font=('Arial', 12),
                fill='black',
                anchor='center'
            )

        # Draw dimensions
        dim_color = '#666666'
        dim_font = ('Arial', 9)

        # Width dimension
        self.preview_canvas.create_line(
            x_offset, y_offset - 10,
            x_offset + display_width, y_offset - 10,
            fill=dim_color, arrow='both'
        )
        self.preview_canvas.create_text(
            x_offset + display_width / 2, y_offset - 15,
            text=f"{width:.0f}mm",
            font=dim_font, fill=dim_color
        )

        # Height dimension
        self.preview_canvas.create_line(
            x_offset - 10, y_offset,
            x_offset - 10, y_offset + display_height,
            fill=dim_color, arrow='both'
        )
        self.preview_canvas.create_text(
            x_offset - 25, y_offset + display_height / 2,
            text=f"{height:.0f}mm",
            font=dim_font, fill=dim_color, angle=90
        )

        # Update info text
        info_text = f"Font: {estimated_font_size:.1f}mm | "
        info_text += f"Heaviness: {heaviness}% | "
        info_text += f"Mode: {'Auto-size' if auto_size else 'Manual'}"
        self.preview_info.config(text=info_text)

    def calculate_auto_font_size(self, text, width, heaviness):
        """Calculate auto font size based on text and width"""
        if not text:
            return 12

        # Base character width estimation
        char_widths = {
            'I': 0.3, 'i': 0.25, 'l': 0.25, '1': 0.5,
            'W': 0.9, 'M': 0.85, 'w': 0.75, 'm': 0.75,
            ' ': 0.3, '-': 0.4, '.': 0.3,
        }

        # Account for heaviness in width calculation
        width_factor = 0.55 + (heaviness / 100) * 0.15

        # Start with a base size
        base_size = 12

        # Calculate estimated width
        estimated_width = 0
        for char in text:
            char_factor = char_widths.get(char, 0.6 if char.isupper() else 0.5)
            estimated_width += base_size * char_factor * (1 + heaviness / 200)

        # Calculate maximum text width (using less margin for manual control)
        max_text_width = width * 0.85  # Use 85% of width instead of 75%

        # Scale font size to fit
        if estimated_width > max_text_width:
            scale = max_text_width / estimated_width
            return base_size * scale
        else:
            # If text fits, allow it to be larger
            scale = min(2.0, max_text_width / estimated_width)
            return base_size * scale

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

        # Check font size (if manual)
        if not self.auto_size_var.get():
            font_size = self.font_size_var.get()
            if font_size < 5 or font_size > 50:
                errors.append("Font size must be between 5-50mm")

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

    def generate_sign(self):
        """Generate the STL files"""
        if not self.validate_inputs():
            return

        # Get all parameters
        text = self.text_input.get('1.0', 'end-1c').strip()
        width = self.width_var.get()
        height = self.height_var.get()
        font_size = self.font_size_var.get()
        auto_size = self.auto_size_var.get()
        heaviness = self.heaviness_var.get()
        bottom_thickness = self.bottom_thickness_var.get()
        top_thickness = self.top_thickness_var.get()

        # Show progress
        self.status_var.set("Generating STL files...")
        self.progress_bar.grid(row=15, column=0, columnspan=3, pady=5)
        self.progress_bar.start(10)

        # Run generation in thread to avoid blocking GUI
        def generate_thread():
            try:
                # Use enhanced generator with heaviness support
                if hasattr(self.generator, 'generate_sign_with_heaviness'):
                    # Pass manual font size if not auto-sizing
                    if auto_size:
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
                        models = self.generator.generate_sign_with_heaviness(
                            text=text,
                            sign_width=width,
                            sign_height=height,
                            font_size=font_size,  # Use manual font size
                            heaviness=heaviness,
                            bottom_thickness=bottom_thickness,
                            top_thickness=top_thickness,
                            auto_size=False  # Disable auto-sizing
                        )
                else:
                    # Fallback to basic generator
                    self.generator.base_thickness = bottom_thickness
                    self.generator.top_thickness = top_thickness

                    models = self.generator.generate_sign(
                        text=text,
                        sign_width=width,
                        sign_height=height,
                        font_size=font_size if not auto_size else None,
                        auto_size=auto_size
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
            for f in files:
                msg += f"• {os.path.basename(f)}\n"
            msg += "\nBambu Studio Instructions:\n"
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

    def reset_fields(self):
        """Reset all fields to defaults"""
        self.text_input.delete('1.0', tk.END)
        self.text_input.insert('1.0', "LABEL")
        self.width_var.set(100.0)
        self.height_var.set(25.0)
        self.font_size_var.set(16.0)
        self.auto_size_var.set(False)
        self.heaviness_var.set(50)
        self.heaviness_preset.set("Regular")
        self.bottom_thickness_var.set(1.0)
        self.top_thickness_var.set(1.0)
        self.status_var.set("Ready")
        self.output_path_var.set("")
        self.update_heaviness_display(50)
        self.update_preview()


def main():
    """Main entry point"""
    root = tk.Tk()

    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme

    # Create custom button style
    style.configure('Accent.TButton', foreground='white', background='#4CAF50')

    # Create and run the GUI
    app = SignGeneratorGUIv2(root)
    root.mainloop()


if __name__ == "__main__":
    main()