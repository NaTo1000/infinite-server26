import React, { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const [metrics, setMetrics] = useState({
    cpu: 45,
    memory: 62,
    threats: 0,
    containers: 8
  });

  const [cpuData, setCpuData] = useState([
    { time: '00:00', value: 30 },
    { time: '00:05', value: 35 },
    { time: '00:10', value: 40 },
    { time: '00:15', value: 45 },
    { time: '00:20', value: 42 }
  ]);

  useEffect(() => {
    // Simulate real-time data updates
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        cpu: Math.floor(Math.random() * 30) + 40,
        memory: Math.floor(Math.random() * 20) + 55
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>System Overview</h2>
        <div className="security-badge">
          <span className="badge-icon">🛡️</span>
          <span className="badge-text">FORTRESS MODE ACTIVE</span>
        </div>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon cpu-icon">⚡</div>
          <div className="metric-content">
            <div className="metric-label">CPU Usage</div>
            <div className="metric-value">{metrics.cpu}%</div>
          </div>
          <div className="metric-bar">
            <div className="metric-bar-fill" style={{ width: `${metrics.cpu}%` }} />
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon memory-icon">💾</div>
          <div className="metric-content">
            <div className="metric-label">Memory Usage</div>
            <div className="metric-value">{metrics.memory}%</div>
          </div>
          <div className="metric-bar">
            <div className="metric-bar-fill" style={{ width: `${metrics.memory}%` }} />
          </div>
        </div>

        <div className="metric-card threats-card">
          <div className="metric-icon threats-icon">🔒</div>
          <div className="metric-content">
            <div className="metric-label">Threats Blocked</div>
            <div className="metric-value">{metrics.threats}</div>
          </div>
          <div className="metric-status">All Clear</div>
        </div>

        <div className="metric-card">
          <div className="metric-icon containers-icon">🐳</div>
          <div className="metric-content">
            <div className="metric-label">Active Containers</div>
            <div className="metric-value">{metrics.containers}</div>
          </div>
          <div className="metric-status">Running</div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>CPU Performance</h3>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={cpuData}>
              <defs>
                <linearGradient id="cpuGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#00ff41" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#00ff41" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="time" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1a1f3a', border: '1px solid #00ff41' }}
              />
              <Area 
                type="monotone" 
                dataKey="value" 
                stroke="#00ff41" 
                fillOpacity={1} 
                fill="url(#cpuGradient)" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>AI Systems Status</h3>
          <div className="ai-systems-list">
            <div className="ai-system-item">
              <div className="ai-system-name">
                <span className="status-dot online"></span>
                NayDoeV1 Orchestrator
              </div>
              <div className="ai-system-status">AUTONOMOUS</div>
            </div>
            
            <div className="ai-system-item">
              <div className="ai-system-name">
                <span className="status-dot online"></span>
                JessicAi Huntress
              </div>
              <div className="ai-system-status">NO MERCY MODE</div>
            </div>
            
            <div className="ai-system-item">
              <div className="ai-system-name">
                <span className="status-dot online"></span>
                Quantum TwinBrain
              </div>
              <div className="ai-system-status">ENHANCED</div>
            </div>
            
            <div className="ai-system-item">
              <div className="ai-system-name">
                <span className="status-dot online"></span>
                NAi_gAil Shield
              </div>
              <div className="ai-system-status">IMPENETRABLE</div>
            </div>
          </div>
        </div>
      </div>

      <div className="activity-feed">
        <h3>Recent Activity</h3>
        <div className="activity-list">
          <div className="activity-item">
            <span className="activity-time">2 min ago</span>
            <span className="activity-message">✓ All systems health check passed</span>
          </div>
          <div className="activity-item">
            <span className="activity-time">5 min ago</span>
            <span className="activity-message">🔒 JessicAi: No threats detected</span>
          </div>
          <div className="activity-item">
            <span className="activity-time">10 min ago</span>
            <span className="activity-message">🤖 NayDoeV1: Optimization cycle completed</span>
          </div>
          <div className="activity-item">
            <span className="activity-time">15 min ago</span>
            <span className="activity-message">⛓️ NiA_Vault: Blockchain sync successful</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
