import React, { useState } from 'react';
import '../styles/SettingsPage.css';

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    mercyMode: false,
    autoHeal: true,
    shieldRadius: 100,
    threatResponse: 'immediate'
  });

  const handleToggle = (setting) => {
    setSettings(prev => ({
      ...prev,
      [setting]: !prev[setting]
    }));
  };

  return (
    <div className="settings-page">
      <h2>System Settings</h2>
      
      <div className="settings-section">
        <h3>Security Settings</h3>
        <div className="setting-item">
          <div className="setting-info">
            <div className="setting-label">JessicAi Mercy Mode</div>
            <div className="setting-description">Enable mercy mode for threat response (Not Recommended)</div>
          </div>
          <label className="toggle">
            <input 
              type="checkbox" 
              checked={settings.mercyMode}
              onChange={() => handleToggle('mercyMode')}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="setting-item">
          <div className="setting-info">
            <div className="setting-label">Auto-Heal</div>
            <div className="setting-description">Automatically heal system failures</div>
          </div>
          <label className="toggle">
            <input 
              type="checkbox" 
              checked={settings.autoHeal}
              onChange={() => handleToggle('autoHeal')}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="setting-item">
          <div className="setting-info">
            <div className="setting-label">Shield Radius</div>
            <div className="setting-description">NAi_gAil mesh shield coverage radius (meters)</div>
          </div>
          <input 
            type="number" 
            className="setting-input"
            value={settings.shieldRadius}
            onChange={(e) => setSettings(prev => ({ ...prev, shieldRadius: e.target.value }))}
          />
        </div>
      </div>

      <div className="settings-section">
        <h3>System Information</h3>
        <div className="info-grid">
          <div className="info-item">
            <span className="info-label">Version:</span>
            <span className="info-value">26.1</span>
          </div>
          <div className="info-item">
            <span className="info-label">Codename:</span>
            <span className="info-value">FORTRESS</span>
          </div>
          <div className="info-item">
            <span className="info-label">Owner:</span>
            <span className="info-value">nato1000</span>
          </div>
          <div className="info-item">
            <span className="info-label">License:</span>
            <span className="info-value">MIT</span>
          </div>
        </div>
      </div>

      <div className="settings-actions">
        <button className="btn btn-primary">Save Settings</button>
        <button className="btn btn-secondary">Reset to Defaults</button>
      </div>
    </div>
  );
};

export default SettingsPage;
