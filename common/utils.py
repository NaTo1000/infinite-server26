#!/usr/bin/env python3

"""
Infinite Server26 - Common Utilities
Version: 26.2 | Built by: NaTo1000

Shared utilities for all components.
"""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Use try/except for optional yaml dependency
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ConfigLoader:
    """Load and manage configuration"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            return self._default_config()
        
        try:
            if YAML_AVAILABLE:
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                # Fallback to JSON if YAML not available
                with open(self.config_path.replace('.yaml', '.json'), 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'server': {'name': 'Infinite Server26', 'version': '26.2'},
            'logging': {'level': 'INFO', 'dir': './logs'},
            'paths': {'data': './data', 'logs': './logs', 'storage': './storage'}
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value


class Logger:
    """Centralized logging utility"""
    
    @staticmethod
    def setup(name: str, config: Optional[ConfigLoader] = None) -> logging.Logger:
        """Setup logger with configuration"""
        if config is None:
            config = ConfigLoader()
        
        log_level = config.get('logging.level', 'INFO')
        log_dir = Path(config.get('logging.dir', './logs'))
        log_format = config.get('logging.format', 
                                '%(asctime)s [%(name)s] %(levelname)s: %(message)s')
        
        # Create log directory
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level))
        
        # Remove existing handlers
        logger.handlers = []
        
        # File handler
        file_handler = logging.FileHandler(log_dir / f"{name.lower()}.log")
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(console_handler)
        
        return logger


class PathManager:
    """Manage paths and directories"""
    
    def __init__(self, config: Optional[ConfigLoader] = None):
        if config is None:
            config = ConfigLoader()
        self.config = config
        self.root = Path(__file__).parent.parent
    
    def get_path(self, key: str, create: bool = True) -> Path:
        """Get path from configuration"""
        path_str = self.config.get(f'paths.{key}', f'./{key}')
        path = self.root / path_str
        
        if create:
            path.mkdir(parents=True, exist_ok=True)
        
        return path
    
    def ensure_directory(self, path: Path) -> bool:
        """Ensure directory exists"""
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory {path}: {e}")
            return False


class ComponentBase:
    """Base class for all system components"""
    
    def __init__(self, name: str, version: str = "26.2"):
        self.name = name
        self.version = version
        self.running = False
        
        # Load configuration
        self.config = ConfigLoader()
        
        # Setup logging
        self.logger = Logger.setup(name, self.config)
        
        # Setup paths
        self.paths = PathManager(self.config)
        
        # Component status
        self.status = {
            'name': self.name,
            'version': self.version,
            'state': 'stopped',
            'started_at': None,
            'errors': []
        }
        
        self.logger.info(f"{self.name} v{self.version} initialized")
    
    def start(self):
        """Start the component"""
        self.running = True
        self.status['state'] = 'running'
        self.status['started_at'] = datetime.now().isoformat()
        self.logger.info(f"{self.name} started")
    
    def stop(self):
        """Stop the component"""
        self.running = False
        self.status['state'] = 'stopped'
        self.logger.info(f"{self.name} stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get component status"""
        return self.status.copy()
    
    def handle_error(self, error: Exception):
        """Handle component error"""
        error_msg = f"{type(error).__name__}: {str(error)}"
        self.status['errors'].append({
            'timestamp': datetime.now().isoformat(),
            'error': error_msg
        })
        self.logger.error(f"Error in {self.name}: {error_msg}")


class DataStore:
    """Simple JSON-based data store"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load data from file"""
        if not self.file_path.exists():
            return {}
        
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def save(self):
        """Save data to file"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key"""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set value by key"""
        self.data[key] = value
        self.save()
    
    def delete(self, key: str):
        """Delete key"""
        if key in self.data:
            del self.data[key]
            self.save()


def print_banner(title: str, version: str = "26.2"):
    """Print formatted banner"""
    width = 70
    border = "═" * (width - 2)
    
    banner = f"""
╔{border}╗
║{title.center(width - 2)}║
║{f"Version {version}".center(width - 2)}║
║{"Built by: NaTo1000".center(width - 2)}║
╚{border}╝
"""
    print(banner)


if __name__ == '__main__':
    # Test utilities
    print_banner("Infinite Server26 - Common Utilities")
    
    config = ConfigLoader()
    print(f"Config loaded: {config.get('server.name')}")
    
    logger = Logger.setup("test")
    logger.info("Logger test successful")
    
    paths = PathManager()
    log_path = paths.get_path('logs')
    print(f"Logs path: {log_path}")
