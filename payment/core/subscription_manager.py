#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - SUBSCRIPTION MANAGER                        ║
║  Auto-Renewal & Subscription Management                          ║
║  Version: 1.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import sys
import json
import logging
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add paths
sys.path.insert(0, '/opt/infinite-server26')

class SubscriptionManager:
    def __init__(self):
        self.name = "SubscriptionManager"
        self.version = "1.0"
        self.subscription_dir = Path('/opt/infinite-server26/payment')
        self.subscription_db = self.subscription_dir / 'subscriptions.json'
        
        # Subscription configuration
        self.check_interval = 3600  # Check every hour
        self.renewal_grace_period = 3  # 3 days grace period
        self.running = False
        
        # Subscription database
        self.subscriptions = {}
        
        # Setup directories
        self.subscription_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [SubscriptionManager] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/subscription-manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SubscriptionManager')
        
        # Load existing subscriptions
        self._load_subscriptions()
        
        self.logger.info("Subscription Manager initialized")
    
    def add_subscription(self, customer_id, subscription_id, license_key, email=None):
        """Add new subscription"""
        try:
            self.logger.info(f"➕ Adding subscription: {subscription_id}")
            
            subscription_data = {
                'customer_id': customer_id,
                'subscription_id': subscription_id,
                'license_key': license_key,
                'email': email,
                'status': 'active',
                'created_at': datetime.now().isoformat(),
                'current_period_start': datetime.now().isoformat(),
                'current_period_end': (datetime.now() + timedelta(days=30)).isoformat(),
                'auto_renew': True,
                'payment_failures': 0,
                'last_checked': datetime.now().isoformat()
            }
            
            self.subscriptions[subscription_id] = subscription_data
            self._save_subscriptions()
            
            self.logger.info(f"✅ Subscription added: {subscription_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to add subscription: {e}")
            return False
    
    def update_subscription(self, subscription_id, **kwargs):
        """Update subscription"""
        try:
            if subscription_id not in self.subscriptions:
                self.logger.warning(f"⚠️  Subscription not found: {subscription_id}")
                return False
            
            self.logger.info(f"🔄 Updating subscription: {subscription_id}")
            
            for key, value in kwargs.items():
                self.subscriptions[subscription_id][key] = value
            
            self.subscriptions[subscription_id]['updated_at'] = datetime.now().isoformat()
            self._save_subscriptions()
            
            self.logger.info(f"✅ Subscription updated: {subscription_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update subscription: {e}")
            return False
    
    def cancel_subscription(self, subscription_id):
        """Cancel subscription"""
        try:
            if subscription_id not in self.subscriptions:
                self.logger.warning(f"⚠️  Subscription not found: {subscription_id}")
                return False
            
            self.logger.info(f"❌ Canceling subscription: {subscription_id}")
            
            self.subscriptions[subscription_id]['status'] = 'canceled'
            self.subscriptions[subscription_id]['canceled_at'] = datetime.now().isoformat()
            self.subscriptions[subscription_id]['auto_renew'] = False
            
            # Revoke license
            license_key = self.subscriptions[subscription_id].get('license_key')
            if license_key:
                from licensing.core.license_manager import LicenseManager
                license_mgr = LicenseManager()
                license_mgr.revoke_license(license_key)
            
            self._save_subscriptions()
            
            self.logger.info(f"✅ Subscription canceled: {subscription_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to cancel subscription: {e}")
            return False
    
    def renew_subscription(self, subscription_id):
        """Renew subscription"""
        try:
            if subscription_id not in self.subscriptions:
                self.logger.warning(f"⚠️  Subscription not found: {subscription_id}")
                return False
            
            self.logger.info(f"🔄 Renewing subscription: {subscription_id}")
            
            subscription = self.subscriptions[subscription_id]
            
            # Update period
            current_end = datetime.fromisoformat(subscription['current_period_end'])
            new_end = current_end + timedelta(days=30)
            
            subscription['current_period_start'] = current_end.isoformat()
            subscription['current_period_end'] = new_end.isoformat()
            subscription['renewed_at'] = datetime.now().isoformat()
            subscription['status'] = 'active'
            subscription['payment_failures'] = 0
            
            # Renew license
            license_key = subscription.get('license_key')
            if license_key:
                from licensing.core.license_manager import LicenseManager
                license_mgr = LicenseManager()
                license_mgr.renew_license(license_key)
            
            self._save_subscriptions()
            
            self.logger.info(f"✅ Subscription renewed: {subscription_id} (expires: {new_end.date()})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to renew subscription: {e}")
            return False
    
    def handle_payment_failure(self, subscription_id):
        """Handle payment failure"""
        try:
            if subscription_id not in self.subscriptions:
                return False
            
            self.logger.warning(f"⚠️  Payment failure for subscription: {subscription_id}")
            
            subscription = self.subscriptions[subscription_id]
            subscription['payment_failures'] = subscription.get('payment_failures', 0) + 1
            subscription['last_payment_failure'] = datetime.now().isoformat()
            
            # If too many failures, suspend subscription
            if subscription['payment_failures'] >= 3:
                self.logger.error(f"❌ Too many payment failures, suspending: {subscription_id}")
                subscription['status'] = 'suspended'
                
                # Revoke license
                license_key = subscription.get('license_key')
                if license_key:
                    from licensing.core.license_manager import LicenseManager
                    license_mgr = LicenseManager()
                    license_mgr.revoke_license(license_key)
            
            self._save_subscriptions()
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to handle payment failure: {e}")
            return False
    
    def check_expiring_subscriptions(self):
        """Check for expiring subscriptions"""
        try:
            self.logger.info("🔍 Checking for expiring subscriptions...")
            
            expiring_soon = []
            now = datetime.now()
            
            for sub_id, subscription in self.subscriptions.items():
                if subscription['status'] != 'active':
                    continue
                
                period_end = datetime.fromisoformat(subscription['current_period_end'])
                days_until_expiry = (period_end - now).days
                
                # Check if expiring within grace period
                if 0 <= days_until_expiry <= self.renewal_grace_period:
                    expiring_soon.append({
                        'subscription_id': sub_id,
                        'days_until_expiry': days_until_expiry,
                        'email': subscription.get('email'),
                        'customer_id': subscription.get('customer_id')
                    })
                    
                    self.logger.warning(f"⚠️  Subscription expiring in {days_until_expiry} days: {sub_id}")
                
                # Check if already expired
                elif days_until_expiry < 0:
                    self.logger.error(f"❌ Subscription expired: {sub_id}")
                    subscription['status'] = 'expired'
                    
                    # Revoke license
                    license_key = subscription.get('license_key')
                    if license_key:
                        from licensing.core.license_manager import LicenseManager
                        license_mgr = LicenseManager()
                        license_mgr.revoke_license(license_key)
            
            if expiring_soon:
                self.logger.info(f"⚠️  Found {len(expiring_soon)} expiring subscriptions")
            else:
                self.logger.info("✅ No expiring subscriptions")
            
            self._save_subscriptions()
            return expiring_soon
            
        except Exception as e:
            self.logger.error(f"❌ Failed to check expiring subscriptions: {e}")
            return []
    
    def auto_renew_subscriptions(self):
        """Auto-renew subscriptions"""
        try:
            self.logger.info("🔄 Processing auto-renewals...")

            upcoming_count = 0

            for sub_id, subscription in self.subscriptions.items():
                if subscription['status'] != 'active':
                    continue

                if not subscription.get('auto_renew', True):
                    continue

                period_end = datetime.fromisoformat(subscription['current_period_end'])
                days_until_expiry = (period_end - datetime.now()).days

                # Log subscriptions renewing tomorrow; Stripe handles billing automatically.
                if days_until_expiry == 1:
                    self.logger.info(f"⏰ Subscription renewing tomorrow (Stripe will charge): {sub_id}")
                    upcoming_count += 1

            if upcoming_count > 0:
                self.logger.info(f"ℹ️  {upcoming_count} subscription(s) renewing tomorrow via Stripe")
            else:
                self.logger.info("ℹ️  No subscriptions renewing tomorrow")

            return upcoming_count
            
        except Exception as e:
            self.logger.error(f"❌ Failed to auto-renew subscriptions: {e}")
            return 0
    
    def start_monitoring(self):
        """Start subscription monitoring"""
        self.logger.info("👁️  Starting subscription monitoring...")
        
        self.running = True
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        
        self.logger.info("✅ Subscription monitoring started")
    
    def stop_monitoring(self):
        """Stop subscription monitoring"""
        self.logger.info("⏹️  Stopping subscription monitoring...")
        self.running = False
    
    def _monitoring_loop(self):
        """Monitoring loop"""
        while self.running:
            try:
                self.logger.info("🔄 Running subscription checks...")
                
                # Check expiring subscriptions
                self.check_expiring_subscriptions()
                
                # Process auto-renewals
                self.auto_renew_subscriptions()
                
                # Update last checked time
                for subscription in self.subscriptions.values():
                    subscription['last_checked'] = datetime.now().isoformat()
                
                self._save_subscriptions()
                
                # Sleep for check interval
                time.sleep(self.check_interval)
                
            except Exception as e:
                self.logger.error(f"❌ Monitoring loop error: {e}")
                time.sleep(self.check_interval)
    
    def get_subscription(self, subscription_id):
        """Get subscription"""
        return self.subscriptions.get(subscription_id)
    
    def list_subscriptions(self, status=None):
        """List subscriptions"""
        if status:
            return {
                k: v for k, v in self.subscriptions.items()
                if v.get('status') == status
            }
        return self.subscriptions
    
    def get_statistics(self):
        """Get subscription statistics"""
        stats = {
            'total_subscriptions': len(self.subscriptions),
            'active': 0,
            'canceled': 0,
            'expired': 0,
            'suspended': 0,
            'total_revenue_monthly': 0
        }
        
        for subscription in self.subscriptions.values():
            status = subscription.get('status', 'unknown')
            if status in stats:
                stats[status] += 1
            
            if status == 'active':
                stats['total_revenue_monthly'] += 25.00  # $25/month
        
        return stats
    
    def _load_subscriptions(self):
        """Load subscriptions from database"""
        if self.subscription_db.exists():
            try:
                with open(self.subscription_db, 'r') as f:
                    self.subscriptions = json.load(f)
                self.logger.info(f"📂 Loaded {len(self.subscriptions)} subscriptions")
            except Exception as e:
                self.logger.error(f"❌ Failed to load subscriptions: {e}")
                self.subscriptions = {}
    
    def _save_subscriptions(self):
        """Save subscriptions to database"""
        try:
            with open(self.subscription_db, 'w') as f:
                json.dump(self.subscriptions, f, indent=2)
            self.logger.info(f"💾 Saved {len(self.subscriptions)} subscriptions")
        except Exception as e:
            self.logger.error(f"❌ Failed to save subscriptions: {e}")
    
    def get_status(self):
        """Get subscription manager status"""
        stats = self.get_statistics()
        
        return {
            'version': self.version,
            'running': self.running,
            'check_interval': f"{self.check_interval}s",
            'grace_period': f"{self.renewal_grace_period} days",
            'total_subscriptions': stats['total_subscriptions'],
            'active_subscriptions': stats['active'],
            'monthly_revenue': f"${stats['total_revenue_monthly']:.2f}"
        }

if __name__ == '__main__':
    manager = SubscriptionManager()
    
    print("\n" + "="*70)
    print("📊 SUBSCRIPTION MANAGER - STATUS")
    print("="*70)
    
    status = manager.get_status()
    print(f"Version: {status['version']}")
    print(f"Running: {status['running']}")
    print(f"Check Interval: {status['check_interval']}")
    print(f"Grace Period: {status['grace_period']}")
    print(f"Total Subscriptions: {status['total_subscriptions']}")
    print(f"Active Subscriptions: {status['active_subscriptions']}")
    print(f"Monthly Revenue: {status['monthly_revenue']}")
    
    print("="*70 + "\n")
    
    # Start monitoring
    print("👁️  Starting subscription monitoring...")
    manager.start_monitoring()
    
    print("Press Ctrl+C to stop...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.stop_monitoring()
