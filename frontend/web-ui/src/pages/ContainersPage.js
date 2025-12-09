import React from 'react';
import '../styles/ContainersPage.css';

const ContainersPage = () => {
  const containers = [
    { name: 'infinite-fortress', status: 'running', cpu: '12%', memory: '2.1 GB' },
    { name: 'rancher-dashboard', status: 'running', cpu: '5%', memory: '512 MB' },
    { name: 'naydoe-orchestrator', status: 'running', cpu: '8%', memory: '1.2 GB' },
    { name: 'jessicai-huntress', status: 'running', cpu: '6%', memory: '800 MB' },
    { name: 'nai-gail-shield', status: 'running', cpu: '4%', memory: '600 MB' },
    { name: 'nia-vault-blockchain', status: 'running', cpu: '10%', memory: '1.5 GB' },
  ];

  return (
    <div className="containers-page">
      <h2>Container Management</h2>
      
      <div className="containers-overview">
        <div className="overview-card">
          <span className="overview-label">Total Containers</span>
          <span className="overview-value">{containers.length}</span>
        </div>
        <div className="overview-card">
          <span className="overview-label">Running</span>
          <span className="overview-value">{containers.filter(c => c.status === 'running').length}</span>
        </div>
        <div className="overview-card">
          <span className="overview-label">Total CPU</span>
          <span className="overview-value">45%</span>
        </div>
        <div className="overview-card">
          <span className="overview-label">Total Memory</span>
          <span className="overview-value">6.7 GB</span>
        </div>
      </div>

      <div className="containers-list">
        <table className="containers-table">
          <thead>
            <tr>
              <th>Container Name</th>
              <th>Status</th>
              <th>CPU</th>
              <th>Memory</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {containers.map((container, index) => (
              <tr key={index}>
                <td className="container-name">
                  <span className="container-icon">🐳</span>
                  {container.name}
                </td>
                <td>
                  <span className={`status-badge ${container.status}`}>
                    {container.status.toUpperCase()}
                  </span>
                </td>
                <td>{container.cpu}</td>
                <td>{container.memory}</td>
                <td>
                  <div className="action-buttons">
                    <button className="btn-icon" title="View Logs">📄</button>
                    <button className="btn-icon" title="Restart">🔄</button>
                    <button className="btn-icon" title="Stop">⏹️</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ContainersPage;
