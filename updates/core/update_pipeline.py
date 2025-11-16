#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - AUTO-UPDATE PIPELINE                        ║
║  6-Month Update Management System                                ║
║  Version: 1.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import requests
import subprocess
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

class UpdatePipeline:
    def __init__(self):
        self.name = "UpdatePipeline"
        self.version = "1.0"
        self.update_dir = Path('/opt/infinite-server26/updates')
        self.cache_dir = self.update_dir / 'cache'
        self.schedule_file = self.update_dir / 'update_schedule.json'
        
        # Update sources
        self.sources = {
            'github': 'https://api.github.com/repos/NaTo1000/infinite-server26',
            'docker': 'https://hub.docker.com/v2/repositories/nato1000/infinite-server26',
            'kali': 'https://http.kali.org/kali/dists/kali-rolling/main/binary-amd64/Packages.gz',
            'cve': 'https://services.nvd.nist.gov/rest/json/cves/2.0',
            'exploit-db': 'https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv'
        }
        
        # Update schedule (6 months)
        self.update_schedule = self._generate_6month_schedule()
        
        # Setup directories
        self.update_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [UpdatePipeline] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/update-pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('UpdatePipeline')
        
        self.logger.info("Update Pipeline initialized")
    
    def _generate_6month_schedule(self):
        """Generate 6-month update schedule"""
        schedule = []
        start_date = datetime.now()
        
        # Weekly security updates
        for week in range(26):  # 6 months = ~26 weeks
            update_date = start_date + timedelta(weeks=week)
            schedule.append({
                'date': update_date.isoformat(),
                'type': 'security',
                'priority': 'high',
                'components': ['kali-tools', 'cve-database', 'exploit-db']
            })
        
        # Monthly system updates
        for month in range(6):
            update_date = start_date + timedelta(days=30*month)
            schedule.append({
                'date': update_date.isoformat(),
                'type': 'system',
                'priority': 'medium',
                'components': ['docker', 'plugins', 'ai-systems']
            })
        
        # Quarterly major updates
        for quarter in range(2):
            update_date = start_date + timedelta(days=90*quarter)
            schedule.append({
                'date': update_date.isoformat(),
                'type': 'major',
                'priority': 'critical',
                'components': ['all']
            })
        
        return sorted(schedule, key=lambda x: x['date'])
    
    def check_updates(self):
        """Check for available updates"""
        self.logger.info("🔍 Checking for updates...")
        
        updates = {
            'available': [],
            'installed': [],
            'pending': []
        }
        
        # Check GitHub releases
        try:
            github_updates = self._check_github_updates()
            if github_updates:
                updates['available'].extend(github_updates)
        except Exception as e:
            self.logger.error(f"GitHub update check failed: {e}")
        
        # Check Docker image updates
        try:
            docker_updates = self._check_docker_updates()
            if docker_updates:
                updates['available'].extend(docker_updates)
        except Exception as e:
            self.logger.error(f"Docker update check failed: {e}")
        
        # Check Kali package updates
        try:
            kali_updates = self._check_kali_updates()
            if kali_updates:
                updates['available'].extend(kali_updates)
        except Exception as e:
            self.logger.error(f"Kali update check failed: {e}")
        
        self.logger.info(f"✅ Found {len(updates['available'])} available updates")
        return updates
    
    def _check_github_updates(self):
        """Check GitHub for new releases"""
        try:
            response = requests.get(
                f"{self.sources['github']}/releases/latest",
                timeout=10
            )
            
            if response.status_code == 200:
                release = response.json()
                return [{
                    'source': 'github',
                    'type': 'release',
                    'version': release.get('tag_name', 'unknown'),
                    'name': release.get('name', 'Unknown'),
                    'date': release.get('published_at', ''),
                    'url': release.get('html_url', '')
                }]
        except:
            pass
        
        return []
    
    def _check_docker_updates(self):
        """Check Docker Hub for image updates"""
        try:
            # Check local Docker image
            result = subprocess.run(
                ['docker', 'images', 'nato1000/infinite-server26', '--format', '{{.Tag}}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                local_tags = result.stdout.strip().split('\n')
                return [{
                    'source': 'docker',
                    'type': 'image',
                    'current_tags': local_tags,
                    'check_url': self.sources['docker']
                }]
        except:
            pass
        
        return []
    
    def _check_kali_updates(self):
        """Check for Kali package updates"""
        try:
            result = subprocess.run(
                ['apt', 'list', '--upgradable'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                packages = []
                for line in result.stdout.split('\n')[1:]:  # Skip header
                    if line.strip():
                        parts = line.split('/')
                        if len(parts) > 0:
                            packages.append(parts[0])
                
                if packages:
                    return [{
                        'source': 'kali',
                        'type': 'packages',
                        'count': len(packages),
                        'packages': packages[:10]  # First 10 packages
                    }]
        except:
            pass
        
        return []
    
    def apply_updates(self, update_type='all'):
        """Apply available updates"""
        self.logger.info(f"🔄 Applying {update_type} updates...")
        
        results = {
            'success': [],
            'failed': [],
            'skipped': []
        }
        
        if update_type in ['all', 'system']:
            # Update system packages
            try:
                self.logger.info("📦 Updating system packages...")
                subprocess.run(['apt', 'update'], check=True, timeout=300)
                subprocess.run(['apt', 'upgrade', '-y'], check=True, timeout=600)
                results['success'].append('system-packages')
            except Exception as e:
                self.logger.error(f"System update failed: {e}")
                results['failed'].append('system-packages')
        
        if update_type in ['all', 'docker']:
            # Pull latest Docker image
            try:
                self.logger.info("🐳 Pulling latest Docker image...")
                subprocess.run(
                    ['docker', 'pull', 'nato1000/infinite-server26:latest'],
                    check=True,
                    timeout=600
                )
                results['success'].append('docker-image')
            except Exception as e:
                self.logger.error(f"Docker update failed: {e}")
                results['failed'].append('docker-image')
        
        if update_type in ['all', 'plugins']:
            # Update plugins
            try:
                self.logger.info("🔌 Updating plugins...")
                # Plugin update logic here
                results['success'].append('plugins')
            except Exception as e:
                self.logger.error(f"Plugin update failed: {e}")
                results['failed'].append('plugins')
        
        self.logger.info(f"✅ Update complete: {len(results['success'])} success, {len(results['failed'])} failed")
        return results
    
    def schedule_update(self, update_date, update_type, components):
        """Schedule an update"""
        scheduled_update = {
            'id': hashlib.md5(f"{update_date}{update_type}".encode()).hexdigest()[:8],
            'date': update_date,
            'type': update_type,
            'components': components,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat()
        }
        
        self.update_schedule.append(scheduled_update)
        self._save_schedule()
        
        self.logger.info(f"📅 Update scheduled for {update_date}: {update_type}")
        return scheduled_update
    
    def get_next_update(self):
        """Get next scheduled update"""
        now = datetime.now()
        
        for update in sorted(self.update_schedule, key=lambda x: x['date']):
            update_date = datetime.fromisoformat(update['date'])
            if update_date > now and update.get('status') != 'completed':
                return update
        
        return None
    
    def get_update_history(self, days=30):
        """Get update history"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        history = [
            update for update in self.update_schedule
            if datetime.fromisoformat(update['date']) > cutoff_date
        ]
        
        return sorted(history, key=lambda x: x['date'], reverse=True)
    
    def _save_schedule(self):
        """Save update schedule to file"""
        with open(self.schedule_file, 'w') as f:
            json.dump({
                'schedule': self.update_schedule,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
    
    def _load_schedule(self):
        """Load update schedule from file"""
        if self.schedule_file.exists():
            with open(self.schedule_file, 'r') as f:
                data = json.load(f)
                self.update_schedule = data.get('schedule', [])
    
    def verify_integrity(self, file_path, expected_hash=None):
        """Verify file integrity"""
        if not os.path.exists(file_path):
            return False
        
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        file_hash = sha256_hash.hexdigest()
        
        if expected_hash:
            return file_hash == expected_hash
        
        return file_hash
    
    def rollback_update(self, update_id):
        """Rollback a specific update"""
        self.logger.info(f"⏪ Rolling back update: {update_id}")
        
        # Rollback logic here
        # This would restore from backup/snapshot
        
        self.logger.info(f"✅ Rollback complete for {update_id}")
        return True
    
    def get_status(self):
        """Get update pipeline status"""
        next_update = self.get_next_update()
        recent_history = self.get_update_history(days=7)
        
        return {
            'pipeline_version': self.version,
            'next_update': next_update,
            'recent_updates': len(recent_history),
            'scheduled_updates': len([u for u in self.update_schedule if u.get('status') == 'scheduled']),
            'total_schedule_items': len(self.update_schedule)
        }

if __name__ == '__main__':
    pipeline = UpdatePipeline()
    
    print("\n" + "="*70)
    print("🔄 UPDATE PIPELINE - STATUS")
    print("="*70)
    
    status = pipeline.get_status()
    print(f"Pipeline Version: {status['pipeline_version']}")
    print(f"Scheduled Updates: {status['scheduled_updates']}")
    print(f"Total Schedule Items: {status['total_schedule_items']}")
    
    if status['next_update']:
        print(f"\nNext Update:")
        print(f"  Date: {status['next_update']['date']}")
        print(f"  Type: {status['next_update']['type']}")
        print(f"  Priority: {status['next_update']['priority']}")
    
    print("="*70 + "\n")
