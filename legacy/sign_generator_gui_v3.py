#!/usr/bin/env python3
"""
Parametric Sign Generator GUI v3
Enhanced with font selection, manual font size control, and 2D preview
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Canvas
import os
import sys
import threading
from pathlib import Path
import platform

# Import the enhanced backend generator with heaviness support
try:
    from gui_generator_backend import EnhancedSignGeneratorWithFonts
except ImportError:
    try:
        from gui_generator_backend import EnhancedSignGenerator as EnhancedSignGeneratorWithFonts
    except ImportError:
        from cadquery_sign_generator import CadQuerySignGenerator as EnhancedSignGeneratorWithFonts


class SignGeneratorGUIv3:
    def __init__(self, root):
        self.root = root
        self.root.title("🏷️ Parametric Sign Generator v3")
        self.root.geometry("1100x820")  # Wider window
        self.root.resizable(True, True)  # Allow resizing
        self.root.minsize(1000, 750)  # Set minimum size

        # Initialize enhanced backend
        self.generator = EnhancedSignGeneratorWithFonts()

        # Available fonts (cross-platform safe selection)
        self.available_fonts = self.get_available_fonts()

        # Variables for inputs
        self.text_var = tk.StringVar(value="LABEL")
        self.font_family_var = tk.StringVar(value="Arial")
        self.width_var = tk.DoubleVar(value=100.0)
        self.height_var = tk.DoubleVar(value=25.0)
        self.font_size_var = tk.DoubleVar(value=16.0)
        self.auto_size_var = tk.BooleanVar(value=False)
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

    def get_available_fonts(self):
        """Get list of available sans-serif fonts based on platform"""
        # Core fonts that should work on most systems
        core_fonts = [
            "Arial",
            "Helvetica",
            "Verdana",
            "Tahoma",
            "Impact",
            "Trebuchet MS"
        ]

        # Additional fonts by platform
        if platform.system() == 'Darwin':  # macOS
            extra_fonts = [
                "Helvetica Neue",
                "Avenir",
                "Futura",
                "Gill Sans",
                "SF Pro Display",
                "SF Pro Text"
            ]
        elif platform.system() == 'Windows':
            extra_fonts = [
                "Calibri",
                "Segoe UI",
                "Century Gothic",
                "Franklin Gothic",
                "MS Sans Serif"
            ]
        else:  # Linux
            extra_fonts = [
                "DejaVu Sans",
                "Liberation Sans",
                "Ubuntu",
                "Cantarell"
            ]

        # Combine and add some popular web fonts if available
        all_fonts = core_fonts + extra_fonts + [
            "Roboto",
            "Open Sans",
            "Montserrat",
            "Raleway",
            "Lato"
        ]

        # Remove duplicates and sort
        return sorted(list(set(all_fonts)))

    def setup_variable_traces(self):
        """Set up variable traces for live preview updates"""
        self.width_var.trace_add('write', lambda *args: self.update_preview())
        self.height_var.trace_add('write', lambda *args: self.update_preview())
        self.font_size_var.trace_add('write', lambda *args: self.update_preview())
        self.heaviness_var.trace_add('write', lambda *args: self.update_preview())
        self.auto_size_var.trace_add('write', lambda *args: self.update_preview())
        self.font_family_var.trace_add('write', lambda *args: self.update_preview())

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

        # NEW: Font Selection section
        ttk.Label(left_frame, text="Font Selection:",
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        font_frame = ttk.Frame(left_frame)
        font_frame.grid(row=row, column=0, columnspan=3, pady=5)

        ttk.Label(font_frame, text="Typeface:").pack(side=tk.LEFT, padx=5)
        self.font_dropdown = ttk.Combobox(font_frame, textvariable=self.font_family_var,
                                          values=self.available_fonts,
                                          width=20, state='readonly')
        self.font_dropdown.pack(side=tk.LEFT, padx=5)

        # Quick font preset buttons
        font_preset_frame = ttk.Frame(left_frame)
        font_preset_frame.grid(row=row+1, column=0, columnspan=3, pady=5)

        font_presets = [
            ("Classic", "Arial"),
            ("Modern", "Helvetica"),
            ("Rounded", "Verdana"),
            ("Bold", "Impact"),
            ("Technical", "Tahoma")
        ]

        for label, font in font_presets:
            btn = ttk.Button(font_preset_frame, text=label,
                           command=lambda f=font: self.set_font_preset(f),
                           width=10)
            btn.pack(side=tk.LEFT, padx=2)
        row += 2

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

        # Font Size Control section
        ttk.Label(left_frame, text="Font Size Control:",
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        size_frame = ttk.Frame(left_frame)
        size_frame.grid(row=row, column=0, columnspan=3, pady=5)

        ttk.Label(size_frame, text="Size (mm):").pack(side=tk.LEFT, padx=5)
        font_size_spin = ttk.Spinbox(size_frame, from_=5, to=50, textvariable=self.font_size_var,
                                     width=10, increment=1, format="%.1f")
        font_size_spin.pack(side=tk.LEFT, padx=5)

        auto_check = ttk.Checkbutton(size_frame, text="Auto-size to fit",
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

        # Create preview canvas (larger for better visibility)
        self.preview_canvas = Canvas(canvas_frame, width=450, height=400,
                                    bg='white', relief='sunken', borderwidth=2)
        self.preview_canvas.grid(row=0, column=0)

        # Preview info
        self.preview_info = ttk.Label(right_frame, text="", font=('Arial', 9))
        self.preview_info.grid(row=2, column=0, pady=5)

    def set_font_preset(self, font_name):
        """Set font from preset button"""
        if font_name in self.available_fonts:
            self.font_family_var.set(font_name)
            self.update_preview()
            self.status_var.set(f"Font changed to {font_name}")

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
        font_family = self.font_family_var.get()
        width = self.width_var.get()
        height = self.height_var.get()
        font_size = self.font_size_var.get()
        heaviness = self.heaviness_var.get()
        auto_size = self.auto_size_var.get()

        # Calculate display dimensions (matching the larger canvas)
        canvas_width = 450
        canvas_height = 400

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
            estimated_font_size = self.calculate_auto_font_size(text, width, heaviness)
        else:
            estimated_font_size = font_size

        # Scale font for display
        display_font_size = int(estimated_font_size * scale)
        display_font_size = max(8, min(display_font_size, 72))

        # Determine font weight and visual effects based on heaviness
        if heaviness <= 15:
            # Very light - smaller font and gray color
            font_weight = 'normal'
            stroke_width = 0
            text_color = '#404040'  # Dark gray for light effect
            size_adjustment = 0.9  # Make slightly smaller
        elif heaviness <= 25:
            # Light - normal size but lighter color
            font_weight = 'normal'
            stroke_width = 0
            text_color = '#202020'  # Very dark gray
            size_adjustment = 0.95
        elif heaviness <= 50:
            # Regular
            font_weight = 'normal'
            stroke_width = 1
            text_color = 'black'
            size_adjustment = 1.0
        elif heaviness <= 75:
            # Bold
            font_weight = 'bold'
            stroke_width = 2
            text_color = 'black'
            size_adjustment = 1.05
        else:
            # Extra bold
            font_weight = 'bold'
            stroke_width = 3
            text_color = 'black'
            size_adjustment = 1.1

        # Apply size adjustment for weight visualization
        adjusted_display_size = int(display_font_size * size_adjustment)
        adjusted_display_size = max(8, min(adjusted_display_size, 72))

        # Draw text with selected font
        try:
            # Try selected font first
            font = (font_family, adjusted_display_size, font_weight)
            text_x = x_offset + display_width / 2
            text_y = y_offset + display_height / 2

            if stroke_width > 1:
                # Draw text multiple times for bold/extra bold effect
                if stroke_width == 2:
                    offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
                else:  # stroke_width == 3
                    offsets = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2)]

                for dx, dy in offsets:
                    self.preview_canvas.create_text(
                        text_x + dx,
                        text_y + dy,
                        text=text,
                        font=font,
                        fill=text_color,
                        anchor='center'
                    )
            else:
                # Single render for light/regular weights
                self.preview_canvas.create_text(
                    text_x,
                    text_y,
                    text=text,
                    font=font,
                    fill=text_color,
                    anchor='center'
                )
        except:
            # Fallback to Arial if font fails
            font = ('Arial', display_font_size, 'normal')
            self.preview_canvas.create_text(
                x_offset + display_width / 2,
                y_offset + display_height / 2,
                text=text,
                font=font,
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
        info_text = f"Font: {font_family} {estimated_font_size:.1f}mm | "
        info_text += f"Heaviness: {heaviness}% | "
        info_text += f"Mode: {'Auto-size' if auto_size else 'Manual'}"
        self.preview_info.config(text=info_text)

    def calculate_auto_font_size(self, text, width, heaviness):
        """Calculate auto font size based on text and width"""
        if not text:
            return 12

        # Base character width estimation (varies by font)
        font = self.font_family_var.get()

        # Font-specific width factors
        font_widths = {
            'Impact': 0.45,
            'Arial': 0.55,
            'Helvetica': 0.55,
            'Verdana': 0.65,
            'Tahoma': 0.60,
            'Trebuchet MS': 0.58,
            'Gill Sans': 0.52,
            'Avenir': 0.58,
            'Futura': 0.60,
        }

        width_factor = font_widths.get(font, 0.55) + (heaviness / 100) * 0.15

        # Start with a base size
        base_size = 12

        # Calculate estimated width
        estimated_width = len(text) * base_size * width_factor

        # Calculate maximum text width
        max_text_width = width * 0.85

        # Scale font size to fit
        if estimated_width > max_text_width:
            scale = max_text_width / estimated_width
            return base_size * scale
        else:
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

        return True

    def generate_sign(self):
        """Generate the STL files"""
        if not self.validate_inputs():
            return

        # Get all parameters
        text = self.text_input.get('1.0', 'end-1c').strip()
        font_family = self.font_family_var.get()
        width = self.width_var.get()
        height = self.height_var.get()
        font_size = self.font_size_var.get()
        auto_size = self.auto_size_var.get()
        heaviness = self.heaviness_var.get()
        bottom_thickness = self.bottom_thickness_var.get()
        top_thickness = self.top_thickness_var.get()

        # Show progress
        self.status_var.set(f"Generating STL files with {font_family} font...")
        self.progress_bar.grid(row=16, column=0, columnspan=3, pady=5)
        self.progress_bar.start(10)

        # Run generation in thread
        def generate_thread():
            try:
                # Use enhanced generator with font support
                if hasattr(self.generator, 'generate_sign_with_font'):
                    models = self.generator.generate_sign_with_font(
                        text=text,
                        font_family=font_family,
                        sign_width=width,
                        sign_height=height,
                        font_size=font_size if not auto_size else None,
                        heaviness=heaviness,
                        bottom_thickness=bottom_thickness,
                        top_thickness=top_thickness,
                        auto_size=auto_size
                    )
                elif hasattr(self.generator, 'generate_sign_with_heaviness'):
                    # Fallback to version without font selection
                    models = self.generator.generate_sign_with_heaviness(
                        text=text,
                        sign_width=width,
                        sign_height=height,
                        font_size=font_size if not auto_size else None,
                        heaviness=heaviness,
                        bottom_thickness=bottom_thickness,
                        top_thickness=top_thickness,
                        auto_size=auto_size
                    )
                else:
                    # Basic generator
                    self.generator.base_thickness = bottom_thickness
                    self.generator.top_thickness = top_thickness
                    models = self.generator.generate_sign(
                        text=text,
                        sign_width=width,
                        sign_height=height,
                        font_size=font_size if not auto_size else None,
                        auto_size=auto_size
                    )

                # Create output name
                safe_text = "".join(c for c in text if c.isalnum() or c in (' ', '-', '_'))[:20]
                safe_font = font_family.replace(' ', '_').lower()[:10]
                output_name = f"{safe_text}_{safe_font}" if safe_text else 'sign'

                # Save files
                if hasattr(self.generator, 'save_with_metadata'):
                    files = self.generator.save_with_metadata(models, output_name, heaviness, font_family)
                elif hasattr(self.generator, 'save_with_heaviness_metadata'):
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

            # Show success dialog
            font = self.font_family_var.get()
            msg = f"Sign files generated successfully!\n"
            msg += f"Font: {font}\n\n"
            msg += "Files created:\n"
            for f in files:
                msg += f"• {os.path.basename(f)}\n"

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

        # Check if it's a font error
        if "font" in error_msg.lower():
            messagebox.showerror("Font Error",
                               f"Failed to generate with selected font.\n{error_msg}\n\n"
                               "Try using Arial or another common font.")
        else:
            messagebox.showerror("Generation Error", f"Failed to generate sign:\n{error_msg}")

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        output_dir = os.path.abspath("output")
        if os.path.exists(output_dir):
            if sys.platform == 'win32':
                os.startfile(output_dir)
            elif sys.platform == 'darwin':
                os.system(f'open "{output_dir}"')
            else:
                os.system(f'xdg-open "{output_dir}"')

    def reset_fields(self):
        """Reset all fields to defaults"""
        self.text_input.delete('1.0', tk.END)
        self.text_input.insert('1.0', "LABEL")
        self.font_family_var.set("Arial")
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
    style.theme_use('clam')

    # Create custom button style
    style.configure('Accent.TButton', foreground='white', background='#4CAF50')

    # Create and run the GUI
    app = SignGeneratorGUIv3(root)
    root.mainloop()


if __name__ == "__main__":
    main()