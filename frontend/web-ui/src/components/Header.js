import React from 'react';
import '../styles/Header.css';

const Header = ({ toggleSidebar, systemStatus }) => {
  const getStatusColor = (status) => {
    switch(status) {
      case 'online': return '#00ff41';
      case 'warning': return '#ffaa00';
      case 'offline': return '#ff0000';
      default: return '#888';
    }
  };

  return (
    <header className="header">
      <div className="header-left">
        <button className="sidebar-toggle" onClick={toggleSidebar}>
          ☰
        </button>
        <h1 className="header-title">Infinite Server26 - Security Fortress</h1>
      </div>
      
      <div className="header-right">
        <div className="system-indicators">
          <div className="indicator">
            <div 
              className="indicator-dot" 
              style={{ backgroundColor: getStatusColor(systemStatus.naydoe) }}
            />
            <span className="indicator-label">NayDoeV1</span>
          </div>
          
          <div className="indicator">
            <div 
              className="indicator-dot" 
              style={{ backgroundColor: getStatusColor(systemStatus.jessicai) }}
            />
            <span className="indicator-label">JessicAi</span>
          </div>
          
          <div className="indicator">
            <div 
              className="indicator-dot" 
              style={{ backgroundColor: getStatusColor(systemStatus.naiGail) }}
            />
            <span className="indicator-label">NAi_gAil</span>
          </div>
          
          <div className="indicator">
            <div 
              className="indicator-dot" 
              style={{ backgroundColor: getStatusColor(systemStatus.niaVault) }}
            />
            <span className="indicator-label">NiA_Vault</span>
          </div>
        </div>
        
        <div className="user-menu">
          <span className="username">nato1000</span>
          <div className="user-avatar">N</div>
        </div>
      </div>
    </header>
  );
};

export default Header;
