"""
Unit tests for validators module
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validators import SignValidator


class TestSignValidator:
    """Test suite for SignValidator class"""

    def setup_method(self):
        """Setup test fixtures"""
        self.validator = SignValidator()

    def test_validate_dimensions_valid(self):
        """Test valid dimensions pass validation"""
        valid, msg = self.validator.validate_dimensions(100, 25)
        assert valid is True
        assert msg is None

    def test_validate_dimensions_invalid_width(self):
        """Test invalid width fails validation"""
        valid, msg = self.validator.validate_dimensions(5, 25)  # Too narrow
        assert valid is False
        assert "Width must be between" in msg

    def test_validate_dimensions_invalid_height(self):
        """Test invalid height fails validation"""
        valid, msg = self.validator.validate_dimensions(100, 2)  # Too short
        assert valid is False
        assert "Height must be between" in msg

    def test_validate_dimensions_bad_aspect_ratio(self):
        """Test unusual aspect ratio triggers warning"""
        valid, msg = self.validator.validate_dimensions(500, 10)  # Very wide
        assert valid is False
        assert "aspect ratio" in msg.lower()

    def test_validate_text_valid(self):
        """Test valid text passes validation"""
        valid, msg = self.validator.validate_text("LABEL")
        assert valid is True
        assert msg is None

    def test_validate_text_empty(self):
        """Test empty text fails validation"""
        valid, msg = self.validator.validate_text("")
        assert valid is False
        assert "cannot be empty" in msg

    def test_validate_text_too_long(self):
        """Test overly long text fails validation"""
        valid, msg = self.validator.validate_text("A" * 101)
        assert valid is False
        assert "too long" in msg.lower()

    def test_validate_font_size_valid(self):
        """Test valid font size passes validation"""
        valid, msg = self.validator.validate_font_size(16, "TEST", 100, False)
        assert valid is True
        assert msg is None

    def test_validate_font_size_auto(self):
        """Test auto-size always passes"""
        valid, msg = self.validator.validate_font_size(999, "TEST", 100, True)
        assert valid is True
        assert msg is None

    def test_validate_font_size_too_large(self):
        """Test overly large font fails validation"""
        valid, msg = self.validator.validate_font_size(60, "TEST", 100, False)
        assert valid is False
        assert "Font size must be between" in msg

    def test_validate_thickness_valid(self):
        """Test valid thickness passes validation"""
        valid, msg = self.validator.validate_thickness(1.0, 1.0)
        assert valid is True
        assert msg is None

    def test_validate_thickness_too_thin(self):
        """Test overly thin layers fail validation"""
        valid, msg = self.validator.validate_thickness(0.1, 0.1)
        assert valid is False
        assert "thickness must be between" in msg.lower()

    def test_validate_heaviness_valid(self):
        """Test valid heaviness passes validation"""
        valid, msg = self.validator.validate_heaviness(50, 16, 1.0)
        assert valid is True
        assert msg is None

    def test_validate_heaviness_warning(self):
        """Test heavy text with thin layer triggers warning"""
        valid, msg = self.validator.validate_heaviness(90, 25, 1.0)
        assert valid is True  # Warning, not error
        assert "may cut through" in msg.lower() or "thicker" in msg.lower()

    def test_pre_validate_all_valid(self):
        """Test comprehensive validation with valid parameters"""
        is_valid, errors, warnings = self.validator.pre_validate_all(
            "TEST", 100, 25, 16, 50, 1.0, 1.0, False
        )
        assert is_valid is True
        assert len(errors) == 0

    def test_pre_validate_all_with_errors(self):
        """Test comprehensive validation catches errors"""
        is_valid, errors, warnings = self.validator.pre_validate_all(
            "", 5, 2, 100, 150, 0.1, 0.1, False
        )
        assert is_valid is False
        assert len(errors) > 0

    def test_estimate_cut_area(self):
        """Test cut area estimation"""
        area = self.validator.estimate_cut_area("TEST", 16, 50)
        assert area > 0
        assert isinstance(area, float)

    def test_will_text_cut_through(self):
        """Test cut-through prediction"""
        # Large text on small sign should predict cut-through
        will_cut, confidence = self.validator.will_text_cut_through(
            "BIGTEXT", 40, 90, 50, 25, 0.5
        )
        assert isinstance(will_cut, bool)
        assert 0 <= confidence <= 100

    def test_suggest_parameters(self):
        """Test parameter suggestion"""
        suggestions = self.validator.suggest_parameters("LABEL", 100, 25)
        assert "font_size" in suggestions
        assert "heaviness" in suggestions
        assert "bottom_thickness" in suggestions
        assert "top_thickness" in suggestions
        assert suggestions["font_size"] > 0