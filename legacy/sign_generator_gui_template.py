#!/usr/bin/env python3
"""
Parametric Sign Generator GUI Application
Starter template for Claude Code to build upon
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import threading

# Import the backend (adapt from existing CLI generator)
# from cadquery_sign_generator import CadQuerySignGenerator

class SignGeneratorGUI:
    """Main GUI Application for Sign Generation"""
    
    def __init__(self):
        """Initialize the GUI application"""
        self.root = tk.Tk()
        self.root.title("Parametric Sign Generator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Variables for input fields
        self.text_var = tk.StringVar(value="LABEL")
        self.width_var = tk.DoubleVar(value=100.0)
        self.height_var = tk.DoubleVar(value=25.0)
        self.heaviness_var = tk.IntVar(value=50)
        self.heaviness_preset = tk.StringVar(value="Regular")
        self.bottom_thickness_var = tk.DoubleVar(value=1.0)
        self.top_thickness_var = tk.DoubleVar(value=1.0)
        
        # Initialize backend (TODO)
        # self.backend = SignBackend()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        row = 0
        
        # Title
        title_label = ttk.Label(main_frame, text="🏷️ Parametric Sign Generator", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, 
                                                            columnspan=2, sticky='ew', pady=5)
        row += 1
        
        # Text Input Section
        ttk.Label(main_frame, text="Text to Print:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        
        self.text_input = tk.Text(main_frame, height=3, width=40, wrap=tk.WORD)
        self.text_input.grid(row=row, column=0, columnspan=2, pady=5, sticky='ew')
        self.text_input.insert(1.0, "LABEL")
        row += 1
        
        # Label Dimensions Section
        ttk.Label(main_frame, text="Label Dimensions (mm):", 
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1
        
        dims_frame = ttk.Frame(main_frame)
        dims_frame.grid(row=row, column=0, columnspan=2, sticky='ew')
        
        ttk.Label(dims_frame, text="Width:").pack(side=tk.LEFT, padx=5)
        self.width_spin = ttk.Spinbox(dims_frame, from_=10, to=500, width=10,
                                      textvariable=self.width_var, increment=5)
        self.width_spin.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(dims_frame, text="Height:").pack(side=tk.LEFT, padx=20)
        self.height_spin = ttk.Spinbox(dims_frame, from_=5, to=200, width=10,
                                       textvariable=self.height_var, increment=5)
        self.height_spin.pack(side=tk.LEFT, padx=5)
        row += 1
        
        # Text Heaviness Section (KEY FEATURE)
        ttk.Label(main_frame, text="Text Heaviness:", 
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1
        
        # Radio buttons for presets
        presets_frame = ttk.Frame(main_frame)
        presets_frame.grid(row=row, column=0, columnspan=2, sticky='ew')
        
        presets = [("Light", 25), ("Regular", 50), ("Bold", 75), ("Extra Bold", 100)]
        for text, value in presets:
            rb = ttk.Radiobutton(presets_frame, text=text, variable=self.heaviness_preset,
                                value=text, command=lambda v=value: self.set_heaviness(v))
            rb.pack(side=tk.LEFT, padx=10)
        row += 1
        
        # Slider for fine control
        slider_frame = ttk.Frame(main_frame)
        slider_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(slider_frame, text="Fine Control:").pack(side=tk.LEFT, padx=5)
        self.heaviness_slider = ttk.Scale(slider_frame, from_=0, to=100, 
                                         orient='horizontal', variable=self.heaviness_var,
                                         command=self.on_heaviness_change)
        self.heaviness_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.heaviness_label = ttk.Label(slider_frame, text="50")
        self.heaviness_label.pack(side=tk.LEFT, padx=5)
        row += 1
        
        # Layer Thickness Section
        ttk.Label(main_frame, text="Layer Thickness (mm):", 
                 font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1
        
        thickness_frame = ttk.Frame(main_frame)
        thickness_frame.grid(row=row, column=0, columnspan=2, sticky='ew')
        
        ttk.Label(thickness_frame, text="Bottom:").pack(side=tk.LEFT, padx=5)
        self.bottom_spin = ttk.Spinbox(thickness_frame, from_=0.2, to=5.0, width=10,
                                       textvariable=self.bottom_thickness_var,
                                       increment=0.1, format="%.1f")
        self.bottom_spin.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(thickness_frame, text="Top:").pack(side=tk.LEFT, padx=20)
        self.top_spin = ttk.Spinbox(thickness_frame, from_=0.2, to=5.0, width=10,
                                    textvariable=self.top_thickness_var,
                                    increment=0.1, format="%.1f")
        self.top_spin.pack(side=tk.LEFT, padx=5)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        self.generate_btn = ttk.Button(button_frame, text="Generate STL ✓",
                                      command=self.generate_stl)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.preview_btn = ttk.Button(button_frame, text="Preview",
                                     command=self.preview, state=tk.DISABLED)
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = ttk.Button(button_frame, text="Reset",
                                   command=self.reset_fields)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        row += 1
        
        # Status Bar
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0,
                                                           columnspan=2, sticky='ew', pady=5)
        row += 1
        
        self.status_label = ttk.Label(main_frame, text="Status: Ready", 
                                     foreground='green')
        self.status_label.grid(row=row, column=0, sticky=tk.W)
        row += 1
        
        self.output_label = ttk.Label(main_frame, text="Output: -", 
                                     foreground='gray')
        self.output_label.grid(row=row, column=0, columnspan=2, sticky=tk.W)
        
    def set_heaviness(self, value):
        """Set heaviness from preset button"""
        self.heaviness_var.set(value)
        
    def on_heaviness_change(self, value):
        """Handle heaviness slider change"""
        val = int(float(value))
        self.heaviness_label.config(text=str(val))
        
        # Update radio button selection based on slider
        if val <= 35:
            self.heaviness_preset.set("Light")
        elif val <= 65:
            self.heaviness_preset.set("Regular")
        elif val <= 85:
            self.heaviness_preset.set("Bold")
        else:
            self.heaviness_preset.set("Extra Bold")
    
    def validate_inputs(self):
        """Validate all input fields"""
        # Get text
        text = self.text_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter text to print")
            return False
        
        # Check dimensions
        if self.width_var.get() < 10 or self.width_var.get() > 500:
            messagebox.showerror("Error", "Width must be between 10 and 500mm")
            return False
            
        if self.height_var.get() < 5 or self.height_var.get() > 200:
            messagebox.showerror("Error", "Height must be between 5 and 200mm")
            return False
        
        return True
    
    def generate_stl(self):
        """Generate STL files with current parameters"""
        if not self.validate_inputs():
            return
        
        # Disable buttons during generation
        self.generate_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Generating...", foreground='orange')
        self.root.update()
        
        # Get parameters
        text = self.text_input.get(1.0, tk.END).strip()
        width = self.width_var.get()
        height = self.height_var.get()
        heaviness = self.heaviness_var.get()
        bottom_thickness = self.bottom_thickness_var.get()
        top_thickness = self.top_thickness_var.get()
        
        # TODO: Call backend to generate files
        # This is where you'll integrate with cadquery_sign_generator.py
        """
        try:
            # Example backend call (implement this)
            backend = SignBackend()
            result = backend.generate_with_heaviness(
                text=text,
                width=width,
                height=height,
                heaviness=heaviness,
                bottom_thickness=bottom_thickness,
                top_thickness=top_thickness
            )
            
            if result.success:
                self.status_label.config(text="Status: Success!", foreground='green')
                self.output_label.config(text=f"Output: {result.output_dir}")
                messagebox.showinfo("Success", f"Files generated:\n{result.files}")
            else:
                raise Exception(result.error)
                
        except Exception as e:
            self.status_label.config(text="Status: Error", foreground='red')
            messagebox.showerror("Generation Error", str(e))
        """
        
        # Temporary placeholder success message
        import time
        time.sleep(2)  # Simulate generation time
        self.status_label.config(text="Status: Success!", foreground='green')
        self.output_label.config(text="Output: output/sign_*.stl")
        messagebox.showinfo("Success", 
                          "Files generated successfully!\n\n"
                          "• sign_bottom_white.stl\n"
                          "• sign_top_yellow.stl\n"
                          "• sign_combined_preview.stl")
        
        # Re-enable buttons
        self.generate_btn.config(state=tk.NORMAL)
        self.preview_btn.config(state=tk.NORMAL)
    
    def preview(self):
        """Show preview of generated sign"""
        messagebox.showinfo("Preview", "Preview feature coming soon!\n\n"
                          "This will show a 2D or 3D preview of your sign.")
    
    def reset_fields(self):
        """Reset all fields to defaults"""
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, "LABEL")
        self.width_var.set(100.0)
        self.height_var.set(25.0)
        self.heaviness_var.set(50)
        self.heaviness_preset.set("Regular")
        self.bottom_thickness_var.set(1.0)
        self.top_thickness_var.set(1.0)
        self.status_label.config(text="Status: Ready", foreground='green')
        self.output_label.config(text="Output: -", foreground='gray')
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


class SignBackend:
    """Backend engine for STL generation (TO BE IMPLEMENTED)"""
    
    def __init__(self):
        """Initialize the backend with CadQuery generator"""
        pass  # TODO: Import and initialize CadQuerySignGenerator
    
    def generate_with_heaviness(self, text, width, height, heaviness, 
                               bottom_thickness, top_thickness):
        """
        Generate STL files with text heaviness control
        
        Parameters:
        - text: Text to print on sign
        - width: Sign width in mm
        - height: Sign height in mm  
        - heaviness: Text boldness (0-100)
        - bottom_thickness: Base layer thickness in mm
        - top_thickness: Top layer thickness in mm
        
        Returns:
        - Result object with success status and file paths
        """
        # TODO: Implement this method
        # 1. Convert heaviness to font weight or stroke width
        # 2. Call CadQuery generator with parameters
        # 3. Return result with file paths
        pass
    
    def heaviness_to_font_weight(self, heaviness):
        """
        Convert heaviness value (0-100) to font weight
        
        Mapping:
        0-25: Light (font-weight 300)
        26-50: Regular (font-weight 400)
        51-75: Bold (font-weight 700)
        76-100: Extra Bold (font-weight 900)
        """
        if heaviness <= 25:
            return 300
        elif heaviness <= 50:
            return 400
        elif heaviness <= 75:
            return 700
        else:
            return 900


def main():
    """Main entry point"""
    app = SignGeneratorGUI()
    app.run()


if __name__ == "__main__":
    main()
