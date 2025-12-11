import React from 'react';
import '../styles/AISystemsPage.css';

const AISystemsPage = () => {
  return (
    <div className="ai-systems-page">
      <h2>AI Systems Control Center</h2>
      
      <div className="ai-grid">
        <div className="ai-card naydoe">
          <div className="ai-card-header">
            <h3>🤖 NayDoeV1 Orchestrator</h3>
            <span className="status-badge online">ONLINE</span>
          </div>
          <div className="ai-card-body">
            <div className="ai-info">
              <div className="info-row">
                <span className="label">Mode:</span>
                <span className="value">AUTONOMOUS</span>
              </div>
              <div className="info-row">
                <span className="label">Uptime:</span>
                <span className="value">156 hours</span>
              </div>
              <div className="info-row">
                <span className="label">Tasks Completed:</span>
                <span className="value">12,847</span>
              </div>
            </div>
            <div className="ai-controls">
              <button className="btn btn-primary">View Logs</button>
              <button className="btn btn-secondary">Configure</button>
            </div>
          </div>
        </div>

        <div className="ai-card jessicai">
          <div className="ai-card-header">
            <h3>🔒 JessicAi Huntress</h3>
            <span className="status-badge online">HUNTING</span>
          </div>
          <div className="ai-card-body">
            <div className="ai-info">
              <div className="info-row">
                <span className="label">Mode:</span>
                <span className="value">NO MERCY</span>
              </div>
              <div className="info-row">
                <span className="label">Threats Blocked:</span>
                <span className="value">0</span>
              </div>
              <div className="info-row">
                <span className="label">Last Scan:</span>
                <span className="value">2 min ago</span>
              </div>
            </div>
            <div className="ai-controls">
              <button className="btn btn-danger">View Threats</button>
              <button className="btn btn-secondary">Reports</button>
            </div>
          </div>
        </div>

        <div className="ai-card twinbrain">
          <div className="ai-card-header">
            <h3>🧠 Quantum TwinBrain</h3>
            <span className="status-badge online">ENHANCED</span>
          </div>
          <div className="ai-card-body">
            <div className="ai-info">
              <div className="info-row">
                <span className="label">Consciousness:</span>
                <span className="value">ACTIVE</span>
              </div>
              <div className="info-row">
                <span className="label">Decisions:</span>
                <span className="value">1,234</span>
              </div>
              <div className="info-row">
                <span className="label">Accuracy:</span>
                <span className="value">99.7%</span>
              </div>
            </div>
            <div className="ai-controls">
              <button className="btn btn-primary">Analytics</button>
              <button className="btn btn-secondary">Settings</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AISystemsPage;
