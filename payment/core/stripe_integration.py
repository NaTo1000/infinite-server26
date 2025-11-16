#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  INFINITE SERVER26 - STRIPE PAYMENT INTEGRATION                  ║
║  $25/Month Subscription System                                   ║
║  Version: 1.0 | Built by: NaTo1000                               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import logging
import hashlib
import hmac
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

# Stripe SDK (install with: pip3 install stripe)
try:
    import stripe
except ImportError:
    print("⚠️  Stripe SDK not installed. Run: pip3 install stripe")
    stripe = None

class StripePaymentSystem:
    def __init__(self):
        self.name = "StripePaymentSystem"
        self.version = "1.0"
        self.payment_dir = Path('/opt/infinite-server26/payment')
        self.config_file = self.payment_dir / 'stripe_config.json'
        
        # Stripe configuration
        self.stripe_api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_YOUR_KEY_HERE')
        self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_YOUR_KEY_HERE')
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_YOUR_SECRET_HERE')
        
        # Subscription configuration
        self.subscription_price = 25.00  # USD
        self.currency = 'usd'
        self.billing_period = 'month'
        self.product_name = 'Infinite Server26 License'
        self.product_description = 'Monthly subscription for Infinite Server26 security fortress'
        
        # Setup directories
        self.payment_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [StripePayment] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/stripe-payment.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('StripePayment')
        
        # Initialize Stripe
        if stripe:
            stripe.api_key = self.stripe_api_key
        
        self.logger.info("Stripe Payment System initialized")
    
    def create_product(self):
        """Create Stripe product"""
        if not stripe:
            self.logger.error("Stripe SDK not available")
            return None
        
        try:
            self.logger.info("📦 Creating Stripe product...")
            
            # Create product
            product = stripe.Product.create(
                name=self.product_name,
                description=self.product_description,
                metadata={
                    'version': self.version,
                    'system': 'infinite-server26'
                }
            )
            
            self.logger.info(f"✅ Product created: {product.id}")
            return product
            
        except Exception as e:
            self.logger.error(f"❌ Product creation failed: {e}")
            return None
    
    def create_price(self, product_id):
        """Create Stripe price"""
        if not stripe:
            self.logger.error("Stripe SDK not available")
            return None
        
        try:
            self.logger.info("💰 Creating Stripe price...")
            
            # Create price
            price = stripe.Price.create(
                product=product_id,
                unit_amount=int(self.subscription_price * 100),  # Convert to cents
                currency=self.currency,
                recurring={
                    'interval': self.billing_period
                },
                metadata={
                    'version': self.version
                }
            )
            
            self.logger.info(f"✅ Price created: {price.id} (${self.subscription_price}/{self.billing_period})")
            return price
            
        except Exception as e:
            self.logger.error(f"❌ Price creation failed: {e}")
            return None
    
    def create_customer(self, email, name=None, metadata=None):
        """Create Stripe customer"""
        if not stripe:
            self.logger.error("Stripe SDK not available")
            return None
        
        try:
            self.logger.info(f"👤 Creating customer: {email}")
            
            customer_data = {
                'email': email,
                'metadata': metadata or {}
            }
            
            if name:
                customer_data['name'] = name
            
            customer = stripe.Customer.create(**customer_data)
            
            self.logger.info(f"✅ Customer created: {customer.id}")
            return customer
            
        except Exception as e:
            self.logger.error(f"❌ Customer creation failed: {e}")
            return None
    
    def create_subscription(self, customer_id, price_id):
        """Create Stripe subscription"""
        if not stripe:
            self.logger.error("Stripe SDK not available")
            return None
        
        try:
            self.logger.info(f"📝 Creating subscription for customer: {customer_id}")
            
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['latest_invoice.payment_intent'],
                metadata={
                    'system': 'infinite-server26',
                    'version': self.version
                }
            )
            
            self.logger.info(f"✅ Subscription created: {subscription.id}")
            return subscription
            
        except Exception as e:
            self.logger.error(f"❌ Subscription creation failed: {e}")
            return None
    
    def create_checkout_session(self, price_id, success_url, cancel_url, customer_email=None):
        """Create Stripe Checkout session"""
        if not stripe:
            self.logger.error("Stripe SDK not available")
            return None
        
        try:
            self.logger.info("🛒 Creating Checkout session...")
            
            session_data = {
                'mode': 'subscription',
                'line_items': [{
                    'price': price_id,
                    'quantity': 1,
                }],
                'success_url': success_url,
                'cancel_url': cancel_url,
                'metadata': {
                    'system': 'infinite-server26'
                }
            }
            
            if customer_email:
                session_data['customer_email'] = customer_email
            
            session = stripe.checkout.Session.create(**session_data)
            
            self.logger.info(f"✅ Checkout session created: {session.id}")
            return session
            
        except Exception as e:
            self.logger.error(f"❌ Checkout session creation failed: {e}")
            return None
    
    def cancel_subscription(self, subscription_id):
        """Cancel Stripe subscription"""
        if not stripe:
            self.logger.error("Stripe SDK not available")
            return False
        
        try:
            self.logger.info(f"❌ Canceling subscription: {subscription_id}")
            
            subscription = stripe.Subscription.delete(subscription_id)
            
            self.logger.info(f"✅ Subscription canceled: {subscription_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Subscription cancellation failed: {e}")
            return False
    
    def get_subscription(self, subscription_id):
        """Get Stripe subscription"""
        if not stripe:
            self.logger.error("Stripe SDK not available")
            return None
        
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return subscription
            
        except Exception as e:
            self.logger.error(f"❌ Subscription retrieval failed: {e}")
            return None
    
    def get_customer(self, customer_id):
        """Get Stripe customer"""
        if not stripe:
            self.logger.error("Stripe SDK not available")
            return None
        
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return customer
            
        except Exception as e:
            self.logger.error(f"❌ Customer retrieval failed: {e}")
            return None
    
    def verify_webhook_signature(self, payload, signature):
        """Verify Stripe webhook signature"""
        if not stripe:
            self.logger.error("Stripe SDK not available")
            return False
        
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            return event
            
        except ValueError as e:
            self.logger.error(f"❌ Invalid payload: {e}")
            return None
        except stripe.error.SignatureVerificationError as e:
            self.logger.error(f"❌ Invalid signature: {e}")
            return None
    
    def handle_webhook_event(self, event):
        """Handle Stripe webhook event"""
        event_type = event['type']
        
        self.logger.info(f"📨 Webhook event: {event_type}")
        
        if event_type == 'customer.subscription.created':
            return self._handle_subscription_created(event)
        elif event_type == 'customer.subscription.updated':
            return self._handle_subscription_updated(event)
        elif event_type == 'customer.subscription.deleted':
            return self._handle_subscription_deleted(event)
        elif event_type == 'invoice.payment_succeeded':
            return self._handle_payment_succeeded(event)
        elif event_type == 'invoice.payment_failed':
            return self._handle_payment_failed(event)
        else:
            self.logger.info(f"ℹ️  Unhandled event type: {event_type}")
            return True
    
    def _handle_subscription_created(self, event):
        """Handle subscription created event"""
        subscription = event['data']['object']
        customer_id = subscription['customer']
        subscription_id = subscription['id']
        
        self.logger.info(f"✅ Subscription created: {subscription_id} for customer: {customer_id}")
        
        # Generate license key
        from licensing.core.license_manager import LicenseManager
        license_mgr = LicenseManager()
        license_key = license_mgr.generate_license(
            customer_id=customer_id,
            subscription_id=subscription_id
        )
        
        self.logger.info(f"🔑 License key generated: {license_key[:16]}...")
        
        return True
    
    def _handle_subscription_updated(self, event):
        """Handle subscription updated event"""
        subscription = event['data']['object']
        subscription_id = subscription['id']
        status = subscription['status']
        
        self.logger.info(f"🔄 Subscription updated: {subscription_id} - Status: {status}")
        
        return True
    
    def _handle_subscription_deleted(self, event):
        """Handle subscription deleted event"""
        subscription = event['data']['object']
        subscription_id = subscription['id']
        
        self.logger.info(f"❌ Subscription deleted: {subscription_id}")
        
        # Revoke license
        from licensing.core.license_manager import LicenseManager
        license_mgr = LicenseManager()
        license_mgr.revoke_license_by_subscription(subscription_id)
        
        return True
    
    def _handle_payment_succeeded(self, event):
        """Handle payment succeeded event"""
        invoice = event['data']['object']
        customer_id = invoice['customer']
        amount = invoice['amount_paid'] / 100  # Convert from cents
        
        self.logger.info(f"💰 Payment succeeded: ${amount} from customer: {customer_id}")
        
        return True
    
    def _handle_payment_failed(self, event):
        """Handle payment failed event"""
        invoice = event['data']['object']
        customer_id = invoice['customer']
        
        self.logger.error(f"❌ Payment failed for customer: {customer_id}")
        
        return True
    
    def get_status(self):
        """Get payment system status"""
        return {
            'version': self.version,
            'subscription_price': f"${self.subscription_price}",
            'billing_period': self.billing_period,
            'currency': self.currency,
            'stripe_configured': bool(stripe and self.stripe_api_key != 'sk_test_YOUR_KEY_HERE')
        }

if __name__ == '__main__':
    payment = StripePaymentSystem()
    
    print("\n" + "="*70)
    print("💳 STRIPE PAYMENT SYSTEM - STATUS")
    print("="*70)
    
    status = payment.get_status()
    print(f"Version: {status['version']}")
    print(f"Subscription Price: {status['subscription_price']}/{status['billing_period']}")
    print(f"Currency: {status['currency'].upper()}")
    print(f"Stripe Configured: {status['stripe_configured']}")
    
    print("="*70 + "\n")
