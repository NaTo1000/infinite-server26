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
        
        # Component status – 'proc' stores a Popen handle for managed processes
        self.components = {
            'jessicai': {'status': 'stopped', 'proc': None},
            'nai_gail': {'status': 'stopped', 'proc': None},
            'nia_vault': {'status': 'stopped', 'proc': None},
            'rancher':   {'status': 'stopped', 'proc': None},
            'docker':    {'status': 'unknown', 'proc': None},
        }

        # Learning system
        self.observations = []
        self.decisions = []
        self.patterns = defaultdict(int)

        # Setup logger without calling basicConfig (may conflict with other modules)
        self.logger = logging.getLogger('NayDoeV1')
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            fmt = logging.Formatter('%(asctime)s [NAYDOEV1] %(levelname)s: %(message)s')
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)
            self.logger.addHandler(sh)
            try:
                fh = logging.FileHandler('/var/log/naydoev1.log')
                fh.setFormatter(fmt)
                self.logger.addHandler(fh)
            except OSError:
                pass
        
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
        """Check health of all system components."""
        self.logger.info("🏥 Checking system health...")

        # Docker
        try:
            result = subprocess.run(
                ['docker', 'info'],
                capture_output=True,
                timeout=5,
            )
            self.components['docker']['status'] = 'running' if result.returncode == 0 else 'stopped'
        except Exception as e:
            self.logger.debug(f"docker info check failed: {e}")
            self.components['docker']['status'] = 'stopped'

        # Process-managed components: check stored proc first, fall back to pgrep
        _PROC_SEARCH = {
            'jessicai': 'jessicai_huntress',
            'nai_gail':  'mesh_shield',
            'nia_vault': 'nia-vault',
        }
        for name, search_term in _PROC_SEARCH.items():
            proc = self.components[name].get('proc')
            if proc is not None and proc.poll() is None:
                self.components[name]['status'] = 'running'
            else:
                self.components[name]['status'] = self.check_process(search_term)

        # Rancher via Docker
        self.components['rancher']['status'] = self.check_docker_container('rancher')

        return self.components

    def check_process(self, name):
        """Check if a process matching *name* is running."""
        try:
            result = subprocess.run(
                ['pgrep', '-f', name],
                capture_output=True,
                timeout=5,
            )
            return 'running' if result.returncode == 0 else 'stopped'
        except Exception as e:
            self.logger.debug(f"pgrep check failed for {name}: {e}")
            return 'unknown'
        """Check if a Docker container is running."""
        try:
            result = subprocess.run(
                ['docker', 'ps', '--filter', f'name={name}', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return 'running' if name in result.stdout else 'stopped'
        except Exception as e:
            self.logger.debug(f"docker ps check failed for {name}: {e}")
            return 'unknown'
        """Start a system component and store its handle for later management."""
        self.logger.info(f"🚀 Starting {component_name}...")

        # Python-process-based components – keyed by name to their script path
        _PROCESS_MAP = {
            'jessicai': '/opt/ai-systems/jessicai_huntress.py',
            'nai_gail': '/opt/nai-gail/mesh_shield.py',
            'nia_vault': '/opt/nia-vault/blockchain.py',
        }

        try:
            if component_name == 'docker':
                subprocess.run(['systemctl', 'start', 'docker'], timeout=10, check=False)

            elif component_name in _PROCESS_MAP:
                # Terminate any previously stored process first
                self._terminate_proc(component_name)
                proc = subprocess.Popen(
                    ['python3', _PROCESS_MAP[component_name]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self.components[component_name]['proc'] = proc

            elif component_name == 'rancher':
                # Only start if not already running
                if self.check_docker_container('rancher') != 'running':
                    subprocess.run([
                        'docker', 'run', '-d',
                        '--name', 'rancher',
                        '--restart=unless-stopped',
                        '-p', '80:80',
                        '-p', '443:443',
                        '--privileged',
                        'rancher/rancher:latest',
                    ], timeout=30, check=False)

            self.components[component_name]['status'] = 'running'
            self.logger.info(f"✅ {component_name} started")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to start {component_name}: {e}")
            self.components[component_name]['status'] = 'stopped'
            return False

    def _terminate_proc(self, component_name):
        """Terminate a stored subprocess if it is still alive."""
        proc = self.components.get(component_name, {}).get('proc')
        if proc is not None and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
        self.components[component_name]['proc'] = None

    def stop_component(self, component_name):
        """Stop a system component."""
        self.logger.info(f"⏹️  Stopping {component_name}...")

        try:
            if component_name == 'docker':
                subprocess.run(['systemctl', 'stop', 'docker'], timeout=10, check=False)

            elif component_name in ('jessicai', 'nai_gail', 'nia_vault'):
                self._terminate_proc(component_name)

            elif component_name == 'rancher':
                subprocess.run(['docker', 'stop', 'rancher'], timeout=30, check=False)
                subprocess.run(['docker', 'rm', 'rancher'], timeout=10, check=False)

            self.components[component_name]['status'] = 'stopped'
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
            if status['status'] == 'stopped':
                self.logger.warning(f"⚠️  {component} is down, attempting restart...")
                self.restart_component(component)
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
        """Save observations to file."""
        try:
            with open('/var/log/naydoev1-observations.json', 'w') as f:
                json.dump({
                    'observations': self.observations[-1000:],
                    'decisions': self.decisions[-1000:],
                    'patterns': dict(self.patterns),
                }, f, indent=2)
        except OSError as exc:
            self.logger.warning(f"Could not save observations: {exc}")
    
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
        except Exception as e:
            self.logger.debug(f"Memory info unavailable: {e}")
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
