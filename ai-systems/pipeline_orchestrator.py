#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - UNIFIED PIPELINE ORCHESTRATOR               ║
║  Single-process, thread-safe system lifecycle manager            ║
║  Version: 2.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import logging
import threading
import time
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Optional

# ── Path bootstrap ────────────────────────────────────────────────────────────
# INFINITE_BASE_DIR: root of the infinite-server26 installation
#   default: /opt/infinite-server26
# INFINITE_LOG_DIR:  directory for log files
#   default: /var/log
_BASE    = Path(os.getenv('INFINITE_BASE_DIR', '/opt/infinite-server26'))
_LOG_DIR = Path(os.getenv('INFINITE_LOG_DIR',  '/var/log'))


def _add_path(p: Path) -> None:
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)


for _sub in (
    'plugins/core',
    'data-streams/core',
    'news-vault/core',
    'intelligence/core',
    'updates/core',
    'ai-systems',
):
    _add_path(_BASE / _sub)

# ── Root logging (configured once here; all other modules inherit) ───────────
_log_file = _LOG_DIR / 'pipeline-orchestrator.log'
_root = logging.getLogger()
if not _root.handlers:
    _fmt = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
    _sh = logging.StreamHandler()
    _sh.setFormatter(_fmt)
    _root.addHandler(_sh)
    try:
        _fh = logging.FileHandler(str(_log_file))
        _fh.setFormatter(_fmt)
        _root.addHandler(_fh)
    except OSError:
        pass
    _root.setLevel(logging.INFO)


# ── Component lifecycle constants ────────────────────────────────────────────
class ComponentState:
    STOPPED    = 'stopped'
    STARTING   = 'starting'
    RUNNING    = 'running'
    FAILED     = 'failed'
    RESTARTING = 'restarting'


# ── Per-component record ──────────────────────────────────────────────────────
class ComponentRecord:
    """Thread-safe lifecycle record for a single managed component."""

    def __init__(
        self,
        name: str,
        factory: Callable,
        starter: Optional[Callable] = None,
        stopper: Optional[Callable] = None,
        health_check: Optional[Callable] = None,
    ):
        self.name          = name
        self._factory      = factory       # () -> instance
        self._starter      = starter       # (instance) -> None
        self._stopper      = stopper       # (instance) -> None
        self._health_fn    = health_check  # (instance) -> bool
        self._lock         = threading.Lock()
        self.instance      = None
        self.state         = ComponentState.STOPPED
        self.started_at: Optional[datetime] = None
        self.last_check: Optional[datetime] = None
        self.error_count   = 0
        self.restart_count = 0

    def start(self, logger: logging.Logger) -> bool:
        with self._lock:
            self.state = ComponentState.STARTING
        try:
            instance = self._factory()
            if self._starter:
                self._starter(instance)
            with self._lock:
                self.instance   = instance
                self.state      = ComponentState.RUNNING
                self.started_at = datetime.now()
                self.last_check = self.started_at
            logger.info("✅  %s started", self.name)
            return True
        except Exception as exc:
            with self._lock:
                self.state       = ComponentState.FAILED
                self.error_count += 1
            logger.error("❌  %s failed to start: %s", self.name, exc)
            return False

    def stop(self, logger: logging.Logger) -> None:
        with self._lock:
            instance = self.instance
        if instance and self._stopper:
            try:
                self._stopper(instance)
            except Exception as exc:
                logger.warning("⚠️   %s stop error: %s", self.name, exc)
        with self._lock:
            self.instance = None
            self.state    = ComponentState.STOPPED

    def is_healthy(self, logger: logging.Logger) -> bool:
        with self._lock:
            instance = self.instance
            if self.state != ComponentState.RUNNING:
                return False
        try:
            ok = self._health_fn(instance) if self._health_fn else True
            with self._lock:
                self.last_check = datetime.now()
            return ok
        except Exception as exc:
            logger.warning("⚠️   %s health-check raised: %s", self.name, exc)
            return False

    def get_instance(self):
        """Return the running instance, or None if not running (thread-safe)."""
        with self._lock:
            return self.instance if self.state == ComponentState.RUNNING else None

    def snapshot(self) -> dict:
        with self._lock:
            return {
                'state':         self.state,
                'started_at':    self.started_at.isoformat() if self.started_at else None,
                'last_check':    self.last_check.isoformat()  if self.last_check  else None,
                'error_count':   self.error_count,
                'restart_count': self.restart_count,
            }


# ── Unified pipeline orchestrator ────────────────────────────────────────────
class PipelineOrchestrator:
    """Single, authoritative orchestrator for all Infinite Server26 components.

    Startup order:
        1. PluginManager      – load extension plugins
        2. DataStreamManager  – live threat-intel feeds
        3. NewsVault          – encrypted article storage
        4. IntelligenceAggregator – analyse & correlate
        5. UpdatePipeline     – manage 6-month update schedule
        6. NayDoeV1           – AI intelligence engine
        7. JessicAiHuntress   – security monitoring threads

    The monitor thread health-checks every component every 60 s and
    auto-restarts any that are failed or unhealthy.
    """

    VERSION = '2.0'
    _RESTART_DELAY  = 5   # seconds between stop and re-start on recovery
    _CHECK_INTERVAL = 60  # seconds between health-check passes

    def __init__(self):
        self._logger  = logging.getLogger('PipelineOrchestrator')
        self._lock    = threading.Lock()
        self._running = False
        self._started_at: Optional[datetime] = None
        self._monitor_thread: Optional[threading.Thread] = None
        self._registry: Dict[str, ComponentRecord] = self._build_registry()
        self._logger.info("PipelineOrchestrator v%s initialised", self.VERSION)

    # ── Registry ──────────────────────────────────────────────────────────────
    def _build_registry(self) -> Dict[str, ComponentRecord]:
        """Build the ordered component registry.  Import errors are logged as
        warnings so that unavailable modules never prevent other components
        from starting.
        """
        reg: Dict[str, ComponentRecord] = OrderedDict()

        # 1 – Plugin Manager
        try:
            from plugin_manager import PluginManager
            def _pm_starter(pm: PluginManager) -> None:
                pm.discover_plugins()
                pm.load_all_plugins()
            reg['plugin_manager'] = ComponentRecord(
                'PluginManager',
                lambda: PluginManager(str(_BASE / 'plugins')),
                starter=_pm_starter,
                health_check=lambda pm: pm is not None,
            )
        except ImportError as exc:
            self._logger.warning("plugin_manager not importable: %s", exc)

        # 2 – Data Stream Manager
        try:
            from stream_manager import DataStreamManager
            reg['data_streams'] = ComponentRecord(
                'DataStreamManager',
                DataStreamManager,
                starter=lambda sm: sm.start_auto_update(),
                stopper=lambda sm: sm.stop_auto_update(),
                health_check=lambda sm: sm is not None,
            )
        except ImportError as exc:
            self._logger.warning("stream_manager not importable: %s", exc)

        # 3 – News Vault
        try:
            from news_vault import NewsVault
            reg['news_vault'] = ComponentRecord(
                'NewsVault',
                NewsVault,
                health_check=lambda nv: nv is not None,
            )
        except ImportError as exc:
            self._logger.warning("news_vault not importable: %s", exc)

        # 4 – Intelligence Aggregator
        try:
            from intel_aggregator import IntelligenceAggregator
            reg['intel_aggregator'] = ComponentRecord(
                'IntelligenceAggregator',
                IntelligenceAggregator,
                health_check=lambda ia: ia is not None,
            )
        except ImportError as exc:
            self._logger.warning("intel_aggregator not importable: %s", exc)

        # 5 – Update Pipeline
        try:
            from update_pipeline import UpdatePipeline
            reg['update_pipeline'] = ComponentRecord(
                'UpdatePipeline',
                UpdatePipeline,
                health_check=lambda up: up is not None,
            )
        except ImportError as exc:
            self._logger.warning("update_pipeline not importable: %s", exc)

        # 6 – NayDoeV1 AI intelligence engine
        try:
            from naydoe_orchestrator import NayDoeV1Orchestrator
            reg['naydoe'] = ComponentRecord(
                'NayDoeV1',
                NayDoeV1Orchestrator,
                health_check=lambda nd: nd is not None,
            )
        except ImportError as exc:
            self._logger.warning("naydoe_orchestrator not importable: %s", exc)

        # 7 – JessicAi security monitoring
        try:
            from jessicai_huntress import JessicAiHuntress
            def _jessicai_starter(h: JessicAiHuntress) -> None:
                for target in (h.monitor_network, h.monitor_files, h.monitor_processes):
                    t = threading.Thread(
                        target=target,
                        daemon=True,
                        name=f'jessicai-{target.__name__}',
                    )
                    t.start()
            def _jessicai_stopper(h) -> None:
                h.running = False
            reg['jessicai'] = ComponentRecord(
                'JessicAiHuntress',
                JessicAiHuntress,
                starter=_jessicai_starter,
                stopper=_jessicai_stopper,
                health_check=lambda h: h.running,
            )
        except ImportError as exc:
            self._logger.warning("jessicai_huntress not importable: %s", exc)

        return reg

    # ── Lifecycle ─────────────────────────────────────────────────────────────
    def start(self) -> None:
        """Start all registered components in order, then launch the monitor."""
        with self._lock:
            if self._running:
                self._logger.warning("Already running; ignoring start()")
                return
            self._running    = True
            self._started_at = datetime.now()

        self._logger.info("🚀 Starting all pipeline systems…")
        for record in self._registry.values():
            record.start(self._logger)

        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True,
            name='pipeline-monitor',
        )
        self._monitor_thread.start()
        self._logger.info("✅ All systems started — monitor running")

    def stop(self) -> None:
        """Stop all components in reverse start order."""
        self._logger.info("⏹️  Stopping all systems…")
        with self._lock:
            self._running = False
        for record in reversed(list(self._registry.values())):
            record.stop(self._logger)
        self._logger.info("✅ All systems stopped")

    # ── Monitor loop ──────────────────────────────────────────────────────────
    def _monitor_loop(self) -> None:
        """Health-check every component; auto-restart failed or unhealthy ones."""
        while True:
            with self._lock:
                if not self._running:
                    break
            for name, record in self._registry.items():
                try:
                    if record.state == ComponentState.RUNNING:
                        if not record.is_healthy(self._logger):
                            self._logger.warning("⚠️   %s unhealthy — restarting", name)
                            self._restart(record)
                    elif record.state == ComponentState.FAILED:
                        self._logger.info("♻️   Attempting recovery of %s", name)
                        self._restart(record)
                except Exception as exc:
                    self._logger.error("Monitor error for %s: %s", name, exc)
            time.sleep(self._CHECK_INTERVAL)

    def _restart(self, record: ComponentRecord) -> None:
        with record._lock:
            record.state         = ComponentState.RESTARTING
            record.restart_count += 1
        record.stop(self._logger)
        time.sleep(self._RESTART_DELAY)
        record.start(self._logger)

    # ── Intelligence aggregation ───────────────────────────────────────────────
    def aggregate_intelligence(self) -> int:
        """Pull stream data → intel aggregator → news vault."""
        self._logger.info("🔄 Aggregating intelligence…")
        try:
            sm_rec = self._registry.get('data_streams')
            ia_rec = self._registry.get('intel_aggregator')
            nv_rec = self._registry.get('news_vault')
            if not (sm_rec and ia_rec and nv_rec):
                self._logger.warning("Required components missing for aggregation")
                return 0
            sm = sm_rec.get_instance()
            ia = ia_rec.get_instance()
            nv = nv_rec.get_instance()
            if not (sm and ia):
                self._logger.warning("Required components not running for aggregation")
                return 0
            stream_data = sm.stream_data
            count = ia.aggregate_from_streams(stream_data)
            intel = dict(ia.intelligence)
            if nv:
                for items in intel.values():
                    for item in items:
                        nv.store_article(item)
            self._logger.info("✅ Aggregated %d intelligence items", count)
            return count
        except Exception as exc:
            self._logger.error("❌ Intelligence aggregation failed: %s", exc)
            return 0

    # ── Update checks ──────────────────────────────────────────────────────────
    def check_updates(self) -> Optional[dict]:
        self._logger.info("🔍 Checking for updates…")
        record = self._registry.get('update_pipeline')
        if not record or not record.instance:
            self._logger.warning("UpdatePipeline not running")
            return None
        try:
            updates = record.instance.check_updates()
            available = updates.get('available', [])
            if available:
                self._logger.info("📦 %d updates available", len(available))
            else:
                self._logger.info("✅ System up to date")
            return updates
        except Exception as exc:
            self._logger.error("❌ Update check failed: %s", exc)
            return None

    # ── Status / metrics ───────────────────────────────────────────────────────
    def status(self) -> dict:
        """Return a snapshot of the orchestrator and all components."""
        with self._lock:
            uptime_s = (
                (datetime.now() - self._started_at).total_seconds()
                if self._started_at else 0.0
            )
            running = self._running
        components = {name: rec.snapshot() for name, rec in self._registry.items()}
        healthy = sum(
            1 for r in self._registry.values()
            if r.state == ComponentState.RUNNING
        )
        total = len(self._registry)
        return {
            'version':        self.VERSION,
            'running':        running,
            'uptime_seconds': round(uptime_s, 1),
            'components_ok':  f'{healthy}/{total}',
            'components':     components,
            'timestamp':      datetime.now().isoformat(),
        }

    def print_status(self) -> None:
        s = self.status()
        print('\n' + '=' * 70)
        print(
            f"  PIPELINE ORCHESTRATOR v{s['version']}"
            f"  |  uptime {s['uptime_seconds']}s"
            f"  |  {s['components_ok']} healthy"
        )
        print('=' * 70)
        for name, snap in s['components'].items():
            icon = '✅' if snap['state'] == ComponentState.RUNNING else '❌'
            print(
                f"  {icon} {name:<22} {snap['state']:<12}"
                f"  restarts={snap['restart_count']}"
                f"  errors={snap['error_count']}"
            )
        print('=' * 70 + '\n')


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    orch = PipelineOrchestrator()

    print('\n' + '=' * 70)
    print('  🎯  PIPELINE ORCHESTRATOR — STARTING')
    print('=' * 70)

    orch.start()
    orch.print_status()

    print('  Press Ctrl+C to stop…\n')
    try:
        while True:
            time.sleep(60)
            orch.print_status()
    except KeyboardInterrupt:
        orch.stop()
