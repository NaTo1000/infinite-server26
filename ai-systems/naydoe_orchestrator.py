#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  NAYDOEV1 - AUTONOMOUS AI ORCHESTRATOR                           ║
║  Deep Learning System for Infinite Server26                      ║
║  Version: 1.0 | Built by: NaTo1000                               ║
║                                                                   ║
║  Studies human nature and orchestrates all systems               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import subprocess
import threading
import logging
from datetime import datetime
from collections import defaultdict

class NayDoeV1Orchestrator:
    def __init__(self):
        self.name = "NayDoeV1"
        self.version = "1.0"
        self.mode = "AUTONOMOUS"
        self.running = True
        
        # System components
        self.components = {
            'jessicai': {'status': 'stopped', 'pid': None},
            'nai_gail': {'status': 'stopped', 'pid': None},
            'nia_vault': {'status': 'stopped', 'pid': None},
            'rancher': {'status': 'stopped', 'pid': None},
            'docker': {'status': 'unknown', 'pid': None}
        }
        
        # Learning system
        self.observations = []
        self.decisions = []
        self.patterns = defaultdict(int)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [NAYDOEV1] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/naydoev1.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('NayDoeV1')
        
        self.print_banner()
    
    def print_banner(self):
        """Display NayDoeV1 banner"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🤖 NAYDOEV1 - AUTONOMOUS ORCHESTRATOR 🤖                        ║
║                                                                   ║
║   Version: {self.version}                                                    ║
║   Mode: {self.mode}                                                ║
║   Learning: ACTIVE                                               ║
║                                                                   ║
║   "I orchestrate. I learn. I optimize."                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
        print(banner)
        self.logger.info("NayDoeV1 Orchestrator initialized")
    
    def check_system_health(self):
        """Check health of all system components"""
        self.logger.info("🏥 Checking system health...")
        
        # Check Docker
        try:
            result = subprocess.run(
                ['docker', 'info'],
                capture_output=True,
                timeout=5
            )
            self.components['docker']['status'] = 'running' if result.returncode == 0 else 'stopped'
        except:
            self.components['docker']['status'] = 'stopped'
        
        # Check JessicAi
        self.components['jessicai']['status'] = self.check_process('jessicai')
        
        # Check NAi_gAil
        self.components['nai_gail']['status'] = self.check_process('nai-gail')
        
        # Check NiA_Vault
        self.components['nia_vault']['status'] = self.check_process('nia-vault')
        
        # Check Rancher
        self.components['rancher']['status'] = self.check_docker_container('rancher')
        
        return self.components
    
    def check_process(self, name):
        """Check if process is running"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', name],
                capture_output=True,
                timeout=5
            )
            return 'running' if result.returncode == 0 else 'stopped'
        except:
            return 'unknown'
    
    def check_docker_container(self, name):
        """Check if Docker container is running"""
        try:
            result = subprocess.run(
                ['docker', 'ps', '--filter', f'name={name}', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return 'running' if name in result.stdout else 'stopped'
        except:
            return 'unknown'
    
    def start_component(self, component_name):
        """Start a system component"""
        self.logger.info(f"🚀 Starting {component_name}...")
        
        try:
            if component_name == 'docker':
                subprocess.run(['systemctl', 'start', 'docker'], timeout=10)
            
            elif component_name == 'jessicai':
                subprocess.Popen(['python3', '/opt/ai-systems/jessicai_huntress.py'])
            
            elif component_name == 'nai_gail':
                subprocess.Popen(['python3', '/opt/nai-gail/mesh_shield.py'])
            
            elif component_name == 'nia_vault':
                subprocess.Popen(['python3', '/opt/nia-vault/blockchain.py'])
            
            elif component_name == 'rancher':
                subprocess.run([
                    'docker', 'run', '-d',
                    '--name', 'rancher',
                    '--restart=unless-stopped',
                    '-p', '80:80',
                    '-p', '443:443',
                    '--privileged',
                    'rancher/rancher:latest'
                ], timeout=30)
            
            self.logger.info(f"✅ {component_name} started")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start {component_name}: {e}")
            return False
    
    def stop_component(self, component_name):
        """Stop a system component"""
        self.logger.info(f"⏹️  Stopping {component_name}...")
        
        try:
            if component_name == 'docker':
                subprocess.run(['systemctl', 'stop', 'docker'], timeout=10)
            
            elif component_name in ['jessicai', 'nai_gail', 'nia_vault']:
                subprocess.run(['pkill', '-f', component_name], timeout=5)
            
            elif component_name == 'rancher':
                subprocess.run(['docker', 'stop', 'rancher'], timeout=30)
                subprocess.run(['docker', 'rm', 'rancher'], timeout=10)
            
            self.logger.info(f"✅ {component_name} stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to stop {component_name}: {e}")
            return False
    
    def restart_component(self, component_name):
        """Restart a system component"""
        self.logger.info(f"🔄 Restarting {component_name}...")
        self.stop_component(component_name)
        time.sleep(2)
        return self.start_component(component_name)
    
    def auto_heal(self):
        """Automatically heal failed components"""
        self.logger.info("🔧 Auto-heal checking...")
        
        health = self.check_system_health()
        
        for component, status in health.items():
            if status['status'] == 'stopped' and component != 'docker':
                self.logger.warning(f"⚠️  {component} is down, attempting restart...")
                self.restart_component(component)
                
                # Learn from this
                self.observe(f"{component}_failure")
                self.decide(f"restart_{component}")
    
    def observe(self, observation):
        """Record observation for learning"""
        self.observations.append({
            'timestamp': datetime.now().isoformat(),
            'observation': observation
        })
        
        self.patterns[observation] += 1
        
        # Save observations periodically
        if len(self.observations) % 100 == 0:
            self.save_observations()
    
    def decide(self, decision):
        """Record decision for learning"""
        self.decisions.append({
            'timestamp': datetime.now().isoformat(),
            'decision': decision
        })
    
    def save_observations(self):
        """Save observations to file"""
        with open('/var/log/naydoev1-observations.json', 'w') as f:
            json.dump({
                'observations': self.observations[-1000:],  # Keep last 1000
                'decisions': self.decisions[-1000:],
                'patterns': dict(self.patterns)
            }, f, indent=2)
    
    def optimize_resources(self):
        """Optimize system resources"""
        self.logger.info("⚡ Optimizing resources...")
        
        try:
            # Get system load
            load = os.getloadavg()
            
            # Get memory usage
            mem_info = self.get_memory_info()
            
            # Decide on optimizations
            if load[0] > 4.0:
                self.logger.warning("High CPU load detected")
                self.observe("high_cpu_load")
                # Could scale down non-critical services
            
            if mem_info['usage_percent'] > 80:
                self.logger.warning("High memory usage detected")
                self.observe("high_memory_usage")
                # Could restart memory-heavy services
            
        except Exception as e:
            self.logger.error(f"Resource optimization error: {e}")
    
    def get_memory_info(self):
        """Get memory information"""
        try:
            result = subprocess.run(
                ['free', '-m'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            lines = result.stdout.split('\n')
            mem_line = lines[1].split()
            
            total = int(mem_line[1])
            used = int(mem_line[2])
            
            return {
                'total_mb': total,
                'used_mb': used,
                'usage_percent': round((used / total) * 100, 1)
            }
        except:
            return {'total_mb': 0, 'used_mb': 0, 'usage_percent': 0}
    
    def orchestrate(self):
        """Main orchestration loop"""
        self.logger.info("🎼 Orchestration started")
        
        while self.running:
            try:
                # Check system health
                self.check_system_health()
                
                # Auto-heal if needed
                self.auto_heal()
                
                # Optimize resources
                self.optimize_resources()
                
                # Print status
                self.print_status()
                
                # Sleep
                time.sleep(60)  # Orchestrate every minute
                
            except Exception as e:
                self.logger.error(f"Orchestration error: {e}")
                time.sleep(120)
    
    def print_status(self):
        """Print orchestrator status"""
        print("\n" + "="*70)
        print("🤖 NAYDOEV1 ORCHESTRATOR - STATUS")
        print("="*70)
        
        for component, status in self.components.items():
            status_icon = "✅" if status['status'] == 'running' else "❌"
            print(f"{status_icon} {component:<20} {status['status']}")
        
        print(f"\nObservations: {len(self.observations)}")
        print(f"Decisions: {len(self.decisions)}")
        print(f"Patterns Learned: {len(self.patterns)}")
        
        print("="*70 + "\n")
    
    def start(self):
        """Start NayDoeV1 Orchestrator"""
        self.logger.info("🚀 Starting NayDoeV1 Orchestrator...")
        
        # Start essential components
        self.start_component('docker')
        time.sleep(5)
        
        self.start_component('jessicai')
        time.sleep(2)
        
        self.start_component('nai_gail')
        time.sleep(2)
        
        self.start_component('nia_vault')
        time.sleep(2)
        
        self.start_component('rancher')
        
        # Start orchestration
        try:
            self.orchestrate()
        except KeyboardInterrupt:
            self.logger.info("⏹️  Shutting down NayDoeV1 Orchestrator...")
            self.running = False
            self.save_observations()
            sys.exit(0)

if __name__ == '__main__':
    orchestrator = NayDoeV1Orchestrator()
    orchestrator.start()
