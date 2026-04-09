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
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# Centralised root – every component path is derived from here
_ROOT = Path('/opt/infinite-server26')

def _setup_paths():
    """Add all component directories to sys.path once."""
    dirs = [
        _ROOT,
        _ROOT / 'plugins' / 'core',
        _ROOT / 'data-streams' / 'core',
        _ROOT / 'news-vault' / 'core',
        _ROOT / 'intelligence' / 'core',
        _ROOT / 'updates' / 'core',
        Path('/opt/ai-systems'),
    ]
    for d in dirs:
        s = str(d)
        if s not in sys.path:
            sys.path.insert(0, s)

_setup_paths()

def _make_logger(name: str) -> logging.Logger:
    """Return a named logger, adding handlers only once."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(f'%(asctime)s [{name}] %(levelname)s: %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    try:
        fh = logging.FileHandler(f'/var/log/{name.lower()}.log')
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except OSError:
        pass  # /var/log may not be writable outside production
    return logger


class PipelineOrchestrator:
    def __init__(self):
        self.name = "PipelineOrchestrator"
        self.version = "1.0"
        self._stop_event = threading.Event()

        # Component status – single source of truth
        self.components = {
            'plugin_manager': {'status': 'stopped', 'last_check': None},
            'update_pipeline': {'status': 'stopped', 'last_check': None},
            'data_streams':    {'status': 'stopped', 'last_check': None},
            'news_vault':      {'status': 'stopped', 'last_check': None},
            'intel_aggregator':{'status': 'stopped', 'last_check': None},
            'naydoev1':        {'status': 'stopped', 'last_check': None},
            'jessicai':        {'status': 'stopped', 'last_check': None},
        }

        self.logger = _make_logger('PipelineOrchestrator')
        self.logger.info("Pipeline Orchestrator initialized")

    @property
    def running(self) -> bool:
        return not self._stop_event.is_set()

    def start_all_systems(self):
        """Start all pipeline systems concurrently then begin monitoring."""
        self.logger.info("🚀 Starting all pipeline systems...")
        self._stop_event.clear()

        # Infrastructure components can start in parallel
        infra_starters = [
            self._start_plugin_manager,
            self._start_data_streams,
            self._start_news_vault,
            self._start_intel_aggregator,
            self._start_update_pipeline,
        ]
        with ThreadPoolExecutor(max_workers=len(infra_starters)) as pool:
            futures = {pool.submit(fn): fn.__name__ for fn in infra_starters}
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    self.logger.error(f"Startup error in {futures[future]}: {exc}")

        # AI systems after infrastructure is ready
        self._start_naydoev1()
        self._start_jessicai()

        self._start_monitoring()
        self.logger.info("✅ All systems started")
    
    def _start_plugin_manager(self):
        """Start plugin manager"""
        try:
            self.logger.info("📦 Starting Plugin Manager...")
            from plugin_manager import PluginManager
            self.plugin_manager = PluginManager()
            self.plugin_manager.discover_plugins()
            self.plugin_manager.load_all_plugins()
            self._mark_running('plugin_manager')
            self.logger.info("✅ Plugin Manager started")
            
        except Exception as e:
            self.logger.error(f"❌ Plugin Manager failed: {e}")
            self.components['plugin_manager']['status'] = 'failed'
    
    def _start_data_streams(self):
        """Start data stream manager"""
        try:
            self.logger.info("📡 Starting Data Stream Manager...")
            from stream_manager import DataStreamManager
            self.stream_manager = DataStreamManager()
            self.stream_manager.start_auto_update()
            self._mark_running('data_streams')
            self.logger.info("✅ Data Stream Manager started")
        except Exception as e:
            self.logger.error(f"❌ Data Stream Manager failed: {e}")
            self.components['data_streams']['status'] = 'failed'

    def _start_news_vault(self):
        """Start news vault"""
        try:
            self.logger.info("🔐 Starting News Vault...")
            from news_vault import NewsVault
            self.news_vault = NewsVault()
            self._mark_running('news_vault')
            self.logger.info("✅ News Vault started")
        except Exception as e:
            self.logger.error(f"❌ News Vault failed: {e}")
            self.components['news_vault']['status'] = 'failed'

    def _start_intel_aggregator(self):
        """Start intelligence aggregator"""
        try:
            self.logger.info("🔍 Starting Intelligence Aggregator...")
            from intel_aggregator import IntelligenceAggregator
            self.intel_aggregator = IntelligenceAggregator()
            self._mark_running('intel_aggregator')
            self.logger.info("✅ Intelligence Aggregator started")
        except Exception as e:
            self.logger.error(f"❌ Intelligence Aggregator failed: {e}")
            self.components['intel_aggregator']['status'] = 'failed'

    def _start_update_pipeline(self):
        """Start update pipeline"""
        try:
            self.logger.info("🔄 Starting Update Pipeline...")
            from update_pipeline import UpdatePipeline
            self.update_pipeline = UpdatePipeline()
            self._mark_running('update_pipeline')
            self.logger.info("✅ Update Pipeline started")
        except Exception as e:
            self.logger.error(f"❌ Update Pipeline failed: {e}")
            self.components['update_pipeline']['status'] = 'failed'
    
    def _mark_running(self, name: str):
        """Mark a component as running with current timestamp."""
        self.components[name]['status'] = 'running'
        self.components[name]['last_check'] = datetime.now().isoformat()

    def _start_naydoev1(self):
        """Start NayDoeV1 orchestrator"""
        try:
            self.logger.info("🤖 Starting NayDoeV1...")
            # NayDoeV1 integration here
            self._mark_running('naydoev1')
            self.logger.info("✅ NayDoeV1 started")
        except Exception as e:
            self.logger.error(f"❌ NayDoeV1 failed: {e}")
            self.components['naydoev1']['status'] = 'failed'

    def _start_jessicai(self):
        """Start JessicAi huntress"""
        try:
            self.logger.info("⚔️  Starting JessicAi...")
            # JessicAi integration here
            self._mark_running('jessicai')
            self.logger.info("✅ JessicAi started")
        except Exception as e:
            self.logger.error(f"❌ JessicAi failed: {e}")
            self.components['jessicai']['status'] = 'failed'

    def _start_monitoring(self):
        """Start monitoring loop in background thread"""
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True,
                                          name='PipelineMonitor')
        monitor_thread.start()
        self.logger.info("👁️  Monitoring started")

    def _monitoring_loop(self):
        """Health-monitoring loop: verify components and attempt restart on failure."""
        # Map component names to their restart functions
        restarters = {
            'plugin_manager':  self._start_plugin_manager,
            'data_streams':    self._start_data_streams,
            'news_vault':      self._start_news_vault,
            'intel_aggregator':self._start_intel_aggregator,
            'update_pipeline': self._start_update_pipeline,
            'naydoev1':        self._start_naydoev1,
            'jessicai':        self._start_jessicai,
        }
        while not self._stop_event.wait(60):
            try:
                for name, info in list(self.components.items()):
                    if info['status'] == 'failed':
                        self.logger.warning(f"⚠️  {name} is in failed state – attempting restart")
                        restart_fn = restarters.get(name)
                        if restart_fn:
                            restart_fn()
                    elif info['status'] == 'running':
                        info['last_check'] = datetime.now().isoformat()
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
    
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
            self.logger.info(f"📄 Daily report: {len(daily_report) if daily_report else 0} items")

            # Weekly report (if Monday)
            if datetime.now().weekday() == 0:
                weekly_report = self.intel_aggregator.generate_weekly_report()
                self.logger.info(f"📄 Weekly report: {len(weekly_report) if weekly_report else 0} items")
            
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
        detail_map = {
            'plugins':      ('plugin_manager', 'list_plugins'),
            'streams':      ('stream_manager',  'get_status'),
            'vault':        ('news_vault',       'get_status'),
            'intelligence': ('intel_aggregator', 'get_status'),
            'updates':      ('update_pipeline',  'get_status'),
        }
        for key, (attr, method) in detail_map.items():
            obj = getattr(self, attr, None)
            if obj is not None:
                try:
                    status[key] = getattr(obj, method)()
                except Exception as exc:
                    self.logger.debug(f"Could not fetch {key} status: {exc}")
        
        return status
    
    def stop_all_systems(self):
        """Stop all systems and signal the monitoring thread to exit."""
        self.logger.info("⏹️  Stopping all systems...")

        self._stop_event.set()

        if hasattr(self, 'stream_manager'):
            try:
                self.stream_manager.stop_auto_update()
            except Exception as exc:
                self.logger.error(f"Error stopping stream manager: {exc}")

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
