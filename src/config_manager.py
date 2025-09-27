"""
Configuration management for Sign Generator
Handles user preferences, defaults, and settings persistence
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration and user preferences"""

    DEFAULT_CONFIG = {
        "window": {
            "width": 1100,
            "height": 820,
            "resizable": True,
            "min_width": 1000,
            "min_height": 750
        },
        "defaults": {
            "text": "LABEL",
            "font": "Arial",
            "width": 100.0,
            "height": 25.0,
            "font_size": 16.0,
            "auto_size": False,
            "heaviness": 50,
            "bottom_thickness": 1.0,
            "top_thickness": 1.0,
            "corner_radius": 2.0
        },
        "output": {
            "directory": "output",
            "auto_open_folder": True,
            "file_naming": "{text}_{font}_{weight}"
        },
        "advanced": {
            "debug_mode": False,
            "show_preview": True,
            "auto_preview_update": True,
            "max_text_length": 100,
            "threading_enabled": True
        },
        "validation": {
            "width_min": 10,
            "width_max": 500,
            "height_min": 5,
            "height_max": 200,
            "font_size_min": 5,
            "font_size_max": 50,
            "thickness_min": 0.2,
            "thickness_max": 5.0
        },
        "recent_files": [],
        "favorite_fonts": ["Arial", "Helvetica", "Verdana", "Impact"],
        "presets": {}
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager

        Args:
            config_path: Optional path to config file. If None, uses default location
        """
        if config_path is None:
            self.config_dir = Path.home() / ".sign_generator"
            self.config_path = self.config_dir / "config.json"
        else:
            self.config_path = Path(config_path)
            self.config_dir = self.config_path.parent

        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_configs(self.DEFAULT_CONFIG, loaded_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()

    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """Save configuration to file"""
        if config is None:
            config = self.config

        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")

    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """Recursively merge loaded config with defaults"""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation

        Args:
            key_path: Dot-separated path to config value (e.g., "defaults.font")
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, key_path: str, value: Any, save: bool = True):
        """Set a configuration value using dot notation

        Args:
            key_path: Dot-separated path to config value
            value: Value to set
            save: Whether to save config immediately
        """
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value

        if save:
            self.save_config()

    def add_recent_file(self, filepath: str, max_recent: int = 10):
        """Add a file to recent files list"""
        recent = self.config.get("recent_files", [])
        if filepath in recent:
            recent.remove(filepath)
        recent.insert(0, filepath)
        self.config["recent_files"] = recent[:max_recent]
        self.save_config()

    def save_preset(self, name: str, settings: Dict[str, Any]):
        """Save a named preset"""
        if "presets" not in self.config:
            self.config["presets"] = {}
        self.config["presets"][name] = settings
        self.save_config()

    def load_preset(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a named preset"""
        return self.config.get("presets", {}).get(name)

    def get_presets(self) -> Dict[str, Dict[str, Any]]:
        """Get all saved presets"""
        return self.config.get("presets", {})

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()

    def export_config(self, filepath: str):
        """Export configuration to a file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError:
            return False

    def import_config(self, filepath: str) -> bool:
        """Import configuration from a file"""
        try:
            with open(filepath, 'r') as f:
                imported = json.load(f)
                self.config = self._merge_configs(self.DEFAULT_CONFIG, imported)
                self.save_config()
            return True
        except (json.JSONDecodeError, IOError):
            return False