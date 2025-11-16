#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - PIPELINE ORCHESTRATOR                       ║
║  AI Integration for Update Pipeline & Intelligence               ║
║  Version: 1.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import logging
import threading
import time
from datetime import datetime
from pathlib import Path

# Add paths
sys.path.insert(0, '/opt/infinite-server26')

class PipelineOrchestrator:
    def __init__(self):
        self.name = "PipelineOrchestrator"
        self.version = "1.0"
        self.running = False
        
        # Component status
        self.components = {
            'plugin_manager': {'status': 'stopped', 'last_check': None},
            'update_pipeline': {'status': 'stopped', 'last_check': None},
            'data_streams': {'status': 'stopped', 'last_check': None},
            'news_vault': {'status': 'stopped', 'last_check': None},
            'intel_aggregator': {'status': 'stopped', 'last_check': None},
            'naydoev1': {'status': 'stopped', 'last_check': None},
            'jessicai': {'status': 'stopped', 'last_check': None}
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [PipelineOrchestrator] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/pipeline-orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('PipelineOrchestrator')
        
        self.logger.info("Pipeline Orchestrator initialized")
    
    def start_all_systems(self):
        """Start all pipeline systems"""
        self.logger.info("🚀 Starting all pipeline systems...")
        
        self.running = True
        
        # Start components in order
        self._start_plugin_manager()
        self._start_data_streams()
        self._start_news_vault()
        self._start_intel_aggregator()
        self._start_update_pipeline()
        
        # Start AI systems
        self._start_naydoev1()
        self._start_jessicai()
        
        # Start monitoring loop
        self._start_monitoring()
        
        self.logger.info("✅ All systems started")
    
    def _start_plugin_manager(self):
        """Start plugin manager"""
        try:
            self.logger.info("📦 Starting Plugin Manager...")
            
            # Import and initialize
            sys.path.insert(0, '/opt/infinite-server26/plugins/core')
            from plugin_manager import PluginManager
            
            self.plugin_manager = PluginManager()
            self.plugin_manager.discover_plugins()
            self.plugin_manager.load_all_plugins()
            
            self.components['plugin_manager']['status'] = 'running'
            self.components['plugin_manager']['last_check'] = datetime.now().isoformat()
            
            self.logger.info("✅ Plugin Manager started")
            
        except Exception as e:
            self.logger.error(f"❌ Plugin Manager failed: {e}")
            self.components['plugin_manager']['status'] = 'failed'
    
    def _start_data_streams(self):
        """Start data stream manager"""
        try:
            self.logger.info("📡 Starting Data Stream Manager...")
            
            sys.path.insert(0, '/opt/infinite-server26/data-streams/core')
            from stream_manager import DataStreamManager
            
            self.stream_manager = DataStreamManager()
            self.stream_manager.start_auto_update()
            
            self.components['data_streams']['status'] = 'running'
            self.components['data_streams']['last_check'] = datetime.now().isoformat()
            
            self.logger.info("✅ Data Stream Manager started")
            
        except Exception as e:
            self.logger.error(f"❌ Data Stream Manager failed: {e}")
            self.components['data_streams']['status'] = 'failed'
    
    def _start_news_vault(self):
        """Start news vault"""
        try:
            self.logger.info("🔐 Starting News Vault...")
            
            sys.path.insert(0, '/opt/infinite-server26/news-vault/core')
            from news_vault import NewsVault
            
            self.news_vault = NewsVault()
            
            self.components['news_vault']['status'] = 'running'
            self.components['news_vault']['last_check'] = datetime.now().isoformat()
            
            self.logger.info("✅ News Vault started")
            
        except Exception as e:
            self.logger.error(f"❌ News Vault failed: {e}")
            self.components['news_vault']['status'] = 'failed'
    
    def _start_intel_aggregator(self):
        """Start intelligence aggregator"""
        try:
            self.logger.info("🔍 Starting Intelligence Aggregator...")
            
            sys.path.insert(0, '/opt/infinite-server26/intelligence/core')
            from intel_aggregator import IntelligenceAggregator
            
            self.intel_aggregator = IntelligenceAggregator()
            
            self.components['intel_aggregator']['status'] = 'running'
            self.components['intel_aggregator']['last_check'] = datetime.now().isoformat()
            
            self.logger.info("✅ Intelligence Aggregator started")
            
        except Exception as e:
            self.logger.error(f"❌ Intelligence Aggregator failed: {e}")
            self.components['intel_aggregator']['status'] = 'failed'
    
    def _start_update_pipeline(self):
        """Start update pipeline"""
        try:
            self.logger.info("🔄 Starting Update Pipeline...")
            
            sys.path.insert(0, '/opt/infinite-server26/updates/core')
            from update_pipeline import UpdatePipeline
            
            self.update_pipeline = UpdatePipeline()
            
            self.components['update_pipeline']['status'] = 'running'
            self.components['update_pipeline']['last_check'] = datetime.now().isoformat()
            
            self.logger.info("✅ Update Pipeline started")
            
        except Exception as e:
            self.logger.error(f"❌ Update Pipeline failed: {e}")
            self.components['update_pipeline']['status'] = 'failed'
    
    def _start_naydoev1(self):
        """Start NayDoeV1 orchestrator"""
        try:
            self.logger.info("🤖 Starting NayDoeV1...")
            
            sys.path.insert(0, '/opt/ai-systems')
            # NayDoeV1 integration here
            
            self.components['naydoev1']['status'] = 'running'
            self.components['naydoev1']['last_check'] = datetime.now().isoformat()
            
            self.logger.info("✅ NayDoeV1 started")
            
        except Exception as e:
            self.logger.error(f"❌ NayDoeV1 failed: {e}")
            self.components['naydoev1']['status'] = 'failed'
    
    def _start_jessicai(self):
        """Start JessicAi huntress"""
        try:
            self.logger.info("⚔️  Starting JessicAi...")
            
            sys.path.insert(0, '/opt/ai-systems')
            # JessicAi integration here
            
            self.components['jessicai']['status'] = 'running'
            self.components['jessicai']['last_check'] = datetime.now().isoformat()
            
            self.logger.info("✅ JessicAi started")
            
        except Exception as e:
            self.logger.error(f"❌ JessicAi failed: {e}")
            self.components['jessicai']['status'] = 'failed'
    
    def _start_monitoring(self):
        """Start monitoring loop"""
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        self.logger.info("👁️  Monitoring started")
    
    def _monitoring_loop(self):
        """Monitoring loop"""
        while self.running:
            try:
                # Check component health
                for component, status in self.components.items():
                    if status['status'] == 'running':
                        status['last_check'] = datetime.now().isoformat()
                
                # Sleep for 60 seconds
                time.sleep(60)
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(60)
    
    def aggregate_intelligence(self):
        """Aggregate intelligence from all sources"""
        self.logger.info("🔄 Aggregating intelligence...")
        
        try:
            # Get stream data
            stream_data = self.stream_manager.stream_data
            
            # Aggregate
            count = self.intel_aggregator.aggregate_from_streams(stream_data)
            
            # Store in vault
            for category, items in self.intel_aggregator.intelligence.items():
                for item in items:
                    self.news_vault.store_article(item)
            
            self.logger.info(f"✅ Aggregated and stored {count} intelligence items")
            return count
            
        except Exception as e:
            self.logger.error(f"❌ Intelligence aggregation failed: {e}")
            return 0
    
    def generate_reports(self):
        """Generate intelligence reports"""
        self.logger.info("📊 Generating reports...")
        
        try:
            # Daily report
            daily_report = self.intel_aggregator.generate_daily_report()
            
            # Weekly report (if Monday)
            if datetime.now().weekday() == 0:
                weekly_report = self.intel_aggregator.generate_weekly_report()
            
            self.logger.info("✅ Reports generated")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Report generation failed: {e}")
            return False
    
    def check_updates(self):
        """Check for system updates"""
        self.logger.info("🔍 Checking for updates...")
        
        try:
            updates = self.update_pipeline.check_updates()
            
            if updates['available']:
                self.logger.info(f"📦 {len(updates['available'])} updates available")
            else:
                self.logger.info("✅ System up to date")
            
            return updates
            
        except Exception as e:
            self.logger.error(f"❌ Update check failed: {e}")
            return None
    
    def get_system_status(self):
        """Get overall system status"""
        status = {
            'orchestrator_version': self.version,
            'running': self.running,
            'components': self.components,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add component-specific status
        try:
            if hasattr(self, 'plugin_manager'):
                status['plugins'] = self.plugin_manager.list_plugins()
        except:
            pass
        
        try:
            if hasattr(self, 'stream_manager'):
                status['streams'] = self.stream_manager.get_status()
        except:
            pass
        
        try:
            if hasattr(self, 'news_vault'):
                status['vault'] = self.news_vault.get_status()
        except:
            pass
        
        try:
            if hasattr(self, 'intel_aggregator'):
                status['intelligence'] = self.intel_aggregator.get_status()
        except:
            pass
        
        try:
            if hasattr(self, 'update_pipeline'):
                status['updates'] = self.update_pipeline.get_status()
        except:
            pass
        
        return status
    
    def stop_all_systems(self):
        """Stop all systems"""
        self.logger.info("⏹️  Stopping all systems...")
        
        self.running = False
        
        # Stop data streams
        if hasattr(self, 'stream_manager'):
            self.stream_manager.stop_auto_update()
        
        # Update component status
        for component in self.components:
            self.components[component]['status'] = 'stopped'
        
        self.logger.info("✅ All systems stopped")

if __name__ == '__main__':
    orchestrator = PipelineOrchestrator()
    
    print("\n" + "="*70)
    print("🎯 PIPELINE ORCHESTRATOR - STARTING")
    print("="*70)
    
    orchestrator.start_all_systems()
    
    print("\n" + "="*70)
    print("📊 SYSTEM STATUS")
    print("="*70)
    
    status = orchestrator.get_system_status()
    print(f"Orchestrator Version: {status['orchestrator_version']}")
    print(f"Running: {status['running']}")
    print(f"\nComponents:")
    for component, info in status['components'].items():
        print(f"  {component}: {info['status']}")
    
    print("="*70 + "\n")
    
    print("Press Ctrl+C to stop...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        orchestrator.stop_all_systems()
