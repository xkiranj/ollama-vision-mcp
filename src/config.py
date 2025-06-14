"""
Configuration management for Ollama Vision MCP Server
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class Config:
    """Configuration manager for the Ollama Vision MCP server"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config_file()
        self.config_data = self._load_config()
        
        # Set configuration values with defaults
        self.ollama_url = self._get_config("ollama_url", "http://localhost:11434")
        self.default_model = self._get_config("default_model", "llava-phi3")
        self.timeout = self._get_config("timeout", 120)  # 2 minutes default
        self.log_level = self._get_config("log_level", "INFO")
        self.cache_enabled = self._get_config("cache_enabled", False)
        self.cache_ttl = self._get_config("cache_ttl", 3600)  # 1 hour
        
        # Vision model preferences in order
        self.model_preferences = self._get_config("model_preferences", [
            "llava-phi3",
            "llava:7b",
            "llava:13b",
            "bakllava"
        ])
        
        # Apply log level
        logging.getLogger().setLevel(getattr(logging, self.log_level.upper()))
    
    def _find_config_file(self) -> Optional[str]:
        """Find configuration file in standard locations"""
        # Check environment variable first
        env_config = os.environ.get("OLLAMA_VISION_CONFIG")
        if env_config and Path(env_config).exists():
            return env_config
        
        # Check standard locations
        locations = [
            Path.cwd() / "ollama-vision-config.json",
            Path.home() / ".ollama-vision-mcp" / "config.json",
            Path(__file__).parent.parent / "config.json"
        ]
        
        for location in locations:
            if location.exists():
                logger.info(f"Found config file at: {location}")
                return str(location)
        
        return None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_path:
            return {}
            
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config from {self.config_path}: {e}")
            return {}
    
    def _get_config(self, key: str, default: Any) -> Any:
        """Get configuration value with fallback to environment variable and default"""
        # First check environment variable
        env_key = f"OLLAMA_VISION_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            # Convert string to appropriate type
            if isinstance(default, bool):
                return env_value.lower() in ('true', '1', 'yes')
            elif isinstance(default, int):
                try:
                    return int(env_value)
                except ValueError:
                    logger.warning(f"Invalid integer value for {env_key}: {env_value}")
                    return default
            elif isinstance(default, list):
                # Handle comma-separated list
                return [v.strip() for v in env_value.split(',')]
            else:
                return env_value
        
        # Then check config file
        if key in self.config_data:
            return self.config_data[key]
        
        # Finally use default
        return default
    
    def save_example_config(self, path: Optional[str] = None):
        """Save an example configuration file"""
        example_config = {
            "ollama_url": "http://localhost:11434",
            "default_model": "llava-phi3",
            "timeout": 120,
            "log_level": "INFO",
            "cache_enabled": False,
            "cache_ttl": 3600,
            "model_preferences": [
                "llava-phi3",
                "llava:7b",
                "llava:13b",
                "bakllava"
            ]
        }
        
        save_path = path or "ollama-vision-config.example.json"
        try:
            with open(save_path, 'w') as f:
                json.dump(example_config, f, indent=2)
            logger.info(f"Saved example config to: {save_path}")
        except Exception as e:
            logger.error(f"Failed to save example config: {e}")
