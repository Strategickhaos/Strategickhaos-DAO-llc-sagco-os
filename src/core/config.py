#!/usr/bin/env python3
"""
SAGCO OS Configuration Manager
Centralized configuration management with profiles
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from pathlib import Path
from datetime import datetime
import json
import os


@dataclass
class ConfigProfile:
    """Configuration profile"""
    name: str
    settings: Dict[str, Any] = field(default_factory=dict)
    parent: Optional[str] = None  # Inherit from parent profile
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)


class ConfigManager:
    """
    Configuration management system for SAGCO OS
    Supports profiles, inheritance, and environment overrides
    """
    
    DEFAULT_CONFIG = {
        "system": {
            "version": "0.1.0",
            "name": "SAGCO OS",
            "owner": "Strategickhaos DAO LLC",
            "operator": "Dom (Me10101)"
        },
        "security": {
            "session_timeout_hours": 8,
            "password_min_length": 8,
            "max_login_attempts": 5,
            "require_2fa": False
        },
        "memory": {
            "l1_cache_size": 1000,
            "l2_storage_enabled": True,
            "l3_persistent_enabled": True,
            "cleanup_interval_seconds": 300
        },
        "scheduler": {
            "max_workers": 4,
            "queue_size": 1000,
            "task_timeout_seconds": 3600
        },
        "ipc": {
            "event_history_size": 1000,
            "queue_timeout_seconds": 30,
            "enable_channels": True
        },
        "logging": {
            "level": "INFO",
            "format": "json",
            "output": ["console", "file"],
            "file_path": "/var/log/sagco/sagco.log",
            "max_file_size_mb": 100,
            "retention_days": 30
        },
        "bloom": {
            "enabled_levels": ["REMEMBER", "UNDERSTAND", "APPLY", "ANALYZE", "EVALUATE", "CREATE"],
            "default_level": "UNDERSTAND"
        },
        "collapse": {
            "required_channels": 2,  # Minimum channels for partial collapse
            "full_collapse_channels": 4  # All channels required
        }
    }
    
    PROFILES = {
        "development": {
            "logging": {
                "level": "DEBUG",
                "output": ["console"]
            },
            "security": {
                "session_timeout_hours": 24,
                "require_2fa": False
            }
        },
        "production": {
            "logging": {
                "level": "WARNING",
                "output": ["file"]
            },
            "security": {
                "session_timeout_hours": 4,
                "require_2fa": True,
                "max_login_attempts": 3
            },
            "scheduler": {
                "max_workers": 8
            }
        },
        "testing": {
            "logging": {
                "level": "DEBUG",
                "output": ["console"]
            },
            "memory": {
                "l1_cache_size": 100
            },
            "scheduler": {
                "max_workers": 2
            }
        }
    }
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".sagco" / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.active_profile = "development"
        self.config = self._load_config()
        self.custom_profiles: Dict[str, ConfigProfile] = {}
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with profile and env overrides"""
        # Start with default config
        config = self.DEFAULT_CONFIG.copy()
        
        # Apply profile settings
        profile_settings = self.PROFILES.get(self.active_profile, {})
        config = self._deep_merge(config, profile_settings)
        
        # Apply environment variable overrides
        # Format: SAGCO_SECTION_KEY=value
        for key, value in os.environ.items():
            if key.startswith("SAGCO_"):
                parts = key[6:].lower().split("_", 1)
                if len(parts) == 2:
                    section, setting = parts
                    if section in config:
                        # Try to parse as JSON, fall back to string
                        try:
                            config[section][setting] = json.loads(value)
                        except (json.JSONDecodeError, ValueError):
                            config[section][setting] = value
        
        return config
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any) -> None:
        """Set configuration value (runtime only)"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self.config.get(section, {})
    
    def set_profile(self, profile_name: str) -> None:
        """Switch to different configuration profile"""
        if profile_name not in self.PROFILES and profile_name not in self.custom_profiles:
            raise ValueError(f"Unknown profile: {profile_name}")
        
        self.active_profile = profile_name
        self.config = self._load_config()
    
    def create_profile(
        self,
        name: str,
        settings: Dict[str, Any],
        parent: Optional[str] = None
    ) -> ConfigProfile:
        """Create custom configuration profile"""
        profile = ConfigProfile(
            name=name,
            settings=settings,
            parent=parent
        )
        self.custom_profiles[name] = profile
        return profile
    
    def save_config(self, filepath: Optional[Path] = None) -> None:
        """Save current configuration to file"""
        if filepath is None:
            filepath = self.config_dir / f"{self.active_profile}.json"
        
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=2, default=str)
    
    def load_config_file(self, filepath: Path) -> None:
        """Load configuration from file"""
        with open(filepath, 'r') as f:
            file_config = json.load(f)
        
        self.config = self._deep_merge(self.config, file_config)
    
    def get_all(self) -> Dict[str, Any]:
        """Get complete configuration"""
        return self.config.copy()
    
    def get_status(self) -> Dict[str, Any]:
        """Get configuration manager status"""
        return {
            "active_profile": self.active_profile,
            "config_dir": str(self.config_dir),
            "available_profiles": list(self.PROFILES.keys()) + list(self.custom_profiles.keys()),
            "sections": list(self.config.keys()),
            "custom_profiles": len(self.custom_profiles)
        }
    
    def validate(self) -> List[str]:
        """Validate configuration, return list of issues"""
        issues = []
        
        # Validate required sections
        required_sections = ["system", "security", "memory", "scheduler", "ipc"]
        for section in required_sections:
            if section not in self.config:
                issues.append(f"Missing required section: {section}")
        
        # Validate specific settings
        if self.get("security", "session_timeout_hours", 0) < 1:
            issues.append("security.session_timeout_hours must be >= 1")
        
        if self.get("memory", "l1_cache_size", 0) < 10:
            issues.append("memory.l1_cache_size must be >= 10")
        
        if self.get("scheduler", "max_workers", 0) < 1:
            issues.append("scheduler.max_workers must be >= 1")
        
        return issues


def get_config() -> ConfigManager:
    """Get singleton configuration manager"""
    if not hasattr(get_config, '_instance'):
        # Determine profile from environment
        profile = os.environ.get("SAGCO_PROFILE", "development")
        get_config._instance = ConfigManager()
        if profile in ConfigManager.PROFILES:
            get_config._instance.set_profile(profile)
    return get_config._instance
