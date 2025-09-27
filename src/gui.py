"""
Consolidated GUI for Sign Generator
Combines all features from v1, v2, and v3 with improvements
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Canvas, simpledialog
import os
import sys
import threading
from pathlib import Path
import platform
from typing import Optional, Dict, Any, List
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sign_generator import SignGenerator
from src.config_manager import ConfigManager
from src.validators import SignValidator
from src.logger import get_logger, set_debug_mode
from src.exceptions import SignGeneratorError, ValidationError, STLExportError


class SignGeneratorGUI:
    """Main GUI application for Sign Generator"""

    def __init__(self, root: tk.Tk, config_path: Optional[str] = None):
        """Initialize the GUI

        Args:
            root: Tkinter root window
            config_path: Optional path to configuration file
        """
        self.root = root
        self.config = ConfigManager(config_path)
        self.logger = get_logger(self.config.get("advanced.debug_mode", False))
        self.validator = SignValidator(self.config)
        self.generator = SignGenerator(
            output_dir=self.config.get("output.directory", "output"),
            debug=self.config.get("advanced.debug_mode", False)
        )

        # Setup window
        self._setup_window()

        # Initialize variables
        self._initialize_variables()

        # Available fonts
        self.available_fonts = self._get_available_fonts()

        # Create GUI
        self._create_widgets()

        # Load last settings if available
        self._load_last_settings()

        # Initial preview
        if self.config.get("advanced.show_preview", True):
            self.update_preview()

    def _setup_window(self):
        """Configure main window"""
        self.root.title("🏷️ Parametric Sign Generator")

        # Window dimensions from config
        width = self.config.get("window.width", 1100)
        height = self.config.get("window.height", 820)
        self.root.geometry(f"{width}x{height}")

        # Resizable settings
        resizable = self.config.get("window.resizable", True)
        self.root.resizable(resizable, resizable)

        if resizable:
            min_width = self.config.get("window.min_width", 1000)
            min_height = self.config.get("window.min_height", 750)
            self.root.minsize(min_width, min_height)

        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _initialize_variables(self):
        """Initialize all GUI variables from config defaults"""
        defaults = self.config.get("defaults", {})

        self.text_var = tk.StringVar(value=defaults.get("text", "LABEL"))
        self.font_var = tk.StringVar(value=defaults.get("font", "Arial"))
        self.font_family_var = self.font_var  # Alias for compatibility
        self.width_var = tk.DoubleVar(value=defaults.get("width", 100.0))
        self.height_var = tk.DoubleVar(value=defaults.get("height", 25.0))
        self.font_size_var = tk.DoubleVar(value=defaults.get("font_size", 16.0))
        self.auto_size_var = tk.BooleanVar(value=defaults.get("auto_size", False))
        self.heaviness_var = tk.IntVar(value=defaults.get("heaviness", 50))
        self.heaviness_preset = tk.StringVar(value="Regular")
        self.bottom_thickness_var = tk.DoubleVar(value=defaults.get("bottom_thickness", 1.0))
        self.top_thickness_var = tk.DoubleVar(value=defaults.get("top_thickness", 1.0))

        # Status and debug variables
        self.status_var = tk.StringVar(value="Ready")
        self.debug_var = tk.BooleanVar(value=self.config.get("advanced.debug_mode", False))
        self.preview_var = tk.BooleanVar(value=self.config.get("advanced.show_preview", True))

        # Generation in progress flag
        self.generating = False

        # Add variable tracing for real-time preview updates
        if self.config.get("advanced.auto_preview_update", True):
            self.width_var.trace_add("write", lambda *args: self.on_parameter_changed())
            self.height_var.trace_add("write", lambda *args: self.on_parameter_changed())
            self.font_family_var.trace_add("write", lambda *args: self.on_parameter_changed())
            self.font_size_var.trace_add("write", lambda *args: self.on_parameter_changed())
            self.auto_size_var.trace_add("write", lambda *args: self.on_parameter_changed())
            self.bottom_thickness_var.trace_add("write", lambda *args: self.on_parameter_changed())
            self.top_thickness_var.trace_add("write", lambda *args: self.on_parameter_changed())

    def _get_available_fonts(self) -> List[str]:
        """Get list of available sans-serif fonts"""
        # Core fonts that should work on most systems
        core_fonts = [
            "Arial", "Helvetica", "Verdana", "Tahoma",
            "Impact", "Trebuchet MS"
        ]

        # Platform-specific fonts
        if platform.system() == 'Darwin':  # macOS
            extra_fonts = [
                "Helvetica Neue", "Avenir", "Futura",
                "Gill Sans", "SF Pro Display"
            ]
        elif platform.system() == 'Windows':
            extra_fonts = [
                "Calibri", "Segoe UI", "Century Gothic",
                "Franklin Gothic"
            ]
        else:  # Linux
            extra_fonts = [
                "DejaVu Sans", "Liberation Sans",
                "Ubuntu", "Cantarell"
            ]

        # Add favorite fonts from config
        favorite_fonts = self.config.get("favorite_fonts", [])

        all_fonts = list(set(core_fonts + extra_fonts + favorite_fonts))
        return sorted(all_fonts)

    def _create_widgets(self):
        """Create all GUI widgets"""
        # Create menu bar
        self._create_menu()

        # Main container
        container = ttk.Frame(self.root, padding="10")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        # Left panel - Controls
        self._create_controls_panel(container)

        # Right panel - Preview (if enabled)
        if self.config.get("advanced.show_preview", True):
            self._create_preview_panel(container)

        # Status bar
        self._create_status_bar()

    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Preset...", command=self.load_preset)
        file_menu.add_command(label="Save Preset...", command=self.save_preset)
        file_menu.add_separator()
        file_menu.add_command(label="Import Settings...", command=self.import_settings)
        file_menu.add_command(label="Export Settings...", command=self.export_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Open Output Folder", command=self.open_output_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Reset to Defaults", command=self.reset_to_defaults)
        edit_menu.add_command(label="Clear Recent Files", command=lambda: self.config.set("recent_files", []))

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(
            label="Debug Mode",
            variable=self.debug_var,
            command=self.on_debug_changed
        )
        view_menu.add_checkbutton(
            label="Auto Preview",
            variable=tk.BooleanVar(value=self.config.get("advanced.auto_preview_update", True)),
            command=lambda: self.config.set("advanced.auto_preview_update", not self.config.get("advanced.auto_preview_update", True))
        )

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_command(label="Troubleshooting", command=self.show_troubleshooting)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)

    def _create_controls_panel(self, parent):
        """Create the controls panel"""
        left_frame = ttk.LabelFrame(parent, text="Sign Parameters", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        # Create notebook for organized controls
        notebook = ttk.Notebook(left_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Basic tab
        basic_frame = ttk.Frame(notebook, padding="10")
        notebook.add(basic_frame, text="Basic")
        self._create_basic_controls(basic_frame)

        # Advanced tab
        advanced_frame = ttk.Frame(notebook, padding="10")
        notebook.add(advanced_frame, text="Advanced")
        self._create_advanced_controls(advanced_frame)

        # Presets tab
        presets_frame = ttk.Frame(notebook, padding="10")
        notebook.add(presets_frame, text="Presets")
        self._create_presets_controls(presets_frame)

        # Buttons
        self._create_action_buttons(left_frame)

    def _create_basic_controls(self, parent):
        """Create basic control inputs"""
        row = 0

        # Text input
        ttk.Label(parent, text="Text to Print:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        self.text_input = tk.Text(parent, height=3, width=40, font=('Arial', 10))
        self.text_input.grid(row=row, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        self.text_input.insert('1.0', self.text_var.get())

        # Bind for live preview
        if self.config.get("advanced.auto_preview_update", True):
            self.text_input.bind('<KeyRelease>', lambda e: self.on_text_changed())
        row += 1

        # Font selection
        ttk.Label(parent, text="Font:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        font_frame = ttk.Frame(parent)
        font_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.font_dropdown = ttk.Combobox(
            font_frame,
            textvariable=self.font_family_var,
            values=self.available_fonts,
            width=20,
            state='readonly'
        )
        self.font_dropdown.pack(side=tk.LEFT, padx=5)

        # Font preset buttons
        for label, font in [("Classic", "Arial"), ("Modern", "Helvetica"), ("Bold", "Impact")]:
            ttk.Button(
                font_frame,
                text=label,
                command=lambda f=font: self.set_font_preset(f),
                width=8
            ).pack(side=tk.LEFT, padx=2)
        row += 1

        # Dimensions
        ttk.Label(parent, text="Dimensions (mm):", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        dims_frame = ttk.Frame(parent)
        dims_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Label(dims_frame, text="Width:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(
            dims_frame,
            from_=self.config.get("validation.width_min", 10),
            to=self.config.get("validation.width_max", 500),
            textvariable=self.width_var,
            width=10,
            increment=5
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(dims_frame, text="Height:").pack(side=tk.LEFT, padx=20)
        ttk.Spinbox(
            dims_frame,
            from_=self.config.get("validation.height_min", 5),
            to=self.config.get("validation.height_max", 200),
            textvariable=self.height_var,
            width=10,
            increment=5
        ).pack(side=tk.LEFT, padx=5)
        row += 1

        # Font size
        ttk.Label(parent, text="Font Size:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        size_frame = ttk.Frame(parent)
        size_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Label(size_frame, text="Size (mm):").pack(side=tk.LEFT, padx=5)
        self.font_size_spinbox = ttk.Spinbox(
            size_frame,
            from_=self.config.get("validation.font_size_min", 5),
            to=self.config.get("validation.font_size_max", 50),
            textvariable=self.font_size_var,
            width=10,
            increment=1,
            format="%.1f",
            command=lambda: self.on_parameter_changed()
        )
        self.font_size_spinbox.pack(side=tk.LEFT, padx=5)
        # Also bind keyboard events for direct typing
        self.font_size_spinbox.bind('<KeyRelease>', lambda e: self.on_parameter_changed())

        self.auto_size_check = ttk.Checkbutton(
            size_frame,
            text="Auto-size to fit",
            variable=self.auto_size_var,
            command=self.on_auto_size_changed
        )
        self.auto_size_check.pack(side=tk.LEFT, padx=20)

        # Suggest optimal button
        ttk.Button(
            size_frame,
            text="Suggest",
            command=self.suggest_optimal_parameters,
            width=8
        ).pack(side=tk.LEFT, padx=5)

    def _create_advanced_controls(self, parent):
        """Create advanced control inputs"""
        row = 0

        # Text heaviness
        ttk.Label(parent, text="Text Heaviness:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        # Radio buttons for presets
        presets_frame = ttk.Frame(parent)
        presets_frame.grid(row=row, column=0, columnspan=2, pady=5)

        for text, value in [("Light", 25), ("Regular", 50), ("Bold", 75), ("Extra Bold", 100)]:
            ttk.Radiobutton(
                presets_frame,
                text=text,
                variable=self.heaviness_preset,
                value=text,
                command=lambda v=value: self.set_heaviness_preset(v)
            ).pack(side=tk.LEFT, padx=10)
        row += 1

        # Slider for fine control
        slider_frame = ttk.Frame(parent)
        slider_frame.grid(row=row, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        ttk.Label(slider_frame, text="Fine Control:").pack(side=tk.LEFT, padx=5)
        self.heaviness_slider = ttk.Scale(
            slider_frame,
            from_=0,
            to=100,
            variable=self.heaviness_var,
            orient=tk.HORIZONTAL,
            length=250,
            command=lambda v: self.on_heaviness_changed()
        )
        self.heaviness_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.heaviness_label = ttk.Label(slider_frame, text="50")
        self.heaviness_label.pack(side=tk.LEFT, padx=5)
        row += 1

        # Layer thickness
        ttk.Label(parent, text="Layer Thickness (mm):", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=10)
        row += 1

        thickness_frame = ttk.Frame(parent)
        thickness_frame.grid(row=row, column=0, columnspan=2)

        ttk.Label(thickness_frame, text="Bottom:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(
            thickness_frame,
            from_=self.config.get("validation.thickness_min", 0.2),
            to=self.config.get("validation.thickness_max", 5.0),
            textvariable=self.bottom_thickness_var,
            width=8,
            increment=0.1,
            format="%.1f"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(thickness_frame, text="Top:").pack(side=tk.LEFT, padx=20)
        ttk.Spinbox(
            thickness_frame,
            from_=self.config.get("validation.thickness_min", 0.2),
            to=self.config.get("validation.thickness_max", 5.0),
            textvariable=self.top_thickness_var,
            width=8,
            increment=0.1,
            format="%.1f"
        ).pack(side=tk.LEFT, padx=5)
        row += 1

        # Validation warning area
        self.validation_text = tk.Text(parent, height=3, width=40, state='disabled',
                                      bg='#f0f0f0', font=('Arial', 9))
        self.validation_text.grid(row=row, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

    def _create_presets_controls(self, parent):
        """Create presets management controls"""
        row = 0

        ttk.Label(parent, text="Saved Presets:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        # Presets listbox
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=row, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.presets_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
        self.presets_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.presets_listbox.yview)

        # Load presets
        self._update_preset_list()
        row += 1

        # Preset buttons
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=10)

        ttk.Button(buttons_frame, text="Load", command=self.load_selected_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Save Current", command=self.save_current_as_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Delete", command=self.delete_selected_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Rename", command=self.rename_selected_preset).pack(side=tk.LEFT, padx=5)

    def _create_action_buttons(self, parent):
        """Create main action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=1, column=0, pady=20)

        # Generate button
        self.generate_btn = ttk.Button(
            button_frame,
            text="Generate STL ✓",
            command=self.generate_sign,
            style='Accent.TButton'
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        # Validate button
        ttk.Button(
            button_frame,
            text="Validate",
            command=self.validate_inputs
        ).pack(side=tk.LEFT, padx=5)

        # Preview button
        ttk.Button(
            button_frame,
            text="Update Preview",
            command=self.update_preview
        ).pack(side=tk.LEFT, padx=5)

        # Reset button
        ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset_to_defaults
        ).pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress_bar = ttk.Progressbar(parent, mode='indeterminate')

    def _create_preview_panel(self, parent):
        """Create the preview panel"""
        right_frame = ttk.LabelFrame(parent, text="Preview", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        # Preview canvas
        self.preview_canvas = Canvas(
            right_frame,
            width=450,
            height=400,
            bg='white',
            relief='sunken',
            borderwidth=2
        )
        self.preview_canvas.pack(pady=10)

        # Preview info
        self.preview_info = ttk.Label(right_frame, text="", font=('Arial', 9))
        self.preview_info.pack(pady=5)

        # Preview controls
        controls_frame = ttk.Frame(right_frame)
        controls_frame.pack()

        ttk.Button(
            controls_frame,
            text="Export Preview",
            command=lambda: messagebox.showinfo("Export", "Export preview image feature coming soon!")
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            controls_frame,
            text="Copy to Clipboard",
            command=lambda: messagebox.showinfo("Copy", "Copy preview feature coming soon!")
        ).pack(side=tk.LEFT, padx=5)

    def _create_status_bar(self):
        """Create status bar at bottom of window"""
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)

        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Arial', 9, 'italic')
        )
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Output folder link
        self.output_link = ttk.Label(
            status_frame,
            text="",
            font=('Arial', 9),
            foreground='blue',
            cursor='hand2'
        )
        self.output_link.pack(side=tk.RIGHT, padx=5)
        self.output_link.bind('<Button-1>', lambda e: self.open_output_folder())

    def _get_available_fonts(self) -> List[str]:
        """Get list of available fonts based on platform"""
        system = platform.system()

        if system == 'Darwin':  # macOS
            fonts = [
                'Arial', 'Arial Black', 'Helvetica', 'Helvetica Neue',
                'Verdana', 'Tahoma', 'Trebuchet MS', 'Impact',
                'Gill Sans', 'Futura', 'Optima', 'Avenir',
                'Avenir Next', 'Geneva', 'Lucida Grande', 'Menlo'
            ]
        elif system == 'Windows':
            fonts = [
                'Arial', 'Arial Black', 'Verdana', 'Tahoma',
                'Trebuchet MS', 'Impact', 'Georgia', 'Calibri',
                'Segoe UI', 'Consolas', 'Comic Sans MS', 'Franklin Gothic'
            ]
        else:  # Linux
            fonts = [
                'Arial', 'Helvetica', 'Sans', 'DejaVu Sans',
                'Liberation Sans', 'FreeSans', 'Ubuntu', 'Cantarell'
            ]

        # Filter to ensure fonts exist
        return [f for f in fonts if f]

    def _load_last_settings(self):
        """Load the last used settings from config"""
        # This is already handled by _initialize_variables using defaults
        pass

    def _on_closing(self):
        """Handle window close event"""
        # Save current settings as defaults
        self._save_current_settings()
        self.root.destroy()

    def _save_current_settings(self):
        """Save current settings to config"""
        self.config.set("defaults.text", self.text_var.get())
        self.config.set("defaults.font", self.font_family_var.get())
        self.config.set("defaults.width", self.width_var.get())
        self.config.set("defaults.height", self.height_var.get())
        self.config.set("defaults.font_size", self.font_size_var.get())
        self.config.set("defaults.auto_size", self.auto_size_var.get())
        self.config.set("defaults.heaviness", self.heaviness_var.get())
        self.config.set("defaults.bottom_thickness", self.bottom_thickness_var.get())
        self.config.set("defaults.top_thickness", self.top_thickness_var.get())

    # Event Handlers
    def on_text_changed(self, *args):
        """Handle text widget changes and sync with StringVar"""
        if hasattr(self, 'text_input'):
            current_text = self.text_input.get('1.0', 'end-1c').strip()
            self.text_var.set(current_text)
        self.on_parameter_changed()

    def on_parameter_changed(self, *args):
        """Handle parameter changes"""
        if self.config.get("advanced.auto_preview_update", True):
            self.update_preview()

    def on_heaviness_changed(self, *args):
        """Handle heaviness slider change"""
        value = self.heaviness_var.get()

        # Update preset label
        if value <= 25:
            preset = "Light"
        elif value <= 50:
            preset = "Regular"
        elif value <= 75:
            preset = "Bold"
        else:
            preset = "Extra Bold"

        self.heaviness_preset.set(preset)
        self.heaviness_label.config(text=f"Text Weight: {preset} ({value})")

        # Update preview
        if self.config.get("advanced.auto_preview_update", True):
            self.update_preview()

    def on_auto_size_changed(self, *args):
        """Handle auto-size checkbox change"""
        if self.auto_size_var.get():
            self.font_size_spinbox.config(state='disabled')
        else:
            self.font_size_spinbox.config(state='normal')

        self.update_preview()

    def on_debug_changed(self, *args):
        """Handle debug mode toggle"""
        debug = self.debug_var.get()
        set_debug_mode(debug)
        self.config.set("advanced.debug_mode", debug)
        self.generator.logger = get_logger(debug)

    def set_heaviness_preset(self, preset: str):
        """Set heaviness from preset button"""
        presets = {
            'Light': 15,
            'Regular': 50,
            'Bold': 75,
            'Extra Bold': 90
        }

        if preset in presets:
            self.heaviness_var.set(presets[preset])

    def set_font_preset(self, font: str):
        """Set font from preset button"""
        if font in self.available_fonts:
            self.font_family_var.set(font)
            self.update_preview()

    def update_preview(self):
        """Update the 2D preview canvas"""
        if not hasattr(self, 'preview_canvas'):
            return

        try:
            # Clear canvas
            self.preview_canvas.delete('all')

            # Get parameters
            # Get text from Text widget if it exists, otherwise from StringVar
            if hasattr(self, 'text_input'):
                text = self.text_input.get('1.0', 'end-1c').strip()
            else:
                text = self.text_var.get()
            width = self.width_var.get()
            height = self.height_var.get()
            font_family = self.font_family_var.get()
            auto_size = self.auto_size_var.get()
            font_size = self.font_size_var.get() if not auto_size else None
            heaviness = self.heaviness_var.get()

            # Canvas dimensions
            canvas_w = 450
            canvas_h = 400

            # Calculate scale
            scale = min((canvas_w - 40) / width, (canvas_h - 40) / height)

            # Calculate rectangle position
            rect_w = width * scale
            rect_h = height * scale
            rect_x = (canvas_w - rect_w) / 2
            rect_y = (canvas_h - rect_h) / 2

            # Draw background rectangle (yellow)
            self.preview_canvas.create_rectangle(
                rect_x, rect_y, rect_x + rect_w, rect_y + rect_h,
                fill='#FFD700', outline='#CCA300', width=2
            )

            # Calculate font size for preview
            if auto_size or font_size is None:
                # Auto-calculate font size
                preview_font_size = self._calculate_preview_font_size(
                    text, rect_w, rect_h, font_family, heaviness
                )
            else:
                preview_font_size = font_size * scale

            # Determine text appearance based on heaviness
            if heaviness <= 15:
                text_color = '#404040'  # Dark gray for very light
                size_adjustment = 0.9
            elif heaviness <= 25:
                text_color = '#303030'  # Darker gray for light
                size_adjustment = 0.95
            elif heaviness <= 50:
                text_color = '#000000'  # Black for regular
                size_adjustment = 1.0
            elif heaviness <= 75:
                text_color = '#000000'  # Black for bold
                size_adjustment = 1.1
            else:
                text_color = '#000000'  # Black for extra bold
                size_adjustment = 1.2

            preview_font_size *= size_adjustment

            # Determine font weight
            if heaviness <= 25:
                weight = 'normal'
            elif heaviness <= 75:
                weight = 'bold'
            else:
                weight = 'bold'  # Extra bold uses bold + offset

            # Create font
            try:
                font = (font_family, int(preview_font_size), weight)
            except:
                font = ('Arial', int(preview_font_size), weight)

            # Draw text with offset for bold effects
            center_x = rect_x + rect_w / 2
            center_y = rect_y + rect_h / 2

            if heaviness > 75:  # Extra bold - multiple overlays
                offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0),
                          (0, 1), (1, -1), (1, 0), (1, 1)]
                for dx, dy in offsets:
                    self.preview_canvas.create_text(
                        center_x + dx, center_y + dy,
                        text=text, font=font, fill=text_color
                    )
            elif heaviness > 50:  # Bold - 5-way overlay
                offsets = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
                for dx, dy in offsets:
                    self.preview_canvas.create_text(
                        center_x + dx, center_y + dy,
                        text=text, font=font, fill=text_color
                    )
            else:  # Regular or light - single text
                self.preview_canvas.create_text(
                    center_x, center_y,
                    text=text, font=font, fill=text_color
                )

            # Add dimensions label
            dim_text = f"{width}mm × {height}mm"
            self.preview_canvas.create_text(
                canvas_w / 2, rect_y + rect_h + 20,
                text=dim_text, font=('Arial', 10), fill='#666666'
            )

        except Exception as e:
            self.logger.error(f"Preview update failed: {e}")

    def _calculate_preview_font_size(self, text: str, rect_w: float, rect_h: float,
                                    font_family: str, heaviness: int) -> float:
        """Calculate font size for preview"""
        # Font-specific width factors (same as backend)
        font_widths = {
            'Impact': 0.45,
            'Arial': 0.55,
            'Arial Black': 0.65,
            'Helvetica': 0.55,
            'Verdana': 0.65,
            'Tahoma': 0.60,
            'Trebuchet MS': 0.58,
            'Gill Sans': 0.52,
            'Futura': 0.60,
        }

        width_factor = font_widths.get(font_family, 0.55)
        width_factor += (heaviness / 100) * 0.15

        # Calculate based on constraints
        max_text_width = rect_w * 0.75
        font_size_width = max_text_width / (len(text) * width_factor) if text else 12
        font_size_height = rect_h * 0.6

        return min(font_size_width, font_size_height)

    def validate_inputs(self) -> bool:
        """Validate all inputs before generation"""
        # Get all parameters
        # Get text from Text widget if it exists, otherwise from StringVar
        if hasattr(self, 'text_input'):
            text = self.text_input.get('1.0', 'end-1c').strip()
        else:
            text = self.text_var.get()
        width = self.width_var.get()
        height = self.height_var.get()
        font_size = self.font_size_var.get() if not self.auto_size_var.get() else 12
        heaviness = self.heaviness_var.get()
        bottom_thickness = self.bottom_thickness_var.get()
        top_thickness = self.top_thickness_var.get()
        auto_size = self.auto_size_var.get()

        # Perform validation
        is_valid, errors, warnings = self.validator.pre_validate_all(
            text, width, height, font_size, heaviness,
            bottom_thickness, top_thickness, auto_size
        )

        # Display warnings in validation area if exists
        if hasattr(self, 'validation_text'):
            self.validation_text.delete(1.0, tk.END)

            if warnings:
                for warning in warnings:
                    self.validation_text.insert(tk.END, f"⚠️ {warning}\n", 'warning')

            if errors:
                for error in errors:
                    self.validation_text.insert(tk.END, f"❌ {error}\n", 'error')

        # Show error dialog for critical errors
        if not is_valid:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False

        # Show warning dialog if text might cut through
        if not auto_size:
            will_cut, confidence = self.validator.will_text_cut_through(
                text, font_size, heaviness, width, height, top_thickness
            )
            if will_cut and confidence > 70:
                response = messagebox.askquestion(
                    "Warning",
                    f"Text may cut completely through the top layer (confidence: {confidence}%).\n"
                    "This will cause the top layer STL export to fail.\n\n"
                    "Continue anyway?",
                    icon='warning'
                )
                if response == 'no':
                    return False

        return True

    def generate_sign(self):
        """Generate the sign STL files"""
        if not self.validate_inputs():
            return

        # Disable generate button
        self.generate_btn.config(state='disabled')
        self.status_var.set("Generating STL files...")

        # Start generation in thread
        thread = threading.Thread(target=self._generate_worker)
        thread.daemon = True
        thread.start()

    def _generate_worker(self):
        """Worker thread for sign generation"""
        try:
            # Get parameters
            # Get text from Text widget if it exists, otherwise from StringVar
            if hasattr(self, 'text_input'):
                text = self.text_input.get('1.0', 'end-1c').strip()
            else:
                text = self.text_var.get()
            width = self.width_var.get()
            height = self.height_var.get()
            font_family = self.font_family_var.get()
            font_size = None if self.auto_size_var.get() else self.font_size_var.get()
            heaviness = self.heaviness_var.get()
            bottom_thickness = self.bottom_thickness_var.get()
            top_thickness = self.top_thickness_var.get()
            auto_size = self.auto_size_var.get()

            # Generate sign
            models = self.generator.generate_sign(
                text=text,
                width=width,
                height=height,
                font_family=font_family,
                font_size=font_size,
                heaviness=heaviness,
                bottom_thickness=bottom_thickness,
                top_thickness=top_thickness,
                auto_size=auto_size,
                validate=True
            )

            # Export STL files
            metadata = {
                'heaviness': heaviness,
                'font': font_family,
                'width': width,
                'height': height
            }

            created_files = self.generator.export_stl(
                models=models,
                base_filename=text,
                metadata=metadata
            )

            # Update UI in main thread
            self.root.after(0, self._generation_complete, created_files)

        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            self.root.after(0, self._generation_failed, str(e))

    def _generation_complete(self, created_files: List[str]):
        """Handle successful generation completion"""
        self.generate_btn.config(state='normal')

        # Format file list
        file_list = "\n".join([os.path.basename(f) for f in created_files])

        # Update status
        self.status_var.set(f"✅ Generated {len(created_files)} files")

        # Show success dialog
        response = messagebox.showinfo(
            "Success",
            f"STL files generated successfully!\n\nCreated files:\n{file_list}\n\n"
            f"Files saved to: {self.generator.output_dir}"
        )

        # Add to recent files
        if created_files:
            self.config.add_recent_file(created_files[0])

        # Open output folder if configured
        if self.config.get("output.auto_open_folder", True):
            self.open_output_folder()

    def _generation_failed(self, error_msg: str):
        """Handle generation failure"""
        self.generate_btn.config(state='normal')
        self.status_var.set("❌ Generation failed")

        # Parse error for specific issues
        if "text cutout may have removed all material" in error_msg.lower():
            messagebox.showerror(
                "Generation Failed",
                "Text has cut completely through the top layer!\n\n"
                "Try one of these solutions:\n"
                "• Reduce font size\n"
                "• Reduce text heaviness\n"
                "• Increase top layer thickness\n"
                "• Use shorter text"
            )
        else:
            messagebox.showerror("Generation Failed", f"Failed to generate STL files:\n\n{error_msg}")

    def reset_to_defaults(self):
        """Reset all inputs to default values"""
        response = messagebox.askquestion(
            "Reset to Defaults",
            "This will reset all settings to default values. Continue?",
            icon='question'
        )

        if response == 'yes':
            defaults = self.config.DEFAULT_CONFIG["defaults"]
            self.text_var.set(defaults["text"])
            self.font_family_var.set(defaults["font"])
            self.width_var.set(defaults["width"])
            self.height_var.set(defaults["height"])
            self.font_size_var.set(defaults["font_size"])
            self.auto_size_var.set(defaults["auto_size"])
            self.heaviness_var.set(defaults["heaviness"])
            self.bottom_thickness_var.set(defaults["bottom_thickness"])
            self.top_thickness_var.set(defaults["top_thickness"])

            self.update_preview()
            self.status_var.set("Reset to defaults")

    def suggest_optimal_parameters(self):
        """Suggest optimal parameters based on text and dimensions"""
        # Get text from Text widget if it exists, otherwise from StringVar
        if hasattr(self, 'text_input'):
            text = self.text_input.get('1.0', 'end-1c').strip()
        else:
            text = self.text_var.get()
        width = self.width_var.get()
        height = self.height_var.get()

        suggestions = self.validator.suggest_parameters(text, width, height)

        # Apply suggestions
        if messagebox.askyesno("Apply Suggestions",
                               f"Suggested settings:\n"
                               f"Font size: {suggestions['font_size']}mm\n"
                               f"Heaviness: {suggestions['heaviness']}\n"
                               f"Auto-size: {'Yes' if suggestions['auto_size'] else 'No'}\n\n"
                               f"Apply these settings?"):
            self.font_size_var.set(suggestions['font_size'])
            self.heaviness_var.set(suggestions['heaviness'])
            self.auto_size_var.set(suggestions['auto_size'])
            self.bottom_thickness_var.set(suggestions['bottom_thickness'])
            self.top_thickness_var.set(suggestions['top_thickness'])
            self.update_preview()

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        output_dir = self.generator.output_dir
        if output_dir.exists():
            if platform.system() == 'Darwin':  # macOS
                os.system(f'open "{output_dir}"')
            elif platform.system() == 'Windows':
                os.startfile(str(output_dir))
            else:  # Linux
                os.system(f'xdg-open "{output_dir}"')

    # Menu Actions
    def new_sign(self):
        """Create a new sign (reset inputs)"""
        self.reset_to_defaults()

    def open_recent(self):
        """Open recent file dialog"""
        recent = self.config.get("recent_files", [])
        if not recent:
            messagebox.showinfo("No Recent Files", "No recent files found")
            return

        # Create dialog to select recent file
        dialog = tk.Toplevel(self.root)
        dialog.title("Recent Files")
        dialog.geometry("400x300")

        listbox = tk.Listbox(dialog)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for file in recent[:10]:
            listbox.insert(tk.END, os.path.basename(file))

        def load_selected():
            selection = listbox.curselection()
            if selection:
                filepath = recent[selection[0]]
                # Load the file settings if possible
                dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Load", command=load_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)

    def save_preset(self):
        """Save current settings as preset"""
        name = tk.simpledialog.askstring("Save Preset", "Enter preset name:")
        if name:
            settings = {
                "text": self.text_var.get(),
                "font": self.font_family_var.get(),
                "width": self.width_var.get(),
                "height": self.height_var.get(),
                "font_size": self.font_size_var.get(),
                "auto_size": self.auto_size_var.get(),
                "heaviness": self.heaviness_var.get(),
                "bottom_thickness": self.bottom_thickness_var.get(),
                "top_thickness": self.top_thickness_var.get()
            }
            self.config.save_preset(name, settings)
            messagebox.showinfo("Preset Saved", f"Preset '{name}' saved successfully")
            self._update_preset_list()

    def load_preset(self):
        """Load a saved preset"""
        presets = self.config.get_presets()
        if not presets:
            messagebox.showinfo("No Presets", "No saved presets found")
            return

        # Create preset selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Load Preset")
        dialog.geometry("300x200")

        listbox = tk.Listbox(dialog)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for name in presets.keys():
            listbox.insert(tk.END, name)

        def load_selected():
            selection = listbox.curselection()
            if selection:
                name = list(presets.keys())[selection[0]]
                settings = presets[name]
                self._apply_preset(settings)
                dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Load", command=load_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)

    def _apply_preset(self, settings: Dict[str, Any]):
        """Apply preset settings"""
        self.text_var.set(settings.get("text", "LABEL"))
        self.font_family_var.set(settings.get("font", "Arial"))
        self.width_var.set(settings.get("width", 100))
        self.height_var.set(settings.get("height", 25))
        self.font_size_var.set(settings.get("font_size", 16))
        self.auto_size_var.set(settings.get("auto_size", False))
        self.heaviness_var.set(settings.get("heaviness", 50))
        self.bottom_thickness_var.set(settings.get("bottom_thickness", 1.0))
        self.top_thickness_var.set(settings.get("top_thickness", 1.0))

        self.update_preview()
        self.status_var.set("Preset loaded")

    def save_current_as_preset(self):
        """Save current settings as a new preset"""
        self.save_preset()

    def delete_selected_preset(self):
        """Delete the selected preset"""
        if not hasattr(self, 'presets_listbox'):
            return

        selection = self.presets_listbox.curselection()
        if selection:
            preset_name = self.presets_listbox.get(selection[0])
            if messagebox.askyesno("Delete Preset", f"Delete preset '{preset_name}'?"):
                presets = self.config.get_presets()
                if preset_name in presets:
                    del presets[preset_name]
                    self.config.set("presets", presets)
                    self._update_preset_list()

    def rename_selected_preset(self):
        """Rename the selected preset"""
        if not hasattr(self, 'presets_listbox'):
            return

        selection = self.presets_listbox.curselection()
        if selection:
            old_name = self.presets_listbox.get(selection[0])
            new_name = simpledialog.askstring("Rename Preset", f"New name for '{old_name}':")
            if new_name:
                presets = self.config.get_presets()
                if old_name in presets:
                    presets[new_name] = presets.pop(old_name)
                    self.config.set("presets", presets)
                    self._update_preset_list()

    def load_selected_preset(self):
        """Load the selected preset from listbox"""
        if not hasattr(self, 'presets_listbox'):
            return

        selection = self.presets_listbox.curselection()
        if selection:
            preset_name = self.presets_listbox.get(selection[0])
            preset = self.config.load_preset(preset_name)
            if preset:
                self._apply_preset(preset)

    def _update_preset_list(self):
        """Update preset list in UI if visible"""
        if hasattr(self, 'presets_listbox'):
            self.presets_listbox.delete(0, tk.END)
            presets = self.config.get_presets()
            for name in presets.keys():
                self.presets_listbox.insert(tk.END, name)

    def export_settings(self):
        """Export current settings to file"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            if self.config.export_config(filepath):
                messagebox.showinfo("Export Successful", f"Settings exported to {filepath}")
            else:
                messagebox.showerror("Export Failed", "Failed to export settings")

    def import_settings(self):
        """Import settings from file"""
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            if self.config.import_config(filepath):
                # Reload settings
                self._initialize_variables()
                self.update_preview()
                messagebox.showinfo("Import Successful", "Settings imported successfully")
            else:
                messagebox.showerror("Import Failed", "Failed to import settings")

    def show_preferences(self):
        """Show preferences dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Preferences")
        dialog.geometry("500x400")

        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # General tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")

        ttk.Label(general_frame, text="Output Directory:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        output_var = tk.StringVar(value=self.config.get("output.directory", "output"))
        ttk.Entry(general_frame, textvariable=output_var, width=30).grid(row=0, column=1, padx=10, pady=5)

        auto_open_var = tk.BooleanVar(value=self.config.get("output.auto_open_folder", True))
        ttk.Checkbutton(general_frame, text="Auto-open output folder", variable=auto_open_var).grid(
            row=1, column=0, columnspan=2, sticky='w', padx=10, pady=5
        )

        # Advanced tab
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Advanced")

        debug_var = tk.BooleanVar(value=self.config.get("advanced.debug_mode", False))
        ttk.Checkbutton(advanced_frame, text="Debug mode", variable=debug_var).grid(
            row=0, column=0, sticky='w', padx=10, pady=5
        )

        preview_var = tk.BooleanVar(value=self.config.get("advanced.show_preview", True))
        ttk.Checkbutton(advanced_frame, text="Show preview", variable=preview_var).grid(
            row=1, column=0, sticky='w', padx=10, pady=5
        )

        auto_update_var = tk.BooleanVar(value=self.config.get("advanced.auto_preview_update", True))
        ttk.Checkbutton(advanced_frame, text="Auto-update preview", variable=auto_update_var).grid(
            row=2, column=0, sticky='w', padx=10, pady=5
        )

        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)

        def save_preferences():
            self.config.set("output.directory", output_var.get())
            self.config.set("output.auto_open_folder", auto_open_var.get())
            self.config.set("advanced.debug_mode", debug_var.get())
            self.config.set("advanced.show_preview", preview_var.get())
            self.config.set("advanced.auto_preview_update", auto_update_var.get())

            # Apply debug mode
            if debug_var.get() != self.debug_var.get():
                self.debug_var.set(debug_var.get())
                self.on_debug_changed()

            dialog.destroy()
            messagebox.showinfo("Preferences", "Preferences saved")

        ttk.Button(btn_frame, text="Save", command=save_preferences).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)

    def show_about(self):
        """Show about dialog"""
        about_text = """Parametric Sign Generator v1.0

A tool for creating customizable two-color signs for 3D printing.

Optimized for Bambu Lab P1S printers with bi-color capability.

© 2024 - Created with CadQuery"""

        messagebox.showinfo("About", about_text)

    def show_user_guide(self):
        """Show user guide"""
        guide = tk.Toplevel(self.root)
        guide.title("User Guide")
        guide.geometry("600x500")

        text = tk.Text(guide, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(guide, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        guide_text = """PARAMETRIC SIGN GENERATOR - USER GUIDE

BASIC USAGE:
1. Enter the text you want on your sign
2. Set the width and height in millimeters
3. Choose a font from the dropdown or preset buttons
4. Adjust text weight with the slider (0-100)
5. Set layer thicknesses (typically 1mm each)
6. Click "Generate STL Files"

TEXT WEIGHT SETTINGS:
• Light (0-25): Thin, delicate text
• Regular (26-50): Standard text weight
• Bold (51-75): Heavier, more prominent text
• Extra Bold (76-100): Maximum text weight

AUTO-SIZE FEATURE:
When enabled, the font size is automatically calculated to fit your text within the sign dimensions. Disable to manually set font size.

LAYER THICKNESS:
• Bottom Layer: The base layer (typically black)
• Top Layer: The layer with text cutout (typically yellow)
• Standard recommendation: 1mm each

TIPS FOR BEST RESULTS:
• Keep text concise for better readability
• Test print small samples before large signs
• Heavier text may require thicker top layer
• Use preview to check text fit before generating

TROUBLESHOOTING:
• If top layer file is missing: Text has cut through completely. Reduce font size or heaviness.
• If text is too small: Disable auto-size and set manual font size
• If generation fails: Check that all inputs are valid numbers

KEYBOARD SHORTCUTS:
• Ctrl/Cmd + N: New sign
• Ctrl/Cmd + G: Generate STL files
• Ctrl/Cmd + R: Reset to defaults
• Ctrl/Cmd + Q: Quit application"""

        text.insert('1.0', guide_text)
        text.config(state='disabled')

    def show_troubleshooting(self):
        """Show troubleshooting help"""
        trouble = tk.Toplevel(self.root)
        trouble.title("Troubleshooting")
        trouble.geometry("500x400")

        text = tk.Text(trouble, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(trouble, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        trouble_text = """TROUBLESHOOTING COMMON ISSUES

PROBLEM: Top layer STL file is not generated
CAUSE: Text has cut completely through the layer
SOLUTIONS:
• Reduce font size
• Reduce text heaviness (lower value)
• Increase top layer thickness
• Use shorter text

PROBLEM: Text is too small on the sign
SOLUTIONS:
• Disable "Auto-size font" checkbox
• Manually increase font size value
• Reduce sign dimensions
• Use fewer characters

PROBLEM: Preview doesn't update
SOLUTIONS:
• Check "Auto-update preview" in Preferences
• Click in another field to trigger update
• Restart the application

PROBLEM: Generation takes too long
SOLUTIONS:
• Simplify text (fewer characters)
• Reduce text heaviness
• Close other applications
• Enable threading in preferences

PROBLEM: Files won't open in slicer
SOLUTIONS:
• Ensure STL files are not empty (>1KB)
• Try opening in different slicer software
• Regenerate with different parameters
• Check file permissions

PROBLEM: Validation errors appear
SOLUTIONS:
• Ensure all numeric fields have valid numbers
• Check dimensions are within limits (10-500mm width, 5-200mm height)
• Ensure text field is not empty
• Font size must be 5-50mm when not auto-sized

For additional help, check the User Guide or visit the project repository."""

        text.insert('1.0', trouble_text)
        text.config(state='disabled')

    def toggle_preview(self):
        """Toggle preview panel visibility"""
        current = self.config.get("advanced.show_preview", True)
        self.config.set("advanced.show_preview", not current)

        if hasattr(self, 'preview_frame'):
            if current:
                self.preview_frame.pack_forget()
            else:
                self.preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5)
                self.update_preview()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SignGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()