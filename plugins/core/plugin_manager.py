#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - PLUGIN MANAGER                              ║
║  Modular Plugin System for Extensions                            ║
║  Version: 1.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import importlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class Plugin:
    """Base plugin class"""
    def __init__(self):
        self.name = "BasePlugin"
        self.version = "1.0"
        self.author = "NaTo1000"
        self.enabled = True
        self.dependencies = []
    
    def initialize(self):
        """Initialize plugin"""
        pass
    
    def execute(self, *args, **kwargs):
        """Execute plugin main function"""
        pass
    
    def cleanup(self):
        """Cleanup on plugin unload"""
        pass
    
    def get_info(self):
        """Get plugin information"""
        return {
            'name': self.name,
            'version': self.version,
            'author': self.author,
            'enabled': self.enabled,
            'dependencies': self.dependencies
        }

class PluginManager:
    def __init__(self, plugin_dir='/opt/infinite-server26/plugins'):
        self.plugin_dir = Path(plugin_dir)
        self.plugins = {}
        self.loaded_plugins = {}
        self.plugin_config = {}
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [PluginManager] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/plugin-manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('PluginManager')
        
        # Create plugin directory
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("Plugin Manager initialized")
    
    def discover_plugins(self):
        """Discover available plugins"""
        self.logger.info("🔍 Discovering plugins...")
        
        plugin_count = 0
        for plugin_file in self.plugin_dir.rglob('*.py'):
            if plugin_file.name.startswith('_'):
                continue
            
            plugin_name = plugin_file.stem
            plugin_path = str(plugin_file.parent)
            
            if plugin_path not in sys.path:
                sys.path.insert(0, plugin_path)
            
            self.plugins[plugin_name] = {
                'file': str(plugin_file),
                'path': plugin_path,
                'loaded': False
            }
            plugin_count += 1
        
        self.logger.info(f"✅ Discovered {plugin_count} plugins")
        return self.plugins
    
    def load_plugin(self, plugin_name):
        """Load a specific plugin"""
        if plugin_name not in self.plugins:
            self.logger.error(f"❌ Plugin not found: {plugin_name}")
            return False
        
        try:
            self.logger.info(f"📦 Loading plugin: {plugin_name}")
            
            # Import plugin module
            module = importlib.import_module(plugin_name)
            
            # Find plugin class
            plugin_class = None
            for item_name in dir(module):
                item = getattr(module, item_name)
                if isinstance(item, type) and issubclass(item, Plugin) and item != Plugin:
                    plugin_class = item
                    break
            
            if not plugin_class:
                self.logger.error(f"❌ No plugin class found in {plugin_name}")
                return False
            
            # Instantiate plugin
            plugin_instance = plugin_class()
            
            # Check dependencies
            if not self._check_dependencies(plugin_instance):
                self.logger.error(f"❌ Missing dependencies for {plugin_name}")
                return False
            
            # Initialize plugin
            plugin_instance.initialize()
            
            # Store loaded plugin
            self.loaded_plugins[plugin_name] = plugin_instance
            self.plugins[plugin_name]['loaded'] = True
            
            self.logger.info(f"✅ Plugin loaded: {plugin_name} v{plugin_instance.version}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load plugin {plugin_name}: {e}")
            return False
    
    def unload_plugin(self, plugin_name):
        """Unload a plugin"""
        if plugin_name not in self.loaded_plugins:
            self.logger.warning(f"⚠️  Plugin not loaded: {plugin_name}")
            return False
        
        try:
            self.logger.info(f"📤 Unloading plugin: {plugin_name}")
            
            # Cleanup plugin
            plugin = self.loaded_plugins[plugin_name]
            plugin.cleanup()
            
            # Remove from loaded plugins
            del self.loaded_plugins[plugin_name]
            self.plugins[plugin_name]['loaded'] = False
            
            self.logger.info(f"✅ Plugin unloaded: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to unload plugin {plugin_name}: {e}")
            return False
    
    def reload_plugin(self, plugin_name):
        """Reload a plugin"""
        self.logger.info(f"🔄 Reloading plugin: {plugin_name}")
        self.unload_plugin(plugin_name)
        return self.load_plugin(plugin_name)
    
    def load_all_plugins(self):
        """Load all discovered plugins"""
        self.logger.info("📦 Loading all plugins...")
        
        loaded_count = 0
        for plugin_name in self.plugins.keys():
            if self.load_plugin(plugin_name):
                loaded_count += 1
        
        self.logger.info(f"✅ Loaded {loaded_count}/{len(self.plugins)} plugins")
        return loaded_count
    
    def execute_plugin(self, plugin_name, *args, **kwargs):
        """Execute a plugin"""
        if plugin_name not in self.loaded_plugins:
            self.logger.error(f"❌ Plugin not loaded: {plugin_name}")
            return None
        
        try:
            plugin = self.loaded_plugins[plugin_name]
            result = plugin.execute(*args, **kwargs)
            return result
        except Exception as e:
            self.logger.error(f"❌ Plugin execution failed {plugin_name}: {e}")
            return None
    
    def get_plugin_info(self, plugin_name):
        """Get plugin information"""
        if plugin_name not in self.loaded_plugins:
            return None
        
        plugin = self.loaded_plugins[plugin_name]
        return plugin.get_info()
    
    def list_plugins(self):
        """List all plugins"""
        return {
            'total': len(self.plugins),
            'loaded': len(self.loaded_plugins),
            'plugins': [
                {
                    'name': name,
                    'loaded': info['loaded'],
                    'file': info['file']
                }
                for name, info in self.plugins.items()
            ]
        }
    
    def _check_dependencies(self, plugin):
        """Check if plugin dependencies are met"""
        for dep in plugin.dependencies:
            if dep not in self.loaded_plugins:
                return False
        return True
    
    def save_config(self):
        """Save plugin configuration"""
        config_file = self.plugin_dir / 'plugin_config.json'
        
        config = {
            'plugins': {
                name: {
                    'enabled': plugin.enabled,
                    'version': plugin.version
                }
                for name, plugin in self.loaded_plugins.items()
            },
            'last_updated': datetime.now().isoformat()
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        self.logger.info(f"💾 Configuration saved to {config_file}")
    
    def load_config(self):
        """Load plugin configuration"""
        config_file = self.plugin_dir / 'plugin_config.json'
        
        if not config_file.exists():
            return {}
        
        with open(config_file, 'r') as f:
            self.plugin_config = json.load(f)
        
        self.logger.info(f"📂 Configuration loaded from {config_file}")
        return self.plugin_config

if __name__ == '__main__':
    manager = PluginManager()
    manager.discover_plugins()
    manager.load_all_plugins()
    
    print("\n" + "="*70)
    print("🔌 PLUGIN MANAGER - STATUS")
    print("="*70)
    
    plugin_list = manager.list_plugins()
    print(f"Total Plugins: {plugin_list['total']}")
    print(f"Loaded Plugins: {plugin_list['loaded']}")
    print("\nPlugins:")
    for plugin in plugin_list['plugins']:
        status = "✅ LOADED" if plugin['loaded'] else "⭕ NOT LOADED"
        print(f"  {status} - {plugin['name']}")
    
    print("="*70 + "\n")
