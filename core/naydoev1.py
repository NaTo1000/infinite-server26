#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  NAYDOEV1 - AUTONOMOUS AI ORCHESTRATOR                           ║
║  Deep Learning System for Infinite Server26 v2                   ║
║  Version: 26.2 | Built by: NaTo1000                              ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import sys
import time
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.utils import ComponentBase, DataStore, print_banner


class NayDoeV1Orchestrator(ComponentBase):
    """Autonomous AI Orchestrator for system management"""
    
    def __init__(self):
        super().__init__("NayDoeV1", "26.2")
        
        # System components
        self.components = {
            'jessicai': {'status': 'stopped', 'restarts': 0},
            'nai_gail': {'status': 'stopped', 'restarts': 0},
            'nia_vault': {'status': 'stopped', 'restarts': 0}
        }
        
        # Learning system
        self.data_store = DataStore(self.paths.get_path('data') / 'naydoev1_observations.json')
        self.patterns = defaultdict(int)
        
        # Configuration
        self.orchestration_interval = self.config.get('ai.naydoev1.orchestration_interval', 60)
        self.auto_heal = self.config.get('ai.naydoev1.auto_heal', True)
        self.learning_mode = self.config.get('ai.naydoev1.learning_mode', True)
        
        print_banner("NAYDOEV1 - AUTONOMOUS ORCHESTRATOR")
    
    def check_system_health(self) -> Dict[str, Dict[str, Any]]:
        """Check health of all system components"""
        self.logger.info("🏥 Checking system health...")
        
        for component in self.components.keys():
            status = self._check_component(component)
            self.components[component]['status'] = status
            self.components[component]['last_check'] = datetime.now().isoformat()
        
        return self.components
    
    def _check_component(self, name: str) -> str:
        """Check if a component process is running"""
        try:
            # Check if process exists
            result = subprocess.run(
                ['pgrep', '-f', name],
                capture_output=True,
                timeout=5
            )
            return 'running' if result.returncode == 0 else 'stopped'
        except Exception as e:
            self.logger.error(f"Error checking {name}: {e}")
            return 'unknown'
    
    def auto_heal_components(self):
        """Automatically heal failed components"""
        if not self.auto_heal:
            return
        
        self.logger.info("🔧 Auto-heal checking...")
        health = self.check_system_health()
        
        for component, info in health.items():
            if info['status'] == 'stopped':
                self.logger.warning(f"⚠️  {component} is down")
                self.observe(f"{component}_failure")
                
                # Only restart if not restarted too many times
                if info['restarts'] < 3:
                    self.logger.info(f"Attempting to restart {component}")
                    self.components[component]['restarts'] += 1
                    # In production, implement actual restart logic
                else:
                    self.logger.error(f"❌ {component} failed too many times, manual intervention needed")
    
    def observe(self, observation: str):
        """Record observation for learning"""
        if not self.learning_mode:
            return
        
        timestamp = datetime.now().isoformat()
        self.patterns[observation] += 1
        
        # Store observation
        observations = self.data_store.get('observations', [])
        observations.append({
            'timestamp': timestamp,
            'observation': observation
        })
        
        # Keep last 1000 observations
        if len(observations) > 1000:
            observations = observations[-1000:]
        
        self.data_store.set('observations', observations)
        self.data_store.set('patterns', dict(self.patterns))
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        status = super().get_status()
        status.update({
            'components': self.components,
            'observations_count': len(self.data_store.get('observations', [])),
            'patterns_learned': len(self.patterns),
            'auto_heal': self.auto_heal,
            'learning_mode': self.learning_mode
        })
        return status
    
    def print_status(self):
        """Print orchestrator status"""
        print("\n" + "="*70)
        print("🤖 NAYDOEV1 ORCHESTRATOR - STATUS")
        print("="*70)
        
        for component, info in self.components.items():
            status_icon = "✅" if info['status'] == 'running' else "❌"
            print(f"{status_icon} {component:<20} {info['status']}")
        
        observations = self.data_store.get('observations', [])
        print(f"\nObservations: {len(observations)}")
        print(f"Patterns Learned: {len(self.patterns)}")
        print(f"Auto-heal: {'ENABLED' if self.auto_heal else 'DISABLED'}")
        print(f"Learning Mode: {'ACTIVE' if self.learning_mode else 'INACTIVE'}")
        print("="*70 + "\n")
    
    def run(self):
        """Main orchestration loop"""
        self.start()
        
        self.logger.info("🎼 Orchestration started")
        
        try:
            while self.running:
                # Check system health
                self.check_system_health()
                
                # Auto-heal if needed
                self.auto_heal_components()
                
                # Print status
                self.print_status()
                
                # Sleep
                time.sleep(self.orchestration_interval)
                
        except KeyboardInterrupt:
            self.logger.info("⏹️  Shutting down NayDoeV1 Orchestrator...")
        except Exception as e:
            self.handle_error(e)
        finally:
            self.stop()


if __name__ == '__main__':
    orchestrator = NayDoeV1Orchestrator()
    orchestrator.run()
