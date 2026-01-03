#!/usr/bin/env python3

"""
Test suite for common utilities
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.utils import ConfigLoader, Logger, PathManager, ComponentBase, DataStore


class TestConfigLoader(unittest.TestCase):
    """Test ConfigLoader class"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = ConfigLoader('nonexistent.yaml')
        self.assertIsNotNone(config.config)
        self.assertEqual(config.get('server.name'), 'Infinite Server26')
    
    def test_get_with_default(self):
        """Test getting value with default"""
        config = ConfigLoader('nonexistent.yaml')
        value = config.get('nonexistent.key', 'default_value')
        self.assertEqual(value, 'default_value')


class TestPathManager(unittest.TestCase):
    """Test PathManager class"""
    
    def test_path_creation(self):
        """Test path creation"""
        pm = PathManager()
        path = pm.get_path('logs')
        self.assertTrue(path.exists())
        self.assertTrue(path.is_dir())


class TestComponentBase(unittest.TestCase):
    """Test ComponentBase class"""
    
    def test_component_initialization(self):
        """Test component initialization"""
        component = ComponentBase("TestComponent")
        self.assertEqual(component.name, "TestComponent")
        self.assertEqual(component.version, "26.2")
        self.assertFalse(component.running)
    
    def test_component_start_stop(self):
        """Test component start and stop"""
        component = ComponentBase("TestComponent")
        component.start()
        self.assertTrue(component.running)
        self.assertEqual(component.status['state'], 'running')
        
        component.stop()
        self.assertFalse(component.running)
        self.assertEqual(component.status['state'], 'stopped')


class TestDataStore(unittest.TestCase):
    """Test DataStore class"""
    
    def setUp(self):
        """Setup test data store"""
        self.test_file = Path('./test_datastore.json')
        self.store = DataStore(self.test_file)
    
    def tearDown(self):
        """Cleanup test file"""
        if self.test_file.exists():
            self.test_file.unlink()
    
    def test_set_and_get(self):
        """Test setting and getting values"""
        self.store.set('test_key', 'test_value')
        value = self.store.get('test_key')
        self.assertEqual(value, 'test_value')
    
    def test_delete(self):
        """Test deleting values"""
        self.store.set('test_key', 'test_value')
        self.store.delete('test_key')
        value = self.store.get('test_key')
        self.assertIsNone(value)


if __name__ == '__main__':
    unittest.main()
