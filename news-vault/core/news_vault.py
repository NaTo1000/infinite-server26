#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - SECURE NEWS VAULT                           ║
║  Encrypted Intelligence & News Storage System                    ║
║  Version: 1.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

class NewsVault:
    def __init__(self):
        self.name = "NewsVault"
        self.version = "1.0"
        self.vault_dir = Path('/opt/infinite-server26/news-vault')
        self.storage_dir = self.vault_dir / 'storage'
        self.index_file = self.vault_dir / 'vault_index.json'
        
        # Encryption
        self.master_key = None
        self.vault_password = "nato1000_news_vault_secure"  # Should be changed
        
        # Storage index
        self.vault_index = {}
        
        # Setup directories
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [NewsVault] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/news-vault.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('NewsVault')
        
        # Initialize vault
        self._initialize_vault()
        
        self.logger.info("News Vault initialized")
    
    def _initialize_vault(self):
        """Initialize vault with encryption"""
        # Derive master key
        salt_file = self.vault_dir / '.salt'
        
        if salt_file.exists():
            with open(salt_file, 'rb') as f:
                salt = f.read()
        else:
            salt = get_random_bytes(32)
            with open(salt_file, 'wb') as f:
                f.write(salt)
        
        self.master_key = PBKDF2(self.vault_password, salt, dkLen=32, count=100000)
        
        # Load index
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.vault_index = json.load(f)
    
    def encrypt_data(self, data):
        """Encrypt data with AES-256-GCM"""
        if isinstance(data, str):
            data = data.encode()
        
        nonce = get_random_bytes(16)
        cipher = AES.new(self.master_key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        return {
            'nonce': nonce.hex(),
            'ciphertext': ciphertext.hex(),
            'tag': tag.hex()
        }
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data"""
        nonce = bytes.fromhex(encrypted_data['nonce'])
        ciphertext = bytes.fromhex(encrypted_data['ciphertext'])
        tag = bytes.fromhex(encrypted_data['tag'])
        
        cipher = AES.new(self.master_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        
        return plaintext.decode()
    
    def store_article(self, article):
        """Store encrypted article"""
        article_id = hashlib.md5(
            f"{article.get('title', '')}{article.get('link', '')}".encode()
        ).hexdigest()
        
        # Encrypt article
        encrypted = self.encrypt_data(json.dumps(article))
        
        # Save encrypted article
        article_file = self.storage_dir / f"{article_id}.enc"
        with open(article_file, 'w') as f:
            json.dump(encrypted, f)
        
        # Update index
        self.vault_index[article_id] = {
            'title': article.get('title', 'Untitled'),
            'category': article.get('category', 'general'),
            'source': article.get('source', 'unknown'),
            'timestamp': article.get('timestamp', datetime.now().isoformat()),
            'file': str(article_file),
            'tags': article.get('tags', [])
        }
        
        self._save_index()
        
        self.logger.info(f"📰 Article stored: {article.get('title', 'Untitled')[:50]}")
        return article_id
    
    def retrieve_article(self, article_id):
        """Retrieve and decrypt article"""
        if article_id not in self.vault_index:
            self.logger.error(f"❌ Article not found: {article_id}")
            return None
        
        article_file = Path(self.vault_index[article_id]['file'])
        
        if not article_file.exists():
            self.logger.error(f"❌ Article file missing: {article_file}")
            return None
        
        # Load encrypted article
        with open(article_file, 'r') as f:
            encrypted = json.load(f)
        
        # Decrypt
        decrypted = self.decrypt_data(encrypted)
        article = json.load(decrypted)
        
        return article
    
    def store_intelligence(self, intel_data):
        """Store threat intelligence data"""
        intel_id = hashlib.md5(
            f"{intel_data.get('type', '')}{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        # Add metadata
        intel_data['stored_at'] = datetime.now().isoformat()
        intel_data['vault_id'] = intel_id
        
        # Encrypt
        encrypted = self.encrypt_data(json.dumps(intel_data))
        
        # Save
        intel_file = self.storage_dir / f"intel_{intel_id}.enc"
        with open(intel_file, 'w') as f:
            json.dump(encrypted, f)
        
        # Update index
        self.vault_index[intel_id] = {
            'type': 'intelligence',
            'category': intel_data.get('category', 'threat-intel'),
            'severity': intel_data.get('severity', 'medium'),
            'timestamp': intel_data['stored_at'],
            'file': str(intel_file),
            'tags': intel_data.get('tags', [])
        }
        
        self._save_index()
        
        self.logger.info(f"🔐 Intelligence stored: {intel_data.get('category', 'unknown')}")
        return intel_id
    
    def search(self, query=None, category=None, tags=None, days=30):
        """Search vault"""
        results = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for item_id, item_data in self.vault_index.items():
            # Date filter
            item_date = datetime.fromisoformat(item_data['timestamp'])
            if item_date < cutoff_date:
                continue
            
            # Category filter
            if category and item_data.get('category') != category:
                continue
            
            # Tags filter
            if tags:
                item_tags = set(item_data.get('tags', []))
                if not item_tags.intersection(set(tags)):
                    continue
            
            # Query filter
            if query:
                title = item_data.get('title', '').lower()
                if query.lower() not in title:
                    continue
            
            results.append({
                'id': item_id,
                **item_data
            })
        
        return sorted(results, key=lambda x: x['timestamp'], reverse=True)
    
    def get_recent(self, count=20, category=None):
        """Get recent items"""
        items = []
        
        for item_id, item_data in self.vault_index.items():
            if category and item_data.get('category') != category:
                continue
            
            items.append({
                'id': item_id,
                **item_data
            })
        
        # Sort by timestamp
        items.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return items[:count]
    
    def get_by_category(self, category):
        """Get all items in a category"""
        return [
            {'id': item_id, **item_data}
            for item_id, item_data in self.vault_index.items()
            if item_data.get('category') == category
        ]
    
    def get_statistics(self):
        """Get vault statistics"""
        stats = {
            'total_items': len(self.vault_index),
            'categories': {},
            'sources': {},
            'by_month': {}
        }
        
        for item_data in self.vault_index.values():
            # Category stats
            category = item_data.get('category', 'unknown')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            # Source stats
            source = item_data.get('source', 'unknown')
            stats['sources'][source] = stats['sources'].get(source, 0) + 1
            
            # Monthly stats
            timestamp = item_data.get('timestamp', '')
            if timestamp:
                month = timestamp[:7]  # YYYY-MM
                stats['by_month'][month] = stats['by_month'].get(month, 0) + 1
        
        return stats
    
    def cleanup_old(self, days=180):
        """Cleanup items older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        removed_count = 0
        
        items_to_remove = []
        
        for item_id, item_data in self.vault_index.items():
            item_date = datetime.fromisoformat(item_data['timestamp'])
            if item_date < cutoff_date:
                # Remove file
                item_file = Path(item_data['file'])
                if item_file.exists():
                    item_file.unlink()
                
                items_to_remove.append(item_id)
                removed_count += 1
        
        # Remove from index
        for item_id in items_to_remove:
            del self.vault_index[item_id]
        
        self._save_index()
        
        self.logger.info(f"🗑️  Cleaned up {removed_count} old items")
        return removed_count
    
    def _save_index(self):
        """Save vault index"""
        with open(self.index_file, 'w') as f:
            json.dump(self.vault_index, f, indent=2)
    
    def export_report(self, category=None, days=7):
        """Export vault report"""
        items = self.search(category=category, days=days)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'period_days': days,
            'category': category or 'all',
            'total_items': len(items),
            'items': items
        }
        
        report_file = self.vault_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"📊 Report exported: {report_file}")
        return str(report_file)
    
    def get_status(self):
        """Get vault status"""
        stats = self.get_statistics()
        
        return {
            'version': self.version,
            'total_items': stats['total_items'],
            'categories': len(stats['categories']),
            'sources': len(stats['sources']),
            'encrypted': True,
            'encryption': 'AES-256-GCM',
            'storage_path': str(self.storage_dir)
        }

if __name__ == '__main__':
    vault = NewsVault()
    
    print("\n" + "="*70)
    print("🔐 NEWS VAULT - STATUS")
    print("="*70)
    
    status = vault.get_status()
    print(f"Version: {status['version']}")
    print(f"Total Items: {status['total_items']}")
    print(f"Categories: {status['categories']}")
    print(f"Sources: {status['sources']}")
    print(f"Encryption: {status['encryption']}")
    print(f"Storage: {status['storage_path']}")
    
    print("="*70 + "\n")
