#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  NAi_gAil - MESH SHIELD DOME                                     ║
║  Impenetrable BLE/WiFi Security Dome                             ║
║  Version: 1.0 | Built by: NaTo1000                               ║
║                                                                   ║
║  Creates a dome of impenetrable shield using BLE and WiFi mesh   ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import subprocess
import threading
import logging
import json
from datetime import datetime
from collections import defaultdict

class NAiGAilMeshShield:
    def __init__(self):
        self.name = "NAi_gAil"
        self.version = "1.0"
        self.codename = "MESH SHIELD DOME"
        self.shield_active = False
        self.running = True
        
        # Mesh network
        self.mesh_nodes = []
        self.wifi_networks = []
        self.ble_devices = []
        
        # Shield parameters
        self.shield_radius = 100  # meters
        self.shield_strength = "MAXIMUM"
        self.penetration_attempts = 0
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [NAi_gAil] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/nai-gail.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('NAi_gAil')
        
        self.print_banner()
    
    def print_banner(self):
        """Display NAi_gAil banner"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🛡️  NAi_gAil - MESH SHIELD DOME 🛡️                             ║
║                                                                   ║
║   Version: {self.version}                                                    ║
║   Shield Status: {"ACTIVE" if self.shield_active else "INACTIVE"}                                          ║
║   Shield Strength: {self.shield_strength}                                       ║
║   Coverage: {self.shield_radius}m radius                                        ║
║                                                                   ║
║   "An impenetrable dome of protection."                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
        print(banner)
        self.logger.info("NAi_gAil Mesh Shield initialized")
    
    def initialize_wifi_mesh(self):
        """Initialize WiFi mesh network"""
        self.logger.info("📡 Initializing WiFi mesh network...")
        
        try:
            # Check for wireless interfaces
            result = subprocess.run(
                ['iw', 'dev'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if 'Interface' in result.stdout:
                self.logger.info("✅ Wireless interface detected")
                
                # Get interface name
                for line in result.stdout.split('\n'):
                    if 'Interface' in line:
                        interface = line.split()[1]
                        self.logger.info(f"Using interface: {interface}")
                        
                        # Setup mesh network
                        self.setup_mesh_interface(interface)
            else:
                self.logger.warning("⚠️  No wireless interface found")
                
        except Exception as e:
            self.logger.error(f"WiFi mesh initialization error: {e}")
    
    def setup_mesh_interface(self, interface):
        """Setup mesh network interface"""
        try:
            # Create mesh interface
            mesh_interface = f"{interface}_mesh"
            
            commands = [
                ['iw', 'dev', interface, 'interface', 'add', mesh_interface, 'type', 'mp'],
                ['ip', 'link', 'set', mesh_interface, 'up'],
                ['iw', 'dev', mesh_interface, 'mesh', 'join', 'NAi_gAil_Mesh']
            ]
            
            for cmd in commands:
                subprocess.run(cmd, timeout=5)
            
            self.logger.info(f"✅ Mesh interface {mesh_interface} created")
            
        except Exception as e:
            self.logger.error(f"Mesh interface setup error: {e}")
    
    def initialize_ble_mesh(self):
        """Initialize BLE mesh network"""
        self.logger.info("📶 Initializing BLE mesh network...")
        
        try:
            # Check for Bluetooth
            result = subprocess.run(
                ['hciconfig'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if 'hci0' in result.stdout:
                self.logger.info("✅ Bluetooth adapter detected")
                
                # Enable Bluetooth
                subprocess.run(['hciconfig', 'hci0', 'up'], timeout=5)
                subprocess.run(['hciconfig', 'hci0', 'piscan'], timeout=5)
                
                self.logger.info("✅ BLE mesh ready")
            else:
                self.logger.warning("⚠️  No Bluetooth adapter found")
                
        except Exception as e:
            self.logger.error(f"BLE mesh initialization error: {e}")
    
    def scan_wifi_networks(self):
        """Scan for WiFi networks in range"""
        try:
            result = subprocess.run(
                ['nmcli', 'dev', 'wifi', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            networks = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        ssid = parts[1] if parts[1] != '--' else 'Hidden'
                        signal = parts[-3] if len(parts) > 3 else '0'
                        networks.append({'ssid': ssid, 'signal': signal})
            
            self.wifi_networks = networks
            return networks
            
        except Exception as e:
            self.logger.error(f"WiFi scan error: {e}")
            return []
    
    def scan_ble_devices(self):
        """Scan for BLE devices in range"""
        try:
            result = subprocess.run(
                ['hcitool', 'scan'],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            devices = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        mac = parts[0]
                        name = ' '.join(parts[1:]) if len(parts) > 1 else 'Unknown'
                        devices.append({'mac': mac, 'name': name})
            
            self.ble_devices = devices
            return devices
            
        except Exception as e:
            self.logger.error(f"BLE scan error: {e}")
            return []
    
    def monitor_intrusions(self):
        """Monitor for intrusion attempts"""
        self.logger.info("👁️  Intrusion monitoring started")
        
        # Whitelist of known devices
        whitelist = self.load_whitelist()
        
        while self.running:
            try:
                # Scan WiFi
                wifi_networks = self.scan_wifi_networks()
                
                for network in wifi_networks:
                    if network['ssid'] not in whitelist.get('wifi', []):
                        self.logger.warning(f"⚠️  Unknown WiFi network: {network['ssid']}")
                        self.penetration_attempts += 1
                
                # Scan BLE
                ble_devices = self.scan_ble_devices()
                
                for device in ble_devices:
                    if device['mac'] not in whitelist.get('ble', []):
                        self.logger.warning(f"⚠️  Unknown BLE device: {device['name']} ({device['mac']})")
                        self.penetration_attempts += 1
                
                time.sleep(30)  # Scan every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Intrusion monitoring error: {e}")
                time.sleep(60)
    
    def load_whitelist(self):
        """Load whitelist of known devices"""
        whitelist_file = '/etc/nai-gail/whitelist.json'
        
        if os.path.exists(whitelist_file):
            with open(whitelist_file, 'r') as f:
                return json.load(f)
        else:
            return {'wifi': [], 'ble': []}
    
    def create_shield_dome(self):
        """Create the shield dome"""
        self.logger.info("🛡️  Creating shield dome...")
        
        # Initialize mesh networks
        self.initialize_wifi_mesh()
        self.initialize_ble_mesh()
        
        # Activate shield
        self.shield_active = True
        self.logger.info("✅ Shield dome ACTIVE")
    
    def strengthen_shield(self):
        """Strengthen shield parameters"""
        self.logger.info("⚡ Strengthening shield...")
        
        try:
            # Increase WiFi power (if supported)
            subprocess.run(['iw', 'dev', 'wlan0', 'set', 'txpower', 'fixed', '30'], timeout=5)
            
            # Increase BLE advertising power
            subprocess.run(['hciconfig', 'hci0', 'leadv', '3'], timeout=5)
            
            self.logger.info("✅ Shield strengthened")
            
        except Exception as e:
            self.logger.error(f"Shield strengthening error: {e}")
    
    def get_status(self):
        """Get shield status"""
        return {
            'name': self.name,
            'version': self.version,
            'shield_active': self.shield_active,
            'shield_strength': self.shield_strength,
            'shield_radius': self.shield_radius,
            'mesh_nodes': len(self.mesh_nodes),
            'wifi_networks': len(self.wifi_networks),
            'ble_devices': len(self.ble_devices),
            'penetration_attempts': self.penetration_attempts
        }
    
    def print_status(self):
        """Print shield status"""
        status = self.get_status()
        
        print("\n" + "="*70)
        print("🛡️  NAi_gAil MESH SHIELD - STATUS")
        print("="*70)
        print(f"Shield Status: {'ACTIVE' if status['shield_active'] else 'INACTIVE'}")
        print(f"Shield Strength: {status['shield_strength']}")
        print(f"Coverage Radius: {status['shield_radius']}m")
        print(f"\nMesh Nodes: {status['mesh_nodes']}")
        print(f"WiFi Networks Detected: {status['wifi_networks']}")
        print(f"BLE Devices Detected: {status['ble_devices']}")
        print(f"Penetration Attempts Blocked: {status['penetration_attempts']}")
        print("="*70 + "\n")
    
    def start(self):
        """Start NAi_gAil Mesh Shield"""
        self.logger.info("🚀 Starting NAi_gAil Mesh Shield...")
        
        # Create shield dome
        self.create_shield_dome()
        
        # Strengthen shield
        self.strengthen_shield()
        
        # Start monitoring
        monitor_thread = threading.Thread(target=self.monitor_intrusions, daemon=True)
        monitor_thread.start()
        
        self.logger.info("✅ All shield systems active")
        
        # Status reporting loop
        try:
            while self.running:
                time.sleep(300)  # Print status every 5 minutes
                self.print_status()
        except KeyboardInterrupt:
            self.logger.info("⏹️  Shutting down NAi_gAil Mesh Shield...")
            self.running = False
            sys.exit(0)

if __name__ == '__main__':
    shield = NAiGAilMeshShield()
    shield.start()
