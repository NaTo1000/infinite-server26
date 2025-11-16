#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - INTELLIGENCE AGGREGATOR                     ║
║  AI-Powered Threat Intelligence Analysis                         ║
║  Version: 1.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Add parent directories to path
sys.path.insert(0, '/opt/infinite-server26')

class IntelligenceAggregator:
    def __init__(self):
        self.name = "IntelligenceAggregator"
        self.version = "1.0"
        self.intel_dir = Path('/opt/infinite-server26/intelligence')
        self.reports_dir = self.intel_dir / 'reports'
        
        # Intelligence categories
        self.categories = {
            'cve': 'CVE Vulnerabilities',
            'exploits': 'Exploit Intelligence',
            'malware': 'Malware Analysis',
            'threat-actors': 'Threat Actor Profiles',
            'ioc': 'Indicators of Compromise',
            'ttps': 'Tactics, Techniques, Procedures',
            'news': 'Security News',
            'advisories': 'Security Advisories'
        }
        
        # Severity levels
        self.severity_levels = ['critical', 'high', 'medium', 'low', 'info']
        
        # Aggregated intelligence
        self.intelligence = defaultdict(list)
        
        # Setup directories
        self.intel_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [IntelAggregator] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/intel-aggregator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('IntelAggregator')
        
        self.logger.info("Intelligence Aggregator initialized")
    
    def aggregate_from_streams(self, stream_data):
        """Aggregate intelligence from data streams"""
        self.logger.info("🔄 Aggregating intelligence from streams...")
        
        aggregated_count = 0
        
        for stream_name, data in stream_data.items():
            category = data.get('category', 'unknown')
            items = data.get('data', [])
            
            if isinstance(items, list):
                for item in items:
                    intel = self._process_stream_item(stream_name, category, item)
                    if intel:
                        self.intelligence[category].append(intel)
                        aggregated_count += 1
        
        self.logger.info(f"✅ Aggregated {aggregated_count} intelligence items")
        return aggregated_count
    
    def _process_stream_item(self, source, category, item):
        """Process individual stream item"""
        if not isinstance(item, dict):
            return None
        
        intel = {
            'source': source,
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'title': item.get('title', 'Untitled'),
            'link': item.get('link', ''),
            'summary': item.get('summary', ''),
            'severity': self._assess_severity(item),
            'tags': self._extract_tags(item)
        }
        
        return intel
    
    def _assess_severity(self, item):
        """Assess severity of intelligence item"""
        title = item.get('title', '').lower()
        summary = item.get('summary', '').lower()
        
        # Critical keywords
        if any(word in title or word in summary for word in ['critical', 'zero-day', '0day', 'rce', 'remote code execution']):
            return 'critical'
        
        # High keywords
        if any(word in title or word in summary for word in ['high', 'exploit', 'vulnerability', 'breach']):
            return 'high'
        
        # Medium keywords
        if any(word in title or word in summary for word in ['medium', 'update', 'patch', 'security']):
            return 'medium'
        
        # Default
        return 'low'
    
    def _extract_tags(self, item):
        """Extract tags from item"""
        tags = []
        
        title = item.get('title', '').lower()
        summary = item.get('summary', '').lower()
        
        # Common security tags
        tag_keywords = {
            'ransomware': ['ransomware', 'crypto', 'encryption'],
            'phishing': ['phishing', 'spear', 'social engineering'],
            'malware': ['malware', 'trojan', 'virus', 'worm'],
            'apt': ['apt', 'advanced persistent'],
            'ddos': ['ddos', 'denial of service'],
            'sql-injection': ['sql injection', 'sqli'],
            'xss': ['xss', 'cross-site scripting'],
            'rce': ['rce', 'remote code execution'],
            'privilege-escalation': ['privilege escalation', 'privesc'],
            'data-breach': ['data breach', 'leak', 'exposed']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in title or keyword in summary for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def generate_daily_report(self):
        """Generate daily intelligence report"""
        self.logger.info("📊 Generating daily intelligence report...")
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'period': 'daily',
            'summary': {
                'total_items': sum(len(items) for items in self.intelligence.values()),
                'by_category': {cat: len(items) for cat, items in self.intelligence.items()},
                'by_severity': self._count_by_severity()
            },
            'critical_items': self._get_by_severity('critical'),
            'high_items': self._get_by_severity('high'),
            'trending_tags': self._get_trending_tags(),
            'recommendations': self._generate_recommendations()
        }
        
        # Save report
        report_file = self.reports_dir / f"daily_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"✅ Daily report generated: {report_file}")
        return report
    
    def generate_weekly_report(self):
        """Generate weekly intelligence report"""
        self.logger.info("📊 Generating weekly intelligence report...")
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'period': 'weekly',
            'summary': {
                'total_items': sum(len(items) for items in self.intelligence.values()),
                'by_category': {cat: len(items) for cat, items in self.intelligence.items()},
                'by_severity': self._count_by_severity()
            },
            'top_threats': self._get_top_threats(10),
            'trending_tags': self._get_trending_tags(20),
            'category_analysis': self._analyze_categories(),
            'recommendations': self._generate_recommendations()
        }
        
        # Save report
        report_file = self.reports_dir / f"weekly_{datetime.now().strftime('%Y_W%W')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"✅ Weekly report generated: {report_file}")
        return report
    
    def _count_by_severity(self):
        """Count intelligence by severity"""
        severity_count = defaultdict(int)
        
        for items in self.intelligence.values():
            for item in items:
                severity = item.get('severity', 'low')
                severity_count[severity] += 1
        
        return dict(severity_count)
    
    def _get_by_severity(self, severity):
        """Get intelligence items by severity"""
        items = []
        
        for category_items in self.intelligence.values():
            for item in category_items:
                if item.get('severity') == severity:
                    items.append(item)
        
        return sorted(items, key=lambda x: x['timestamp'], reverse=True)
    
    def _get_trending_tags(self, limit=10):
        """Get trending tags"""
        tag_count = defaultdict(int)
        
        for items in self.intelligence.values():
            for item in items:
                for tag in item.get('tags', []):
                    tag_count[tag] += 1
        
        # Sort by count
        trending = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
        
        return [{'tag': tag, 'count': count} for tag, count in trending[:limit]]
    
    def _get_top_threats(self, limit=10):
        """Get top threats"""
        critical_and_high = []
        
        for items in self.intelligence.values():
            for item in items:
                if item.get('severity') in ['critical', 'high']:
                    critical_and_high.append(item)
        
        # Sort by severity then timestamp
        severity_order = {'critical': 0, 'high': 1}
        critical_and_high.sort(
            key=lambda x: (severity_order.get(x.get('severity', 'low'), 2), x['timestamp']),
            reverse=True
        )
        
        return critical_and_high[:limit]
    
    def _analyze_categories(self):
        """Analyze intelligence by category"""
        analysis = {}
        
        for category, items in self.intelligence.items():
            if not items:
                continue
            
            severity_dist = defaultdict(int)
            for item in items:
                severity_dist[item.get('severity', 'low')] += 1
            
            analysis[category] = {
                'total': len(items),
                'severity_distribution': dict(severity_dist),
                'latest': items[-1] if items else None
            }
        
        return analysis
    
    def _generate_recommendations(self):
        """Generate security recommendations"""
        recommendations = []
        
        # Check for critical items
        critical_count = len(self._get_by_severity('critical'))
        if critical_count > 0:
            recommendations.append({
                'priority': 'critical',
                'action': f"Review and address {critical_count} critical security items immediately",
                'category': 'immediate-action'
            })
        
        # Check for high severity items
        high_count = len(self._get_by_severity('high'))
        if high_count > 5:
            recommendations.append({
                'priority': 'high',
                'action': f"Prioritize {high_count} high-severity security items",
                'category': 'priority-action'
            })
        
        # Check trending tags
        trending = self._get_trending_tags(5)
        if trending:
            top_tag = trending[0]['tag']
            recommendations.append({
                'priority': 'medium',
                'action': f"Monitor '{top_tag}' threats - trending in intelligence feeds",
                'category': 'monitoring'
            })
        
        # General recommendations
        recommendations.append({
            'priority': 'low',
            'action': "Maintain regular system updates and security patches",
            'category': 'maintenance'
        })
        
        return recommendations
    
    def get_status(self):
        """Get aggregator status"""
        return {
            'version': self.version,
            'total_intelligence': sum(len(items) for items in self.intelligence.values()),
            'categories': len(self.intelligence),
            'critical_items': len(self._get_by_severity('critical')),
            'high_items': len(self._get_by_severity('high')),
            'last_aggregation': datetime.now().isoformat()
        }

if __name__ == '__main__':
    aggregator = IntelligenceAggregator()
    
    print("\n" + "="*70)
    print("🔍 INTELLIGENCE AGGREGATOR - STATUS")
    print("="*70)
    
    status = aggregator.get_status()
    print(f"Version: {status['version']}")
    print(f"Total Intelligence: {status['total_intelligence']}")
    print(f"Categories: {status['categories']}")
    print(f"Critical Items: {status['critical_items']}")
    print(f"High Items: {status['high_items']}")
    
    print("="*70 + "\n")
