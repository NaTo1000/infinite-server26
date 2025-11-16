#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  NiA_VAULT - BRAIDED BLOCKCHAIN                                  ║
║  Encrypted Distributed Storage System                            ║
║  Version: 1.0 | Built by: NaTo1000                               ║
║                                                                   ║
║  Braided blockchain with quantum-resistant encryption            ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import hashlib
import threading
import logging
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

class Block:
    def __init__(self, index, timestamp, data, previous_hash, braid_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.braid_hash = braid_hash  # Connection to parallel chain
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate block hash"""
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.braid_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine block with proof of work"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class BraidedBlockchain:
    def __init__(self, chain_id=0):
        self.chain_id = chain_id
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 100
    
    def create_genesis_block(self):
        """Create genesis block"""
        return Block(0, datetime.now().isoformat(), "Genesis Block", "0")
    
    def get_latest_block(self):
        """Get latest block"""
        return self.chain[-1]
    
    def add_block(self, new_block):
        """Add block to chain"""
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        """Validate blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True

class NiAVault:
    def __init__(self):
        self.name = "NiA_Vault"
        self.version = "1.0"
        self.codename = "BRAIDED BLOCKCHAIN"
        self.running = True
        
        # Braided blockchain (3 parallel chains)
        self.chains = [
            BraidedBlockchain(chain_id=0),
            BraidedBlockchain(chain_id=1),
            BraidedBlockchain(chain_id=2)
        ]
        
        # Encryption
        self.master_key = None
        self.vault_password = None
        
        # Storage
        self.vault_path = '/opt/nia-vault/storage'
        self.encrypted_files = {}
        
        # Stats
        self.blocks_mined = 0
        self.files_encrypted = 0
        self.total_storage = 0
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [NiA_Vault] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('/var/log/nia-vault.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('NiA_Vault')
        
        # Create vault directory
        os.makedirs(self.vault_path, exist_ok=True)
        
        self.print_banner()
    
    def print_banner(self):
        """Display NiA_Vault banner"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🔐 NiA_VAULT - BRAIDED BLOCKCHAIN 🔐                            ║
║                                                                   ║
║   Version: {self.version}                                                    ║
║   Chains: {len(self.chains)} (Braided)                                           ║
║   Encryption: AES-256-GCM                                        ║
║   Status: ACTIVE                                                 ║
║                                                                   ║
║   "Your data, encrypted and distributed."                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
        print(banner)
        self.logger.info("NiA_Vault Braided Blockchain initialized")
    
    def initialize_vault(self, password):
        """Initialize vault with password"""
        self.logger.info("🔐 Initializing vault...")
        
        self.vault_password = password
        
        # Derive master key from password
        salt = get_random_bytes(32)
        self.master_key = PBKDF2(password, salt, dkLen=32, count=100000)
        
        # Save salt
        with open(f'{self.vault_path}/.salt', 'wb') as f:
            f.write(salt)
        
        self.logger.info("✅ Vault initialized")
    
    def encrypt_data(self, data):
        """Encrypt data with AES-256-GCM"""
        if not self.master_key:
            raise Exception("Vault not initialized")
        
        # Generate nonce
        nonce = get_random_bytes(16)
        
        # Create cipher
        cipher = AES.new(self.master_key, AES.MODE_GCM, nonce=nonce)
        
        # Encrypt
        ciphertext, tag = cipher.encrypt_and_digest(data.encode() if isinstance(data, str) else data)
        
        return {
            'nonce': nonce.hex(),
            'ciphertext': ciphertext.hex(),
            'tag': tag.hex()
        }
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data"""
        if not self.master_key:
            raise Exception("Vault not initialized")
        
        # Extract components
        nonce = bytes.fromhex(encrypted_data['nonce'])
        ciphertext = bytes.fromhex(encrypted_data['ciphertext'])
        tag = bytes.fromhex(encrypted_data['tag'])
        
        # Create cipher
        cipher = AES.new(self.master_key, AES.MODE_GCM, nonce=nonce)
        
        # Decrypt
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        
        return plaintext
    
    def store_file(self, filename, data):
        """Store file in vault"""
        self.logger.info(f"📁 Storing file: {filename}")
        
        # Encrypt data
        encrypted = self.encrypt_data(data)
        
        # Create block for each chain
        for i, chain in enumerate(self.chains):
            block_data = {
                'filename': filename,
                'timestamp': datetime.now().isoformat(),
                'size': len(data),
                'encrypted': encrypted if i == 0 else None,  # Only store in first chain
                'chain_id': i
            }
            
            new_block = Block(
                len(chain.chain),
                datetime.now().isoformat(),
                json.dumps(block_data),
                chain.get_latest_block().hash
            )
            
            # Braid with other chains
            if i < len(self.chains) - 1:
                new_block.braid_hash = self.chains[i+1].get_latest_block().hash
            
            chain.add_block(new_block)
            self.blocks_mined += 1
        
        # Save encrypted file
        file_path = os.path.join(self.vault_path, f"{filename}.encrypted")
        with open(file_path, 'w') as f:
            json.dump(encrypted, f)
        
        self.encrypted_files[filename] = file_path
        self.files_encrypted += 1
        self.total_storage += len(data)
        
        self.logger.info(f"✅ File stored: {filename}")
    
    def retrieve_file(self, filename):
        """Retrieve file from vault"""
        self.logger.info(f"📂 Retrieving file: {filename}")
        
        if filename not in self.encrypted_files:
            raise Exception(f"File not found: {filename}")
        
        # Load encrypted file
        with open(self.encrypted_files[filename], 'r') as f:
            encrypted = json.load(f)
        
        # Decrypt
        decrypted = self.decrypt_data(encrypted)
        
        self.logger.info(f"✅ File retrieved: {filename}")
        return decrypted
    
    def verify_integrity(self):
        """Verify blockchain integrity"""
        self.logger.info("🔍 Verifying blockchain integrity...")
        
        all_valid = True
        for i, chain in enumerate(self.chains):
            if chain.is_chain_valid():
                self.logger.info(f"✅ Chain {i} is valid")
            else:
                self.logger.error(f"❌ Chain {i} is INVALID")
                all_valid = False
        
        return all_valid
    
    def sync_chains(self):
        """Sync braided chains"""
        self.logger.info("🔄 Syncing braided chains...")
        
        # Ensure all chains have same length
        max_length = max(len(chain.chain) for chain in self.chains)
        
        for chain in self.chains:
            while len(chain.chain) < max_length:
                # Add empty block
                new_block = Block(
                    len(chain.chain),
                    datetime.now().isoformat(),
                    json.dumps({'type': 'sync_block'}),
                    chain.get_latest_block().hash
                )
                chain.add_block(new_block)
        
        self.logger.info("✅ Chains synced")
    
    def get_status(self):
        """Get vault status"""
        return {
            'name': self.name,
            'version': self.version,
            'chains': len(self.chains),
            'blocks_per_chain': [len(chain.chain) for chain in self.chains],
            'blocks_mined': self.blocks_mined,
            'files_encrypted': self.files_encrypted,
            'total_storage_bytes': self.total_storage,
            'vault_initialized': self.master_key is not None
        }
    
    def print_status(self):
        """Print vault status"""
        status = self.get_status()
        
        print("\n" + "="*70)
        print("🔐 NiA_VAULT BRAIDED BLOCKCHAIN - STATUS")
        print("="*70)
        print(f"Vault Initialized: {'YES' if status['vault_initialized'] else 'NO'}")
        print(f"Braided Chains: {status['chains']}")
        print(f"Blocks per Chain: {status['blocks_per_chain']}")
        print(f"Total Blocks Mined: {status['blocks_mined']}")
        print(f"Files Encrypted: {status['files_encrypted']}")
        print(f"Total Storage: {status['total_storage_bytes']} bytes")
        print("="*70 + "\n")
    
    def auto_sync(self):
        """Auto-sync chains periodically"""
        while self.running:
            try:
                self.sync_chains()
                self.verify_integrity()
                time.sleep(300)  # Sync every 5 minutes
            except Exception as e:
                self.logger.error(f"Auto-sync error: {e}")
                time.sleep(600)
    
    def start(self):
        """Start NiA_Vault"""
        self.logger.info("🚀 Starting NiA_Vault...")
        
        # Initialize vault with default password (should be changed)
        self.initialize_vault("nato1000_fortress_vault")
        
        # Start auto-sync thread
        sync_thread = threading.Thread(target=self.auto_sync, daemon=True)
        sync_thread.start()
        
        self.logger.info("✅ NiA_Vault active")
        
        # Status reporting loop
        try:
            while self.running:
                time.sleep(300)  # Print status every 5 minutes
                self.print_status()
        except KeyboardInterrupt:
            self.logger.info("⏹️  Shutting down NiA_Vault...")
            self.running = False
            sys.exit(0)

if __name__ == '__main__':
    vault = NiAVault()
    vault.start()
