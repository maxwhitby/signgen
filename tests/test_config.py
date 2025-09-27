"""
Unit tests for config_manager module
"""

import pytest
import json
import tempfile
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_manager import ConfigManager


class TestConfigManager:
    """Test suite for ConfigManager class"""

    def setup_method(self):
        """Setup test fixtures with temporary config file"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.json"
        self.config = ConfigManager(str(self.config_path))

    def teardown_method(self):
        """Cleanup temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_default_config(self):
        """Test loading default configuration"""
        assert self.config.config is not None
        assert "defaults" in self.config.config
        assert "window" in self.config.config
        assert "validation" in self.config.config

    def test_get_config_value(self):
        """Test getting configuration values"""
        value = self.config.get("defaults.text")
        assert value == "LABEL"

        value = self.config.get("defaults.width")
        assert value == 100.0

    def test_get_nested_config(self):
        """Test getting nested configuration values"""
        value = self.config.get("window.width")
        assert value == 1100

        value = self.config.get("validation.width_min")
        assert value == 10

    def test_get_with_default(self):
        """Test getting non-existent key with default"""
        value = self.config.get("nonexistent.key", "default_value")
        assert value == "default_value"

    def test_set_config_value(self):
        """Test setting configuration values"""
        self.config.set("defaults.text", "CUSTOM", save=False)
        assert self.config.get("defaults.text") == "CUSTOM"

    def test_set_nested_config(self):
        """Test setting nested configuration values"""
        self.config.set("custom.nested.value", 42, save=False)
        assert self.config.get("custom.nested.value") == 42

    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        self.config.set("test.value", "saved_value")

        # Create new instance to load saved config
        new_config = ConfigManager(str(self.config_path))
        assert new_config.get("test.value") == "saved_value"

    def test_add_recent_file(self):
        """Test adding recent files"""
        self.config.add_recent_file("file1.stl")
        self.config.add_recent_file("file2.stl")

        recent = self.config.config.get("recent_files")
        assert len(recent) == 2
        assert recent[0] == "file2.stl"  # Most recent first

    def test_recent_files_max_limit(self):
        """Test recent files list respects max limit"""
        for i in range(15):
            self.config.add_recent_file(f"file{i}.stl")

        recent = self.config.config.get("recent_files")
        assert len(recent) <= 10

    def test_save_preset(self):
        """Test saving presets"""
        preset = {"width": 150, "height": 30}
        self.config.save_preset("large", preset)

        saved = self.config.load_preset("large")
        assert saved == preset

    def test_load_nonexistent_preset(self):
        """Test loading non-existent preset returns None"""
        preset = self.config.load_preset("nonexistent")
        assert preset is None

    def test_get_presets(self):
        """Test getting all presets"""
        self.config.save_preset("small", {"width": 50})
        self.config.save_preset("large", {"width": 200})

        presets = self.config.get_presets()
        assert len(presets) == 2
        assert "small" in presets
        assert "large" in presets

    def test_reset_to_defaults(self):
        """Test resetting configuration to defaults"""
        self.config.set("defaults.text", "MODIFIED", save=False)
        self.config.reset_to_defaults()

        assert self.config.get("defaults.text") == "LABEL"

    def test_export_import_config(self):
        """Test exporting and importing configuration"""
        export_path = Path(self.temp_dir) / "export.json"

        self.config.set("test.export", "exported", save=False)
        success = self.config.export_config(str(export_path))
        assert success is True

        new_config = ConfigManager()
        success = new_config.import_config(str(export_path))
        assert success is True
        assert new_config.get("test.export") == "exported"

    def test_merge_configs(self):
        """Test configuration merging preserves defaults"""
        loaded = {"defaults": {"text": "CUSTOM"}}
        merged = self.config._merge_configs(self.config.DEFAULT_CONFIG, loaded)

        assert merged["defaults"]["text"] == "CUSTOM"  # Override
        assert merged["defaults"]["width"] == 100.0  # Preserved default