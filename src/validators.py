"""
Validation utilities for Sign Generator
Pre-validates parameters to prevent generation failures
"""

from typing import Tuple, List, Optional
from .exceptions import ValidationError


class SignValidator:
    """Validates sign generation parameters"""

    def __init__(self, config=None):
        """Initialize validator with optional config"""
        if config:
            self.width_range = (
                config.get("validation.width_min", 10),
                config.get("validation.width_max", 500)
            )
            self.height_range = (
                config.get("validation.height_min", 5),
                config.get("validation.height_max", 200)
            )
            self.font_size_range = (
                config.get("validation.font_size_min", 5),
                config.get("validation.font_size_max", 50)
            )
            self.thickness_range = (
                config.get("validation.thickness_min", 0.2),
                config.get("validation.thickness_max", 5.0)
            )
        else:
            # Default ranges
            self.width_range = (10, 500)
            self.height_range = (5, 200)
            self.font_size_range = (5, 50)
            self.thickness_range = (0.2, 5.0)

    def validate_dimensions(self, width: float, height: float) -> Tuple[bool, Optional[str]]:
        """Validate sign dimensions"""
        errors = []

        if not self.width_range[0] <= width <= self.width_range[1]:
            errors.append(f"Width must be between {self.width_range[0]}-{self.width_range[1]}mm")

        if not self.height_range[0] <= height <= self.height_range[1]:
            errors.append(f"Height must be between {self.height_range[0]}-{self.height_range[1]}mm")

        # Check aspect ratio
        if width > 0 and height > 0:
            aspect_ratio = width / height
            if aspect_ratio > 20 or aspect_ratio < 0.05:
                errors.append(f"Unusual aspect ratio ({aspect_ratio:.1f}:1)")

        if errors:
            return False, "; ".join(errors)
        return True, None

    def validate_text(self, text: str, max_length: int = 100) -> Tuple[bool, Optional[str]]:
        """Validate text input"""
        if not text or not text.strip():
            return False, "Text cannot be empty"

        if len(text) > max_length:
            return False, f"Text too long (max {max_length} characters)"

        # Check for problematic characters
        problematic_chars = set()
        for char in text:
            if ord(char) > 127 and char not in "äöüÄÖÜßéèêëàâçñ":
                problematic_chars.add(char)

        if problematic_chars:
            return True, f"Warning: Special characters may not render correctly: {', '.join(problematic_chars)}"

        return True, None

    def validate_font_size(self, font_size: float, text: str, width: float,
                           auto_size: bool = False) -> Tuple[bool, Optional[str]]:
        """Validate font size relative to text and dimensions"""
        if auto_size:
            return True, None

        if not self.font_size_range[0] <= font_size <= self.font_size_range[1]:
            return False, f"Font size must be between {self.font_size_range[0]}-{self.font_size_range[1]}mm"

        # Estimate if text will fit
        avg_char_width = font_size * 0.6  # Rough estimate
        estimated_text_width = len(text) * avg_char_width

        if estimated_text_width > width * 1.2:
            return False, f"Text likely too wide for sign (estimated {estimated_text_width:.0f}mm, sign width {width:.0f}mm)"

        return True, None

    def validate_thickness(self, bottom: float, top: float) -> Tuple[bool, Optional[str]]:
        """Validate layer thicknesses"""
        errors = []

        if not self.thickness_range[0] <= bottom <= self.thickness_range[1]:
            errors.append(f"Bottom thickness must be between {self.thickness_range[0]}-{self.thickness_range[1]}mm")

        if not self.thickness_range[0] <= top <= self.thickness_range[1]:
            errors.append(f"Top thickness must be between {self.thickness_range[0]}-{self.thickness_range[1]}mm")

        total = bottom + top
        if total > 10:
            errors.append(f"Total thickness {total:.1f}mm may be excessive")

        if errors:
            return False, "; ".join(errors)
        return True, None

    def validate_heaviness(self, heaviness: int, font_size: float,
                          top_thickness: float) -> Tuple[bool, Optional[str]]:
        """Validate text heaviness settings"""
        warnings = []

        if not 0 <= heaviness <= 100:
            return False, "Heaviness must be between 0-100"

        # Check if heavy text might cut through layer
        if heaviness > 75 and font_size > 20 and top_thickness < 1.5:
            warnings.append("Heavy text with large font may cut through thin top layer")

        if heaviness > 90 and top_thickness < 2.0:
            warnings.append("Extra bold text may require thicker top layer")

        if warnings:
            return True, "; ".join(warnings)
        return True, None

    def pre_validate_all(self, text: str, width: float, height: float,
                         font_size: float, heaviness: int, bottom_thickness: float,
                         top_thickness: float, auto_size: bool = False) -> Tuple[bool, List[str], List[str]]:
        """Comprehensive pre-validation of all parameters

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        # Validate each component
        valid, msg = self.validate_text(text)
        if not valid:
            errors.append(msg)
        elif msg:  # Warning
            warnings.append(msg)

        valid, msg = self.validate_dimensions(width, height)
        if not valid:
            errors.append(msg)

        valid, msg = self.validate_font_size(font_size, text, width, auto_size)
        if not valid:
            errors.append(msg)

        valid, msg = self.validate_thickness(bottom_thickness, top_thickness)
        if not valid:
            errors.append(msg)

        valid, msg = self.validate_heaviness(heaviness, font_size, top_thickness)
        if not valid:
            errors.append(msg)
        elif msg:
            warnings.append(msg)

        return len(errors) == 0, errors, warnings

    def estimate_cut_area(self, text: str, font_size: float, heaviness: int) -> float:
        """Estimate the area that will be cut from the top layer"""
        # Base character area estimation
        char_area = (font_size * 0.7) * (font_size * 0.9)  # Rough character bounding box

        # Adjust for heaviness
        heaviness_factor = 1.0 + (heaviness / 100) * 0.5

        # Estimate total cut area
        return len(text) * char_area * heaviness_factor

    def will_text_cut_through(self, text: str, font_size: float, heaviness: int,
                              sign_width: float, sign_height: float,
                              top_thickness: float) -> Tuple[bool, float]:
        """Predict if text will cut completely through the top layer

        Returns:
            Tuple of (will_cut_through, confidence_percentage)
        """
        cut_area = self.estimate_cut_area(text, font_size, heaviness)
        sign_area = sign_width * sign_height

        # Calculate coverage ratio
        coverage_ratio = cut_area / sign_area

        # Factors that increase cut-through risk
        risk_score = 0

        if coverage_ratio > 0.7:
            risk_score += 40

        if heaviness > 80:
            risk_score += 20

        if font_size > sign_height * 0.8:
            risk_score += 20

        if top_thickness < 1.0:
            risk_score += 20

        # Multiple offset cuts for bold text increase risk
        if heaviness > 75:
            risk_score += 10

        will_cut_through = risk_score >= 60
        confidence = min(risk_score, 100)

        return will_cut_through, confidence

    def suggest_parameters(self, text: str, width: float, height: float) -> dict:
        """Suggest optimal parameters for given text and dimensions"""
        text_length = len(text)

        # Base font size on text length and dimensions
        if text_length <= 5:
            suggested_font = min(height * 0.6, width / (text_length * 0.8))
        elif text_length <= 10:
            suggested_font = min(height * 0.5, width / (text_length * 0.7))
        else:
            suggested_font = min(height * 0.4, width / (text_length * 0.6))

        # Clamp to valid range
        suggested_font = max(self.font_size_range[0],
                           min(suggested_font, self.font_size_range[1]))

        # Suggest moderate heaviness for reliability
        suggested_heaviness = 50

        # Standard thicknesses
        suggested_bottom = 1.0
        suggested_top = 1.0

        # If text is large relative to sign, suggest thicker top
        if suggested_font > height * 0.5:
            suggested_top = 1.5

        return {
            "font_size": round(suggested_font, 1),
            "heaviness": suggested_heaviness,
            "bottom_thickness": suggested_bottom,
            "top_thickness": suggested_top,
            "auto_size": text_length > 15  # Suggest auto-size for long text
        }