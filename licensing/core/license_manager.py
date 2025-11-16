#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - LICENSE MANAGER                             ║
║  SHA-512 License Key Generation & Validation                     ║
║  Version: 1.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import logging
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

class LicenseManager:
    def __init__(self):
        self.name = "LicenseManager"
        self.version = "1.0"
        self.license_dir = Path('/opt/infinite-server26/licensing')
        self.license_db = self.license_dir / 'licenses.json'
        self.master_secret = os.getenv('LICENSE_MASTER_SECRET', 'nato1000_infinite_server26_master_secret')
        
        # License configuration
        self.license_validity_days = 30  # 30 days per billing cycle
        self.hash_algorithm = 'sha512'  # SHA-512 (512 bits = 64 bytes = 128 hex chars)
        
        # License database
        self.licenses = {}
        
        # Setup directories
        self.license_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [LicenseManager] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/license-manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('LicenseManager')
        
        # Load existing licenses
        self._load_licenses()
        
        self.logger.info("License Manager initialized")
    
    def generate_license(self, customer_id, subscription_id, email=None):
        """Generate SHA-512 license key"""
        try:
            self.logger.info(f"🔑 Generating license for customer: {customer_id}")
            
            # Generate unique license data
            timestamp = datetime.now().isoformat()
            random_salt = secrets.token_hex(32)  # 32 bytes = 64 hex chars
            
            # Create license payload
            license_payload = f"{customer_id}:{subscription_id}:{timestamp}:{random_salt}"
            
            # Generate SHA-512 hash
            license_hash = hashlib.sha512(license_payload.encode()).hexdigest()
            
            # Create HMAC signature for additional security
            hmac_signature = hmac.new(
                self.master_secret.encode(),
                license_hash.encode(),
                hashlib.sha512
            ).hexdigest()
            
            # Combine hash and signature (128 + 128 = 256 hex chars total)
            full_license_key = f"{license_hash}{hmac_signature}"
            
            # Format license key (add dashes for readability)
            formatted_key = self._format_license_key(full_license_key)
            
            # Calculate expiration
            expiration = datetime.now() + timedelta(days=self.license_validity_days)
            
            # Store license
            license_data = {
                'license_key': formatted_key,
                'customer_id': customer_id,
                'subscription_id': subscription_id,
                'email': email,
                'generated_at': timestamp,
                'expires_at': expiration.isoformat(),
                'status': 'active',
                'activations': 0,
                'max_activations': 1,  # Single server license
                'hash_algorithm': self.hash_algorithm,
                'version': self.version
            }
            
            self.licenses[formatted_key] = license_data
            self._save_licenses()
            
            self.logger.info(f"✅ License generated: {formatted_key[:32]}...")
            return formatted_key
            
        except Exception as e:
            self.logger.error(f"❌ License generation failed: {e}")
            return None
    
    def _format_license_key(self, key):
        """Format license key with dashes for readability"""
        # Split into groups of 16 characters
        groups = [key[i:i+16] for i in range(0, len(key), 16)]
        return '-'.join(groups)
    
    def _unformat_license_key(self, formatted_key):
        """Remove dashes from formatted key"""
        return formatted_key.replace('-', '')
    
    def validate_license(self, license_key):
        """Validate license key"""
        try:
            self.logger.info(f"🔍 Validating license: {license_key[:32]}...")
            
            # Check if license exists
            if license_key not in self.licenses:
                self.logger.warning(f"❌ License not found: {license_key[:32]}...")
                return {
                    'valid': False,
                    'reason': 'License key not found'
                }
            
            license_data = self.licenses[license_key]
            
            # Check status
            if license_data['status'] != 'active':
                self.logger.warning(f"❌ License inactive: {license_key[:32]}...")
                return {
                    'valid': False,
                    'reason': f"License status: {license_data['status']}"
                }
            
            # Check expiration
            expiration = datetime.fromisoformat(license_data['expires_at'])
            if datetime.now() > expiration:
                self.logger.warning(f"❌ License expired: {license_key[:32]}...")
                license_data['status'] = 'expired'
                self._save_licenses()
                return {
                    'valid': False,
                    'reason': 'License expired'
                }
            
            # Check activations
            if license_data['activations'] >= license_data['max_activations']:
                self.logger.warning(f"❌ License max activations reached: {license_key[:32]}...")
                return {
                    'valid': False,
                    'reason': 'Maximum activations reached'
                }
            
            # Verify HMAC signature
            unformatted_key = self._unformat_license_key(license_key)
            license_hash = unformatted_key[:128]  # First 128 chars (SHA-512)
            provided_signature = unformatted_key[128:]  # Last 128 chars (HMAC)
            
            expected_signature = hmac.new(
                self.master_secret.encode(),
                license_hash.encode(),
                hashlib.sha512
            ).hexdigest()
            
            if provided_signature != expected_signature:
                self.logger.error(f"❌ License signature invalid: {license_key[:32]}...")
                return {
                    'valid': False,
                    'reason': 'Invalid license signature'
                }
            
            self.logger.info(f"✅ License valid: {license_key[:32]}...")
            return {
                'valid': True,
                'license_data': license_data
            }
            
        except Exception as e:
            self.logger.error(f"❌ License validation failed: {e}")
            return {
                'valid': False,
                'reason': f'Validation error: {str(e)}'
            }
    
    def activate_license(self, license_key, server_id=None):
        """Activate license on a server"""
        try:
            self.logger.info(f"🔓 Activating license: {license_key[:32]}...")
            
            # Validate license first
            validation = self.validate_license(license_key)
            if not validation['valid']:
                return validation
            
            license_data = self.licenses[license_key]
            
            # Check if already activated
            if license_data['activations'] >= license_data['max_activations']:
                return {
                    'valid': False,
                    'reason': 'License already activated on maximum servers'
                }
            
            # Activate
            license_data['activations'] += 1
            license_data['activated_at'] = datetime.now().isoformat()
            if server_id:
                license_data['server_id'] = server_id
            
            self._save_licenses()
            
            self.logger.info(f"✅ License activated: {license_key[:32]}...")
            return {
                'valid': True,
                'activated': True,
                'license_data': license_data
            }
            
        except Exception as e:
            self.logger.error(f"❌ License activation failed: {e}")
            return {
                'valid': False,
                'reason': f'Activation error: {str(e)}'
            }
    
    def deactivate_license(self, license_key):
        """Deactivate license"""
        try:
            self.logger.info(f"🔒 Deactivating license: {license_key[:32]}...")
            
            if license_key not in self.licenses:
                return False
            
            license_data = self.licenses[license_key]
            
            if license_data['activations'] > 0:
                license_data['activations'] -= 1
            
            license_data['deactivated_at'] = datetime.now().isoformat()
            
            self._save_licenses()
            
            self.logger.info(f"✅ License deactivated: {license_key[:32]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ License deactivation failed: {e}")
            return False
    
    def revoke_license(self, license_key):
        """Revoke license"""
        try:
            self.logger.info(f"❌ Revoking license: {license_key[:32]}...")
            
            if license_key not in self.licenses:
                return False
            
            self.licenses[license_key]['status'] = 'revoked'
            self.licenses[license_key]['revoked_at'] = datetime.now().isoformat()
            
            self._save_licenses()
            
            self.logger.info(f"✅ License revoked: {license_key[:32]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ License revocation failed: {e}")
            return False
    
    def revoke_license_by_subscription(self, subscription_id):
        """Revoke license by subscription ID"""
        try:
            self.logger.info(f"❌ Revoking license for subscription: {subscription_id}")
            
            for license_key, license_data in self.licenses.items():
                if license_data.get('subscription_id') == subscription_id:
                    license_data['status'] = 'revoked'
                    license_data['revoked_at'] = datetime.now().isoformat()
                    self.logger.info(f"✅ License revoked: {license_key[:32]}...")
            
            self._save_licenses()
            return True
            
        except Exception as e:
            self.logger.error(f"❌ License revocation failed: {e}")
            return False
    
    def renew_license(self, license_key):
        """Renew license (extend expiration)"""
        try:
            self.logger.info(f"🔄 Renewing license: {license_key[:32]}...")
            
            if license_key not in self.licenses:
                return False
            
            license_data = self.licenses[license_key]
            
            # Extend expiration by 30 days
            current_expiration = datetime.fromisoformat(license_data['expires_at'])
            new_expiration = current_expiration + timedelta(days=self.license_validity_days)
            
            license_data['expires_at'] = new_expiration.isoformat()
            license_data['renewed_at'] = datetime.now().isoformat()
            license_data['status'] = 'active'
            
            self._save_licenses()
            
            self.logger.info(f"✅ License renewed: {license_key[:32]}... (expires: {new_expiration.date()})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ License renewal failed: {e}")
            return False
    
    def get_license_info(self, license_key):
        """Get license information"""
        if license_key not in self.licenses:
            return None
        
        return self.licenses[license_key]
    
    def list_licenses(self, status=None):
        """List all licenses"""
        if status:
            return {
                k: v for k, v in self.licenses.items()
                if v.get('status') == status
            }
        return self.licenses
    
    def get_statistics(self):
        """Get license statistics"""
        stats = {
            'total_licenses': len(self.licenses),
            'active': 0,
            'expired': 0,
            'revoked': 0,
            'suspended': 0
        }
        
        for license_data in self.licenses.values():
            status = license_data.get('status', 'unknown')
            if status in stats:
                stats[status] += 1
        
        return stats
    
    def _load_licenses(self):
        """Load licenses from database"""
        if self.license_db.exists():
            try:
                with open(self.license_db, 'r') as f:
                    self.licenses = json.load(f)
                self.logger.info(f"📂 Loaded {len(self.licenses)} licenses")
            except Exception as e:
                self.logger.error(f"❌ Failed to load licenses: {e}")
                self.licenses = {}
    
    def _save_licenses(self):
        """Save licenses to database"""
        try:
            with open(self.license_db, 'w') as f:
                json.dump(self.licenses, f, indent=2)
            self.logger.info(f"💾 Saved {len(self.licenses)} licenses")
        except Exception as e:
            self.logger.error(f"❌ Failed to save licenses: {e}")
    
    def get_status(self):
        """Get license manager status"""
        stats = self.get_statistics()
        
        return {
            'version': self.version,
            'hash_algorithm': self.hash_algorithm,
            'license_validity_days': self.license_validity_days,
            'total_licenses': stats['total_licenses'],
            'active_licenses': stats['active'],
            'expired_licenses': stats['expired'],
            'revoked_licenses': stats['revoked']
        }

if __name__ == '__main__':
    manager = LicenseManager()
    
    print("\n" + "="*70)
    print("🔑 LICENSE MANAGER - STATUS")
    print("="*70)
    
    status = manager.get_status()
    print(f"Version: {status['version']}")
    print(f"Hash Algorithm: {status['hash_algorithm'].upper()}")
    print(f"License Validity: {status['license_validity_days']} days")
    print(f"Total Licenses: {status['total_licenses']}")
    print(f"Active: {status['active_licenses']}")
    print(f"Expired: {status['expired_licenses']}")
    print(f"Revoked: {status['revoked_licenses']}")
    
    print("="*70 + "\n")
    
    # Demo: Generate a test license
    print("🔑 Generating test license...")
    test_license = manager.generate_license(
        customer_id='cus_test123',
        subscription_id='sub_test456',
        email='test@example.com'
    )
    
    if test_license:
        print(f"✅ Test License Generated:")
        print(f"   {test_license}")
        print(f"   Length: {len(test_license.replace('-', ''))} characters (256 hex chars = 1024 bits)")
        
        # Validate
        print("\n🔍 Validating test license...")
        validation = manager.validate_license(test_license)
        print(f"   Valid: {validation['valid']}")
        
        if validation['valid']:
            # Activate
            print("\n🔓 Activating test license...")
            activation = manager.activate_license(test_license, server_id='server_001')
            print(f"   Activated: {activation.get('activated', False)}")
