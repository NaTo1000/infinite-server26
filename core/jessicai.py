#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  JESSICAI - THE HUNTRESS                                         ║
║  No Mercy Security AI (Rewritten)                                ║
║  Version: 26.2 | Built by: NaTo1000                              ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import sys
import time
import subprocess
import threading
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.utils import ComponentBase, DataStore, print_banner


class JessicAiHuntress(ComponentBase):
    """No Mercy Security AI for threat detection and elimination"""
    
    def __init__(self):
        super().__init__("JessicAi", "26.2")
        
        # Security configuration
        self.security_level = self.config.get('ai.jessicai.security_level', 'MAXIMUM')
        self.mercy_mode = self.config.get('ai.jessicai.mercy_mode', False)
        self.monitoring_interval = self.config.get('ai.jessicai.monitoring_interval', 5)
        self.threat_threshold = self.config.get('ai.jessicai.threat_threshold', 10)
        
        # Threat tracking
        self.threats_detected = 0
        self.threats_blocked = 0
        self.banned_ips: Set[str] = set()
        self.suspicious_activity = defaultdict(int)
        
        # Data store
        self.data_store = DataStore(self.paths.get_path('data') / 'jessicai_threats.json')
        
        # Load banned IPs from storage
        self.banned_ips = set(self.data_store.get('banned_ips', []))
        
        print_banner("JESSICAI - THE HUNTRESS")
        self.logger.info(f"Security Level: {self.security_level}")
        self.logger.info(f"Mercy Mode: {'ENABLED' if self.mercy_mode else 'DISABLED'}")
    
    def monitor_network(self):
        """Monitor network connections for threats"""
        self.logger.info("🔍 Network monitoring started")
        
        while self.running:
            try:
                connections = self._get_connections()
                
                for conn in connections:
                    if self._is_threat(conn):
                        self._handle_threat(conn)
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.handle_error(e)
                time.sleep(10)
    
    def _get_connections(self) -> List[Dict[str, str]]:
        """Get active network connections"""
        try:
            result = subprocess.run(
                ['ss', '-tunaH'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            connections = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5:
                        remote = parts[4].split(':')
                        if len(remote) == 2:
                            connections.append({
                                'ip': remote[0],
                                'port': remote[1]
                            })
            
            return connections
        except Exception as e:
            self.logger.error(f"Error getting connections: {e}")
            return []
    
    def _is_threat(self, connection: Dict[str, str]) -> bool:
        """Determine if connection is a threat"""
        ip = connection.get('ip', '')
        port = connection.get('port', '')
        
        # Check banned IPs
        if ip in self.banned_ips:
            return True
        
        # Check suspicious activity
        if self.suspicious_activity[ip] > self.threat_threshold:
            return True
        
        # Check malicious ports (configurable)
        malicious_ports = self.config.get('security.malicious_ports', 
                                         ['4444', '5555', '6666', '31337', '12345'])
        if port in malicious_ports:
            self.suspicious_activity[ip] += 1
            return True
        
        return False
    
    def _handle_threat(self, connection: Dict[str, str]):
        """Handle detected threat"""
        ip = connection.get('ip', '')
        port = connection.get('port', '')
        
        self.threats_detected += 1
        self.logger.warning(f"⚠️  THREAT DETECTED: {ip}:{port}")
        
        # Log threat
        threats = self.data_store.get('threats', [])
        threats.append({
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'port': port,
            'action': 'detected'
        })
        self.data_store.set('threats', threats[-1000:])  # Keep last 1000
        
        # Block if not in mercy mode
        if not self.mercy_mode:
            self._block_ip(ip)
    
    def _block_ip(self, ip: str):
        """Block IP address"""
        try:
            # In production, use iptables or firewall commands
            # For now, just track it
            self.banned_ips.add(ip)
            self.threats_blocked += 1
            
            # Save banned IPs
            self.data_store.set('banned_ips', list(self.banned_ips))
            
            self.logger.info(f"🛡️  BLOCKED: {ip}")
            
        except Exception as e:
            self.logger.error(f"Error blocking IP {ip}: {e}")
    
    def monitor_files(self):
        """Monitor critical files for unauthorized changes"""
        self.logger.info("📁 File monitoring started")
        
        critical_files = [
            Path('./config.yaml'),
            Path('./requirements.txt')
        ]
        
        # Store file hashes
        file_hashes = {}
        for file_path in critical_files:
            if file_path.exists():
                file_hashes[str(file_path)] = self._hash_file(file_path)
        
        while self.running:
            try:
                for file_path in critical_files:
                    if file_path.exists():
                        current_hash = self._hash_file(file_path)
                        stored_hash = file_hashes.get(str(file_path))
                        
                        if stored_hash and current_hash != stored_hash:
                            self.logger.critical(f"🚨 UNAUTHORIZED CHANGE: {file_path}")
                        
                        file_hashes[str(file_path)] = current_hash
                
                time.sleep(30)
                
            except Exception as e:
                self.handle_error(e)
                time.sleep(60)
    
    def _hash_file(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""
    
    def get_status(self) -> Dict[str, Any]:
        """Get huntress status"""
        status = super().get_status()
        status.update({
            'security_level': self.security_level,
            'mercy_mode': self.mercy_mode,
            'threats_detected': self.threats_detected,
            'threats_blocked': self.threats_blocked,
            'banned_ips_count': len(self.banned_ips)
        })
        return status
    
    def print_status(self):
        """Print status report"""
        print("\n" + "="*70)
        print("⚔️  JESSICAI HUNTRESS - STATUS REPORT")
        print("="*70)
        print(f"Security Level: {self.security_level}")
        print(f"Mercy Mode: {'ENABLED' if self.mercy_mode else 'DISABLED'}")
        print(f"\nThreats Detected: {self.threats_detected}")
        print(f"Threats Blocked: {self.threats_blocked}")
        print(f"Banned IPs: {len(self.banned_ips)}")
        print("="*70 + "\n")
    
    def run(self):
        """Start JessicAi Huntress"""
        self.start()
        
        # Start monitoring threads
        threads = [
            threading.Thread(target=self.monitor_network, daemon=True),
            threading.Thread(target=self.monitor_files, daemon=True)
        ]
        
        for thread in threads:
            thread.start()
        
        self.logger.info("✅ All monitoring systems active")
        
        try:
            while self.running:
                time.sleep(300)  # Print status every 5 minutes
                self.print_status()
                
        except KeyboardInterrupt:
            self.logger.info("⏹️  Shutting down JessicAi Huntress...")
        except Exception as e:
            self.handle_error(e)
        finally:
            self.stop()


if __name__ == '__main__':
    huntress = JessicAiHuntress()
    huntress.run()
