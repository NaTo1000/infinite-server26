#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - MAIN SERVER                                 ║
║  Autonomous AI-Powered Security Fortress                         ║
║  Version: 26.2 | Built by: NaTo1000                              ║
║  Multi-Edition Support: Lite, Standard, Enterprise               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import sys
import time
import signal
import threading
import argparse
import os
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent))

from common.utils import print_banner, ConfigLoader, Logger
from core.naydoev1 import NayDoeV1Orchestrator
from core.jessicai import JessicAiHuntress
from core.nia_vault import NiAVault


class InfiniteServer:
    """Main server orchestrator with multi-edition support"""
    
    def __init__(self, edition: str = "standard", config_file: str = None):
        self.edition = edition.lower()
        self.version = f"26.2-{self.edition}"
        
        # Load edition-specific config
        if config_file is None:
            if self.edition == "lite":
                config_file = "config-lite.yaml"
            elif self.edition == "enterprise":
                config_file = "config-enterprise.yaml"
            else:
                config_file = "config.yaml"
        
        self.config = ConfigLoader(config_file)
        self.logger = Logger.setup("InfiniteServer")
        self.running = False
        
        # Components
        self.components: Dict[str, Any] = {}
        self.threads: List[threading.Thread] = []
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        edition_name = {
            "lite": "FORTRESS LITE",
            "standard": "FORTRESS",
            "enterprise": "FORTRESS ENTERPRISE"
        }.get(self.edition, "FORTRESS")
        
        print_banner(f"INFINITE SERVER26 - {edition_name}", self.version)
        self.logger.info(f"Infinite Server26 {self.edition.upper()} edition initializing...")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info("Shutdown signal received")
        self.shutdown()
    
    def initialize_components(self):
        """Initialize all server components based on edition"""
        self.logger.info(f"🚀 Initializing {self.edition.upper()} edition components...")
        
        try:
            # Initialize NayDoeV1 if enabled
            if self.config.get('ai.naydoev1.enabled', True):
                self.components['naydoev1'] = NayDoeV1Orchestrator()
                self.logger.info("✅ NayDoeV1 initialized")
            
            # Initialize JessicAi if enabled
            if self.config.get('ai.jessicai.enabled', True):
                self.components['jessicai'] = JessicAiHuntress()
                self.logger.info("✅ JessicAi initialized")
            
            # Initialize NiA_Vault if enabled (not in lite edition)
            if self.edition != "lite" and self.config.get('blockchain.nia_vault.enabled', True):
                self.components['nia_vault'] = NiAVault()
                self.logger.info("✅ NiA_Vault initialized")
            elif self.edition == "lite":
                self.logger.info("ℹ️  NiA_Vault disabled in Lite edition")
            
            # Enterprise features
            if self.edition == "enterprise":
                self.logger.info("ℹ️  Enterprise features available (API, Plugins, HA)")
            
            self.logger.info(f"✅ Initialized {len(self.components)} components for {self.edition.upper()} edition")
            
        except Exception as e:
            self.logger.error(f"Error initializing components: {e}")
            raise
    
    def start_components(self):
        """Start all components in separate threads"""
        self.logger.info("🚀 Starting components...")
        
        for name, component in self.components.items():
            thread = threading.Thread(
                target=component.run,
                name=name,
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
            self.logger.info(f"✅ Started {name}")
        
        self.logger.info("✅ All components started")
    
    def monitor_status(self):
        """Monitor and print status of all components"""
        while self.running:
            try:
                time.sleep(300)  # Every 5 minutes
                
                print("\n" + "="*70)
                print("🏰 INFINITE SERVER26 - FORTRESS STATUS")
                print("="*70)
                
                for name, component in self.components.items():
                    status = component.get_status()
                    state_icon = "✅" if status['state'] == 'running' else "❌"
                    print(f"{state_icon} {name:<20} {status['state']}")
                
                print("="*70 + "\n")
                
            except Exception as e:
                self.logger.error(f"Error in status monitoring: {e}")
                time.sleep(60)
    
    def run(self):
        """Run the main server"""
        try:
            self.running = True
            
            # Initialize components
            self.initialize_components()
            
            # Start components
            self.start_components()
            
            # Start status monitoring
            self.monitor_status()
            
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
        except Exception as e:
            self.logger.error(f"Server error: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown the server"""
        if not self.running:
            return
        
        self.logger.info("🛑 Shutting down Infinite Server26...")
        self.running = False
        
        # Stop all components
        for name, component in self.components.items():
            try:
                component.stop()
                self.logger.info(f"✅ Stopped {name}")
            except Exception as e:
                self.logger.error(f"Error stopping {name}: {e}")
        
        self.logger.info("✅ Infinite Server26 shutdown complete")
        sys.exit(0)


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Infinite Server26 - Autonomous AI-Powered Security Fortress',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Edition Options:
  lite       - Lite edition for personal use (minimal features)
  standard   - Standard edition for small teams (default)
  enterprise - Enterprise edition for large organizations

Examples:
  python3 server.py --edition=lite
  python3 server.py --edition=standard
  python3 server.py --edition=enterprise --config=custom-config.yaml
        """
    )
    
    parser.add_argument(
        '--edition',
        type=str,
        default='standard',
        choices=['lite', 'standard', 'enterprise'],
        help='Server edition to run (default: standard)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to configuration file (auto-selected based on edition if not specified)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Infinite Server26 v26.2'
    )
    
    args = parser.parse_args()
    
    # Create and run server
    server = InfiniteServer(edition=args.edition, config_file=args.config)
    server.run()
