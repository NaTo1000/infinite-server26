#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - DATA STREAM MANAGER                         ║
║  Real-time Threat Intelligence & Security Feeds                  ║
║  Version: 1.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import requests
import feedparser
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import threading
import time

class DataStream:
    """Base data stream class"""
    def __init__(self, name, url, stream_type='rss'):
        self.name = name
        self.url = url
        self.stream_type = stream_type
        self.enabled = True
        self.last_update = None
        self.update_interval = 3600  # 1 hour default
    
    def fetch(self):
        """Fetch data from stream"""
        raise NotImplementedError
    
    def parse(self, data):
        """Parse stream data"""
        raise NotImplementedError

class DataStreamManager:
    def __init__(self):
        self.name = "DataStreamManager"
        self.version = "1.0"
        self.stream_dir = Path('/opt/infinite-server26/data-streams')
        self.cache_dir = self.stream_dir / 'cache'
        
        # Data streams configuration
        self.streams = {
            # CVE/Vulnerability Feeds
            'nvd_cve': {
                'name': 'NVD CVE Feed',
                'url': 'https://services.nvd.nist.gov/rest/json/cves/2.0',
                'type': 'api',
                'category': 'vulnerabilities',
                'enabled': True
            },
            'cve_mitre': {
                'name': 'MITRE CVE',
                'url': 'https://cve.mitre.org/data/downloads/allitems.csv',
                'type': 'csv',
                'category': 'vulnerabilities',
                'enabled': True
            },
            
            # Exploit Databases
            'exploit_db': {
                'name': 'Exploit-DB',
                'url': 'https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv',
                'type': 'csv',
                'category': 'exploits',
                'enabled': True
            },
            
            # Threat Intelligence
            'alienvault_otx': {
                'name': 'AlienVault OTX',
                'url': 'https://otx.alienvault.com/api/v1/pulses/subscribed',
                'type': 'api',
                'category': 'threat-intel',
                'enabled': True
            },
            'abuse_ch': {
                'name': 'Abuse.ch',
                'url': 'https://urlhaus.abuse.ch/downloads/csv_recent/',
                'type': 'csv',
                'category': 'threat-intel',
                'enabled': True
            },
            
            # Security News
            'kali_blog': {
                'name': 'Kali Linux Blog',
                'url': 'https://www.kali.org/rss.xml',
                'type': 'rss',
                'category': 'news',
                'enabled': True
            },
            'security_weekly': {
                'name': 'Security Weekly',
                'url': 'https://securityweekly.com/feed/',
                'type': 'rss',
                'category': 'news',
                'enabled': True
            },
            'krebs_security': {
                'name': 'Krebs on Security',
                'url': 'https://krebsonsecurity.com/feed/',
                'type': 'rss',
                'category': 'news',
                'enabled': True
            },
            'dark_reading': {
                'name': 'Dark Reading',
                'url': 'https://www.darkreading.com/rss.xml',
                'type': 'rss',
                'category': 'news',
                'enabled': True
            },
            'bleeping_computer': {
                'name': 'Bleeping Computer',
                'url': 'https://www.bleepingcomputer.com/feed/',
                'type': 'rss',
                'category': 'news',
                'enabled': True
            },
            
            # Malware Analysis
            'malware_bazaar': {
                'name': 'MalwareBazaar',
                'url': 'https://bazaar.abuse.ch/export/csv/recent/',
                'type': 'csv',
                'category': 'malware',
                'enabled': True
            },
            
            # IP Reputation
            'blocklist_de': {
                'name': 'Blocklist.de',
                'url': 'https://lists.blocklist.de/lists/all.txt',
                'type': 'txt',
                'category': 'ip-reputation',
                'enabled': True
            },
            
            # GitHub Security
            'github_advisories': {
                'name': 'GitHub Security Advisories',
                'url': 'https://github.com/advisories',
                'type': 'api',
                'category': 'advisories',
                'enabled': True
            }
        }
        
        # Setup directories
        self.stream_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [DataStreamManager] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/data-streams.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('DataStreamManager')
        
        # Stream data storage
        self.stream_data = {}
        self.running = True
        
        self.logger.info("Data Stream Manager initialized")
    
    def fetch_rss_feed(self, stream_name, url):
        """Fetch RSS feed"""
        try:
            self.logger.info(f"📡 Fetching RSS: {stream_name}")
            feed = feedparser.parse(url)
            
            entries = []
            for entry in feed.entries[:20]:  # Latest 20 entries
                entries.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', '')[:200]  # First 200 chars
                })
            
            self.logger.info(f"✅ Fetched {len(entries)} entries from {stream_name}")
            return entries
            
        except Exception as e:
            self.logger.error(f"❌ RSS fetch failed for {stream_name}: {e}")
            return []
    
    def fetch_api_data(self, stream_name, url):
        """Fetch API data"""
        try:
            self.logger.info(f"📡 Fetching API: {stream_name}")
            
            headers = {'User-Agent': 'Infinite-Server26/1.0'}
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json() if 'json' in response.headers.get('content-type', '') else response.text
                self.logger.info(f"✅ API data fetched from {stream_name}")
                return data
            else:
                self.logger.warning(f"⚠️  API returned {response.status_code} for {stream_name}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ API fetch failed for {stream_name}: {e}")
            return None
    
    def fetch_csv_data(self, stream_name, url):
        """Fetch CSV data"""
        try:
            self.logger.info(f"📡 Fetching CSV: {stream_name}")
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                lines = response.text.split('\n')[:100]  # First 100 lines
                self.logger.info(f"✅ CSV data fetched from {stream_name}")
                return lines
            else:
                self.logger.warning(f"⚠️  CSV fetch returned {response.status_code} for {stream_name}")
                return []
                
        except Exception as e:
            self.logger.error(f"❌ CSV fetch failed for {stream_name}: {e}")
            return []
    
    def fetch_stream(self, stream_name):
        """Fetch data from a specific stream"""
        if stream_name not in self.streams:
            self.logger.error(f"❌ Stream not found: {stream_name}")
            return None
        
        stream = self.streams[stream_name]
        
        if not stream['enabled']:
            self.logger.info(f"⏭️  Stream disabled: {stream_name}")
            return None
        
        # Fetch based on type
        if stream['type'] == 'rss':
            data = self.fetch_rss_feed(stream_name, stream['url'])
        elif stream['type'] == 'api':
            data = self.fetch_api_data(stream_name, stream['url'])
        elif stream['type'] == 'csv':
            data = self.fetch_csv_data(stream_name, stream['url'])
        elif stream['type'] == 'txt':
            data = self.fetch_api_data(stream_name, stream['url'])
        else:
            self.logger.error(f"❌ Unknown stream type: {stream['type']}")
            return None
        
        # Cache data
        if data:
            self.stream_data[stream_name] = {
                'data': data,
                'timestamp': datetime.now().isoformat(),
                'category': stream['category']
            }
            
            # Save to cache file
            cache_file = self.cache_dir / f"{stream_name}.json"
            with open(cache_file, 'w') as f:
                json.dump(self.stream_data[stream_name], f, indent=2)
        
        return data
    
    def fetch_all_streams(self):
        """Fetch all enabled streams"""
        self.logger.info("📡 Fetching all data streams...")
        
        fetched_count = 0
        for stream_name in self.streams.keys():
            if self.streams[stream_name]['enabled']:
                data = self.fetch_stream(stream_name)
                if data:
                    fetched_count += 1
                
                # Rate limiting
                time.sleep(2)
        
        self.logger.info(f"✅ Fetched {fetched_count} streams")
        return fetched_count
    
    def get_stream_data(self, stream_name):
        """Get cached stream data"""
        return self.stream_data.get(stream_name)
    
    def get_category_data(self, category):
        """Get all data for a specific category"""
        category_data = {}
        
        for stream_name, data in self.stream_data.items():
            if data.get('category') == category:
                category_data[stream_name] = data
        
        return category_data
    
    def search_streams(self, query):
        """Search across all stream data"""
        results = []
        
        query_lower = query.lower()
        
        for stream_name, stream_data in self.stream_data.items():
            data = stream_data.get('data', [])
            
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        # Search in title and summary
                        title = item.get('title', '').lower()
                        summary = item.get('summary', '').lower()
                        
                        if query_lower in title or query_lower in summary:
                            results.append({
                                'stream': stream_name,
                                'item': item,
                                'timestamp': stream_data.get('timestamp')
                            })
        
        return results
    
    def auto_update_loop(self):
        """Automatic update loop"""
        self.logger.info("🔄 Starting auto-update loop...")
        
        while self.running:
            try:
                self.fetch_all_streams()
                
                # Update every hour
                time.sleep(3600)
                
            except Exception as e:
                self.logger.error(f"Auto-update error: {e}")
                time.sleep(600)  # Wait 10 minutes on error
    
    def start_auto_update(self):
        """Start automatic updates in background"""
        update_thread = threading.Thread(target=self.auto_update_loop, daemon=True)
        update_thread.start()
        self.logger.info("✅ Auto-update started")
    
    def stop_auto_update(self):
        """Stop automatic updates"""
        self.running = False
        self.logger.info("⏹️  Auto-update stopped")
    
    def get_status(self):
        """Get stream manager status"""
        return {
            'version': self.version,
            'total_streams': len(self.streams),
            'enabled_streams': len([s for s in self.streams.values() if s['enabled']]),
            'cached_streams': len(self.stream_data),
            'categories': list(set(s['category'] for s in self.streams.values())),
            'last_update': max(
                [d.get('timestamp', '') for d in self.stream_data.values()],
                default='Never'
            )
        }

if __name__ == '__main__':
    manager = DataStreamManager()
    
    print("\n" + "="*70)
    print("📡 DATA STREAM MANAGER - STATUS")
    print("="*70)
    
    status = manager.get_status()
    print(f"Version: {status['version']}")
    print(f"Total Streams: {status['total_streams']}")
    print(f"Enabled Streams: {status['enabled_streams']}")
    print(f"Cached Streams: {status['cached_streams']}")
    print(f"\nCategories:")
    for cat in status['categories']:
        print(f"  • {cat}")
    
    print("="*70 + "\n")
