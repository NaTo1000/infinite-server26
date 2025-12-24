#!/usr/bin/env python3

"""
╔═══════════════════════════════════════════════════════════════════╗
║  NiA_VAULT - BRAIDED BLOCKCHAIN                                  ║
║  Encrypted Distributed Storage System (Rewritten)                ║
║  Version: 26.2 | Built by: NaTo1000                              ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import sys
import time
import json
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Conditional imports for crypto
try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Protocol.KDF import PBKDF2
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.utils import ComponentBase, print_banner


class Block:
    """Blockchain block"""
    
    def __init__(self, index: int, timestamp: str, data: str, previous_hash: str, braid_hash: str = ''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.braid_hash = braid_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash"""
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.braid_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """Mine block with proof of work"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


class BraidedBlockchain:
    """Single blockchain in the braided system"""
    
    def __init__(self, chain_id: int, difficulty: int = 4):
        self.chain_id = chain_id
        self.chain = [self._create_genesis_block()]
        self.difficulty = difficulty
    
    def _create_genesis_block(self) -> Block:
        """Create genesis block"""
        return Block(0, datetime.now().isoformat(), "Genesis Block", "0")
    
    def get_latest_block(self) -> Block:
        """Get latest block"""
        return self.chain[-1]
    
    def add_block(self, new_block: Block):
        """Add block to chain"""
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
    
    def is_valid(self) -> bool:
        """Validate blockchain"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != current.calculate_hash():
                return False
            
            if current.previous_hash != previous.hash:
                return False
        
        return True


class NiAVault(ComponentBase):
    """Braided blockchain storage system"""
    
    def __init__(self):
        super().__init__("NiA_Vault", "26.2")
        
        if not CRYPTO_AVAILABLE:
            self.logger.warning("⚠️  Crypto library not available, encryption disabled")
        
        # Configuration
        num_chains = self.config.get('blockchain.nia_vault.chains', 3)
        difficulty = self.config.get('blockchain.nia_vault.difficulty', 4)
        self.storage_dir = self.paths.get_path('storage') / 'blockchain'
        self.sync_interval = self.config.get('blockchain.nia_vault.auto_sync_interval', 300)
        
        # Create storage directory
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Braided blockchain
        self.chains = [
            BraidedBlockchain(chain_id=i, difficulty=difficulty)
            for i in range(num_chains)
        ]
        
        # Encryption
        self.master_key: Optional[bytes] = None
        
        # Stats
        self.blocks_mined = 0
        self.files_encrypted = 0
        
        print_banner("NiA_VAULT - BRAIDED BLOCKCHAIN")
        self.logger.info(f"Initialized with {num_chains} braided chains")
    
    def initialize_vault(self, password: str):
        """Initialize vault with password"""
        if not CRYPTO_AVAILABLE:
            self.logger.error("Cannot initialize vault without crypto library")
            return False
        
        self.logger.info("🔐 Initializing vault...")
        
        try:
            # Derive master key
            salt = get_random_bytes(32)
            self.master_key = PBKDF2(password, salt, dkLen=32, count=100000)
            
            # Save salt
            salt_file = self.storage_dir / '.salt'
            with open(salt_file, 'wb') as f:
                f.write(salt)
            
            self.logger.info("✅ Vault initialized")
            return True
            
        except Exception as e:
            self.handle_error(e)
            return False
    
    def encrypt_data(self, data: str) -> Optional[Dict[str, str]]:
        """Encrypt data with AES-256-GCM"""
        if not CRYPTO_AVAILABLE or not self.master_key:
            return None
        
        try:
            nonce = get_random_bytes(16)
            cipher = AES.new(self.master_key, AES.MODE_GCM, nonce=nonce)
            ciphertext, tag = cipher.encrypt_and_digest(data.encode())
            
            return {
                'nonce': nonce.hex(),
                'ciphertext': ciphertext.hex(),
                'tag': tag.hex()
            }
        except Exception as e:
            self.handle_error(e)
            return None
    
    def store_file(self, filename: str, data: str) -> bool:
        """Store file in vault"""
        self.logger.info(f"📁 Storing file: {filename}")
        
        try:
            # Encrypt if crypto available
            encrypted = self.encrypt_data(data) if CRYPTO_AVAILABLE else None
            
            # Create block for each chain
            for i, chain in enumerate(self.chains):
                block_data = {
                    'filename': filename,
                    'timestamp': datetime.now().isoformat(),
                    'size': len(data),
                    'encrypted': encrypted if i == 0 else None
                }
                
                new_block = Block(
                    len(chain.chain),
                    datetime.now().isoformat(),
                    json.dumps(block_data),
                    chain.get_latest_block().hash
                )
                
                # Braid with next chain
                if i < len(self.chains) - 1:
                    new_block.braid_hash = self.chains[i+1].get_latest_block().hash
                
                chain.add_block(new_block)
                self.blocks_mined += 1
            
            # Save encrypted file
            if encrypted:
                file_path = self.storage_dir / f"{filename}.encrypted"
                with open(file_path, 'w') as f:
                    json.dump(encrypted, f)
            
            self.files_encrypted += 1
            self.logger.info(f"✅ File stored: {filename}")
            return True
            
        except Exception as e:
            self.handle_error(e)
            return False
    
    def verify_integrity(self) -> bool:
        """Verify blockchain integrity"""
        self.logger.info("🔍 Verifying blockchain integrity...")
        
        all_valid = True
        for i, chain in enumerate(self.chains):
            if chain.is_valid():
                self.logger.info(f"✅ Chain {i} is valid")
            else:
                self.logger.error(f"❌ Chain {i} is INVALID")
                all_valid = False
        
        return all_valid
    
    def sync_chains(self):
        """Sync braided chains"""
        while self.running:
            try:
                self.logger.info("🔄 Syncing braided chains...")
                
                # Ensure all chains have same length
                max_length = max(len(chain.chain) for chain in self.chains)
                
                for chain in self.chains:
                    while len(chain.chain) < max_length:
                        # Add empty sync block
                        new_block = Block(
                            len(chain.chain),
                            datetime.now().isoformat(),
                            json.dumps({'type': 'sync_block'}),
                            chain.get_latest_block().hash
                        )
                        chain.add_block(new_block)
                
                # Verify integrity
                self.verify_integrity()
                
                time.sleep(self.sync_interval)
                
            except Exception as e:
                self.handle_error(e)
                time.sleep(600)
    
    def get_status(self) -> Dict[str, Any]:
        """Get vault status"""
        status = super().get_status()
        status.update({
            'chains': len(self.chains),
            'blocks_per_chain': [len(chain.chain) for chain in self.chains],
            'blocks_mined': self.blocks_mined,
            'files_encrypted': self.files_encrypted,
            'vault_initialized': self.master_key is not None,
            'crypto_available': CRYPTO_AVAILABLE
        })
        return status
    
    def print_status(self):
        """Print vault status"""
        status = self.get_status()
        
        print("\n" + "="*70)
        print("🔐 NiA_VAULT BRAIDED BLOCKCHAIN - STATUS")
        print("="*70)
        print(f"Vault Initialized: {'YES' if status['vault_initialized'] else 'NO'}")
        print(f"Crypto Available: {'YES' if status['crypto_available'] else 'NO'}")
        print(f"Braided Chains: {status['chains']}")
        print(f"Blocks per Chain: {status['blocks_per_chain']}")
        print(f"Total Blocks Mined: {status['blocks_mined']}")
        print(f"Files Encrypted: {status['files_encrypted']}")
        print("="*70 + "\n")
    
    def run(self):
        """Start NiA_Vault"""
        self.start()
        
        # Initialize vault with default password
        if CRYPTO_AVAILABLE:
            self.initialize_vault("default_password_change_me")
        
        # Start sync thread
        sync_thread = threading.Thread(target=self.sync_chains, daemon=True)
        sync_thread.start()
        
        self.logger.info("✅ NiA_Vault active")
        
        try:
            while self.running:
                time.sleep(300)
                self.print_status()
                
        except KeyboardInterrupt:
            self.logger.info("⏹️  Shutting down NiA_Vault...")
        except Exception as e:
            self.handle_error(e)
        finally:
            self.stop()


if __name__ == '__main__':
    vault = NiAVault()
    vault.run()
