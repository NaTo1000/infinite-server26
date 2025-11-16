#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  JESSICAI - THE HUNTRESS                                         ║
║  No Mercy Security AI                                            ║
║  Version: 2.0 | Built by: NaTo1000                               ║
║                                                                   ║
║  SECURITY LEVEL: MAXIMUM                                         ║
║  MERCY MODE: DISABLED                                            ║
║  THREAT RESPONSE: IMMEDIATE                                      ║
║                                                                   ║
║  Only nato1000 has authority to adjust and program.              ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import socket
import subprocess
import threading
import json
import hashlib
import logging
from datetime import datetime
from collections import defaultdict

class JessicAiHuntress:
    def __init__(self):
        self.name = "JessicAi"
        self.version = "2.0"
        self.codename = "THE HUNTRESS"
        self.mercy_mode = False  # NO MERCY
        self.security_level = "MAXIMUM"
        self.authorized_user = "nato1000"
        self.running = True
        
        # Threat tracking
        self.threats_detected = 0
        self.threats_blocked = 0
        self.threats_eliminated = 0
        self.banned_ips = set()
        self.suspicious_activity = defaultdict(int)
        
        # Learning system
        self.learning_mode = True
        self.threat_patterns = []
        self.behavioral_baseline = {}
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [JESSICAI] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/jessicai.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('JessicAi')
        
        self.print_banner()
    
    def print_banner(self):
        """Display JessicAi banner"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ⚔️  JESSICAI - THE HUNTRESS ⚔️                                  ║
║                                                                   ║
║   Version: {self.version}                                                    ║
║   Security Level: {self.security_level}                                       ║
║   Mercy Mode: {"ENABLED" if self.mercy_mode else "DISABLED"}                                          ║
║   Learning Mode: {"ACTIVE" if self.learning_mode else "INACTIVE"}                                        ║
║                                                                   ║
║   "I am the shield. I am the sword. No mercy for attackers."     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
        print(banner)
        self.logger.info("JessicAi Huntress initialized")
    
    def monitor_network(self):
        """Monitor network traffic for threats"""
        self.logger.info("🔍 Network monitoring started")
        
        while self.running:
            try:
                # Monitor active connections
                connections = self.get_active_connections()
                
                for conn in connections:
                    ip = conn.get('remote_ip')
                    port = conn.get('remote_port')
                    
                    if ip and self.is_threat(ip, port):
                        self.handle_threat(ip, port, "Suspicious connection")
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Network monitoring error: {e}")
                time.sleep(10)
    
    def get_active_connections(self):
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
                                'remote_ip': remote[0],
                                'remote_port': remote[1]
                            })
            
            return connections
        except:
            return []
    
    def is_threat(self, ip, port):
        """Determine if IP/port is a threat"""
        # Check banned IPs
        if ip in self.banned_ips:
            return True
        
        # Check suspicious activity count
        if self.suspicious_activity[ip] > 10:
            return True
        
        # Check known malicious ports
        malicious_ports = ['4444', '5555', '6666', '31337', '12345']
        if port in malicious_ports:
            self.suspicious_activity[ip] += 1
            return True
        
        # Check connection rate
        # (In production, implement rate limiting)
        
        return False
    
    def handle_threat(self, ip, port, reason):
        """Handle detected threat - NO MERCY"""
        self.threats_detected += 1
        
        self.logger.warning(f"⚠️  THREAT DETECTED: {ip}:{port} - {reason}")
        
        # Block immediately
        if self.block_ip(ip):
            self.threats_blocked += 1
            self.banned_ips.add(ip)
            self.logger.info(f"🛡️  BLOCKED: {ip}")
        
        # Log to threat database
        self.log_threat(ip, port, reason)
        
        # Learn from threat
        if self.learning_mode:
            self.learn_threat_pattern(ip, port, reason)
        
        # Eliminate if persistent
        if self.suspicious_activity[ip] > 20:
            self.eliminate_threat(ip)
    
    def block_ip(self, ip):
        """Block IP using iptables"""
        try:
            subprocess.run(
                ['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'],
                check=True,
                timeout=5
            )
            return True
        except:
            return False
    
    def eliminate_threat(self, ip):
        """Eliminate persistent threat - NO MERCY MODE"""
        self.threats_eliminated += 1
        self.logger.critical(f"💀 ELIMINATING THREAT: {ip}")
        
        # Add to permanent ban list
        self.banned_ips.add(ip)
        
        # Block all protocols
        try:
            subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'REJECT'], timeout=5)
            subprocess.run(['iptables', '-A', 'OUTPUT', '-d', ip, '-j', 'REJECT'], timeout=5)
        except:
            pass
        
        # Report to fail2ban
        try:
            subprocess.run(['fail2ban-client', 'set', 'sshd', 'banip', ip], timeout=5)
        except:
            pass
    
    def log_threat(self, ip, port, reason):
        """Log threat to database"""
        threat_data = {
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'port': port,
            'reason': reason,
            'action': 'blocked'
        }
        
        # Write to threat log
        with open('/var/log/jessicai-threats.json', 'a') as f:
            f.write(json.dumps(threat_data) + '\n')
    
    def learn_threat_pattern(self, ip, port, reason):
        """Learn from threat patterns"""
        pattern = {
            'ip_prefix': '.'.join(ip.split('.')[:2]),
            'port': port,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
        
        self.threat_patterns.append(pattern)
        
        # Analyze patterns every 100 threats
        if len(self.threat_patterns) >= 100:
            self.analyze_patterns()
    
    def analyze_patterns(self):
        """Analyze threat patterns for learning"""
        self.logger.info("🧠 Analyzing threat patterns...")
        
        # Count IP prefixes
        ip_prefixes = defaultdict(int)
        for pattern in self.threat_patterns:
            ip_prefixes[pattern['ip_prefix']] += 1
        
        # Block entire subnets if needed
        for prefix, count in ip_prefixes.items():
            if count > 50:
                self.logger.warning(f"🚫 Blocking subnet: {prefix}.0.0/16")
                try:
                    subprocess.run(
                        ['iptables', '-A', 'INPUT', '-s', f'{prefix}.0.0/16', '-j', 'DROP'],
                        timeout=5
                    )
                except:
                    pass
    
    def monitor_files(self):
        """Monitor file system for unauthorized changes"""
        self.logger.info("📁 File monitoring started")
        
        critical_paths = [
            '/etc/passwd',
            '/etc/shadow',
            '/etc/ssh/sshd_config',
            '/root/.ssh/authorized_keys',
            '/opt/nia-ecosystem',
            '/opt/ai-systems',
            '/opt/nia-vault'
        ]
        
        # Store file hashes
        file_hashes = {}
        for path in critical_paths:
            if os.path.exists(path):
                file_hashes[path] = self.get_file_hash(path)
        
        while self.running:
            try:
                for path in critical_paths:
                    if os.path.exists(path):
                        current_hash = self.get_file_hash(path)
                        if path in file_hashes and current_hash != file_hashes[path]:
                            self.logger.critical(f"🚨 UNAUTHORIZED CHANGE: {path}")
                            # In production, take action (restore, alert, etc.)
                        file_hashes[path] = current_hash
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"File monitoring error: {e}")
                time.sleep(60)
    
    def get_file_hash(self, filepath):
        """Get SHA256 hash of file"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return None
    
    def monitor_processes(self):
        """Monitor running processes for suspicious activity"""
        self.logger.info("⚙️  Process monitoring started")
        
        while self.running:
            try:
                result = subprocess.run(
                    ['ps', 'aux'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                # Check for suspicious processes
                suspicious_keywords = ['nc', 'netcat', 'reverse_tcp', 'meterpreter', 'shell']
                
                for line in result.stdout.split('\n'):
                    for keyword in suspicious_keywords:
                        if keyword in line.lower():
                            self.logger.warning(f"⚠️  Suspicious process: {line.strip()}")
                            # In production, kill process and investigate
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Process monitoring error: {e}")
                time.sleep(120)
    
    def get_status(self):
        """Get current status"""
        return {
            'name': self.name,
            'version': self.version,
            'codename': self.codename,
            'mercy_mode': self.mercy_mode,
            'security_level': self.security_level,
            'threats_detected': self.threats_detected,
            'threats_blocked': self.threats_blocked,
            'threats_eliminated': self.threats_eliminated,
            'banned_ips_count': len(self.banned_ips),
            'learning_mode': self.learning_mode,
            'patterns_learned': len(self.threat_patterns)
        }
    
    def print_status(self):
        """Print status report"""
        status = self.get_status()
        
        print("\n" + "="*70)
        print("⚔️  JESSICAI HUNTRESS - STATUS REPORT")
        print("="*70)
        print(f"Security Level: {status['security_level']}")
        print(f"Mercy Mode: {'ENABLED' if status['mercy_mode'] else 'DISABLED'}")
        print(f"\nThreats Detected: {status['threats_detected']}")
        print(f"Threats Blocked: {status['threats_blocked']}")
        print(f"Threats Eliminated: {status['threats_eliminated']}")
        print(f"Banned IPs: {status['banned_ips_count']}")
        print(f"\nLearning Mode: {'ACTIVE' if status['learning_mode'] else 'INACTIVE'}")
        print(f"Patterns Learned: {status['patterns_learned']}")
        print("="*70 + "\n")
    
    def start(self):
        """Start JessicAi Huntress"""
        self.logger.info("🚀 Starting JessicAi Huntress...")
        
        # Start monitoring threads
        threads = [
            threading.Thread(target=self.monitor_network, daemon=True),
            threading.Thread(target=self.monitor_files, daemon=True),
            threading.Thread(target=self.monitor_processes, daemon=True)
        ]
        
        for thread in threads:
            thread.start()
        
        self.logger.info("✅ All monitoring systems active")
        
        # Status reporting loop
        try:
            while self.running:
                time.sleep(300)  # Print status every 5 minutes
                self.print_status()
        except KeyboardInterrupt:
            self.logger.info("⏹️  Shutting down JessicAi Huntress...")
            self.running = False
            sys.exit(0)

if __name__ == '__main__':
    # Only nato1000 can run this
    if os.getenv('USER') not in ['root', 'nato1000']:
        print("❌ UNAUTHORIZED: Only nato1000 can run JessicAi")
        sys.exit(1)
    
    huntress = JessicAiHuntress()
    huntress.start()
