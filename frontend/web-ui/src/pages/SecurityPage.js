import React from 'react';
import '../styles/SecurityPage.css';

const SecurityPage = () => {
  return (
    <div className="security-page">
      <h2>Security Control Center</h2>
      
      <div className="security-overview">
        <div className="security-status">
          <div className="status-icon">🛡️</div>
          <h3>FORTRESS MODE ACTIVE</h3>
          <p>All defense systems operational</p>
        </div>
      </div>

      <div className="security-grid">
        <div className="security-card">
          <h3>NAi_gAil Mesh Shield</h3>
          <div className="shield-status">
            <div className="shield-visual">
              <div className="shield-dome"></div>
            </div>
            <div className="shield-info">
              <div className="info-item">
                <span className="label">Status:</span>
                <span className="value online">IMPENETRABLE</span>
              </div>
              <div className="info-item">
                <span className="label">Coverage:</span>
                <span className="value">100m Radius</span>
              </div>
              <div className="info-item">
                <span className="label">Devices:</span>
                <span className="value">12 Protected</span>
              </div>
            </div>
          </div>
        </div>

        <div className="security-card">
          <h3>Firewall Status</h3>
          <div className="firewall-info">
            <div className="info-item">
              <span className="label">UFW Status:</span>
              <span className="value online">ACTIVE</span>
            </div>
            <div className="info-item">
              <span className="label">Fail2Ban:</span>
              <span className="value online">ENABLED</span>
            </div>
            <div className="info-item">
              <span className="label">Blocked IPs:</span>
              <span className="value">0</span>
            </div>
            <div className="info-item">
              <span className="label">Rules:</span>
              <span className="value">24 Active</span>
            </div>
          </div>
        </div>
      </div>

      <div className="threat-log">
        <h3>Threat Log</h3>
        <div className="log-container">
          <div className="log-entry success">
            <span className="log-time">[16:20:45]</span>
            <span className="log-message">System scan completed - No threats detected</span>
          </div>
          <div className="log-entry info">
            <span className="log-time">[16:15:30]</span>
            <span className="log-message">Firewall rules updated successfully</span>
          </div>
          <div className="log-entry info">
            <span className="log-time">[16:10:12]</span>
            <span className="log-message">Mesh shield integrity verified</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SecurityPage;
