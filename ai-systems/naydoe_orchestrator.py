#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  NAYDOEV1 - AUTONOMOUS AI INTELLIGENCE ENGINE                    ║
║  Pattern Learning & Resource Optimisation for Infinite Server26  ║
║  Version: 2.0 | Built by: NaTo1000                               ║
║                                                                   ║
║  Studies system behaviour, records observations, surfaces        ║
║  resource anomalies.  Lifecycle is managed by PipelineOrchestrator║
╚═══════════════════════════════════════════════════════════════════╝
"""

import json
import logging
import os
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger('NayDoeV1')


class NayDoeV1Orchestrator:
    """AI intelligence and resource-optimisation engine.

    Observes system state, learns patterns, and surfaces decisions.
    Lifecycle (start/stop) is managed by PipelineOrchestrator; this
    class does not spawn sub-processes or manage component lifetimes
    itself.
    """

    VERSION = '2.0'

    def __init__(self):
        self.name    = 'NayDoeV1'
        self.mode    = 'AUTONOMOUS'
        self.running = True

        # Learning data
        self._observations: list      = []
        self._decisions:    list      = []
        self._patterns:     defaultdict = defaultdict(int)

        self._obs_path = Path(
            os.getenv('INFINITE_LOG_DIR', '/var/log')
        ) / 'naydoev1-observations.json'

        logger.info("NayDoeV1 v%s initialised (mode=%s)", self.VERSION, self.mode)

    # ── Observation & decision recording ─────────────────────────────────────
    def observe(self, event: str) -> None:
        """Record a system event for pattern learning."""
        self._observations.append({'ts': datetime.now().isoformat(), 'event': event})
        self._patterns[event] += 1
        if len(self._observations) % 100 == 0:
            self.save_state()

    def decide(self, action: str) -> None:
        """Record an autonomous decision."""
        self._decisions.append({'ts': datetime.now().isoformat(), 'action': action})
        logger.debug("Decision recorded: %s", action)

    # ── Resource assessment ────────────────────────────────────────────────
    def check_memory(self) -> dict:
        """Return basic memory usage info."""
        try:
            result = subprocess.run(
                ['free', '-m'], capture_output=True, text=True, timeout=5
            )
            parts = result.stdout.splitlines()[1].split()
            total, used = int(parts[1]), int(parts[2])
            pct = round(used / total * 100, 1) if total else 0.0
            return {'total_mb': total, 'used_mb': used, 'usage_pct': pct}
        except Exception as exc:
            logger.debug("Memory check failed: %s", exc)
            return {'total_mb': 0, 'used_mb': 0, 'usage_pct': 0.0}

    def check_cpu_load(self) -> Tuple[float, float, float]:
        """Return (1 m, 5 m, 15 m) load averages."""
        try:
            return os.getloadavg()
        except OSError:
            return (0.0, 0.0, 0.0)

    def assess_resources(self) -> dict:
        """Evaluate current resource usage and record anomalies."""
        mem  = self.check_memory()
        load = self.check_cpu_load()

        if load[0] > 4.0:
            logger.warning("High CPU load: %.2f", load[0])
            self.observe('high_cpu_load')

        if mem['usage_pct'] > 80:
            logger.warning("High memory usage: %.1f%%", mem['usage_pct'])
            self.observe('high_memory_usage')

        return {'memory': mem, 'load': {'1m': load[0], '5m': load[1], '15m': load[2]}}

    # ── Pattern analysis ───────────────────────────────────────────────────
    def top_patterns(self, n: int = 10) -> List[tuple]:
        """Return the n most-frequent observed events."""
        return sorted(
            self._patterns.items(), key=lambda kv: kv[1], reverse=True
        )[:n]

    # ── Persistence ────────────────────────────────────────────────────────
    def save_state(self) -> None:
        """Persist observations and patterns to disk."""
        try:
            data = {
                'observations': self._observations[-1000:],
                'decisions':    self._decisions[-1000:],
                'patterns':     dict(self._patterns),
                'saved_at':     datetime.now().isoformat(),
            }
            self._obs_path.write_text(json.dumps(data, indent=2))
        except Exception as exc:
            logger.warning("Could not save state: %s", exc)

    # ── Status ─────────────────────────────────────────────────────────────
    def get_status(self) -> dict:
        resources = self.assess_resources()
        return {
            'version':         self.VERSION,
            'mode':            self.mode,
            'observations':    len(self._observations),
            'decisions':       len(self._decisions),
            'unique_patterns': len(self._patterns),
            'top_patterns':    self.top_patterns(5),
            'resources':       resources,
        }

    def print_status(self) -> None:
        s = self.get_status()
        print('\n' + '=' * 70)
        print(f"  🤖  NAYDOEV1 v{s['version']}  |  mode={s['mode']}")
        print('=' * 70)
        print(f"  Observations : {s['observations']}")
        print(f"  Decisions    : {s['decisions']}")
        print(f"  Patterns     : {s['unique_patterns']}")
        mem  = s['resources']['memory']
        load = s['resources']['load']
        print(f"  Memory       : {mem['used_mb']} / {mem['total_mb']} MB  ({mem['usage_pct']}%)")
        print(f"  CPU load     : {load['1m']}  {load['5m']}  {load['15m']}")
        print('=' * 70 + '\n')


# ── Standalone entry point ────────────────────────────────────────────────────
if __name__ == '__main__':
    import time

    # When run standalone, bootstrap a console logger
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        )

    engine = NayDoeV1Orchestrator()
    engine.print_status()

    print("  Press Ctrl+C to stop…\n")
    try:
        while engine.running:
            engine.assess_resources()
            time.sleep(60)
    except KeyboardInterrupt:
        engine.running = False
        engine.save_state()
        print("NayDoeV1 stopped.")
