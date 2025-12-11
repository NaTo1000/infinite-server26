import React from 'react';
import '../styles/BlockchainPage.css';

const BlockchainPage = () => {
  return (
    <div className="blockchain-page">
      <h2>NiA_Vault Blockchain</h2>
      
      <div className="vault-status">
        <div className="vault-card">
          <h3>⛓️ Braided Blockchain Status</h3>
          <div className="chains-visual">
            <div className="chain chain-1">
              <span className="chain-label">Chain A</span>
              <div className="chain-blocks">
                {[1, 2, 3, 4, 5].map(i => (
                  <div key={i} className="block"></div>
                ))}
              </div>
            </div>
            <div className="chain chain-2">
              <span className="chain-label">Chain B</span>
              <div className="chain-blocks">
                {[1, 2, 3, 4, 5].map(i => (
                  <div key={i} className="block"></div>
                ))}
              </div>
            </div>
            <div className="chain chain-3">
              <span className="chain-label">Chain C</span>
              <div className="chain-blocks">
                {[1, 2, 3, 4, 5].map(i => (
                  <div key={i} className="block"></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="blockchain-metrics">
        <div className="metric-card">
          <div className="metric-label">Total Blocks</div>
          <div className="metric-value">1,247</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Storage Used</div>
          <div className="metric-value">3.2 GB</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Encryption</div>
          <div className="metric-value">AES-256-GCM</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Last Sync</div>
          <div className="metric-value">2 min ago</div>
        </div>
      </div>

      <div className="recent-transactions">
        <h3>Recent Transactions</h3>
        <div className="transactions-list">
          <div className="transaction-item">
            <span className="tx-hash">0x7a8b...</span>
            <span className="tx-type">Store</span>
            <span className="tx-time">2 min ago</span>
          </div>
          <div className="transaction-item">
            <span className="tx-hash">0x5c3d...</span>
            <span className="tx-type">Verify</span>
            <span className="tx-time">5 min ago</span>
          </div>
          <div className="transaction-item">
            <span className="tx-hash">0x9f2e...</span>
            <span className="tx-type">Sync</span>
            <span className="tx-time">8 min ago</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlockchainPage;
