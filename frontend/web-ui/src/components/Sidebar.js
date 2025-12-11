import React from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/Sidebar.css';

const Sidebar = ({ isOpen }) => {
  const menuItems = [
    { path: '/', icon: '🏠', label: 'Dashboard' },
    { path: '/ai-systems', icon: '🤖', label: 'AI Systems' },
    { path: '/security', icon: '🛡️', label: 'Security' },
    { path: '/blockchain', icon: '⛓️', label: 'Blockchain' },
    { path: '/containers', icon: '🐳', label: 'Containers' },
    { path: '/settings', icon: '⚙️', label: 'Settings' }
  ];

  return (
    <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <div className="sidebar-header">
        <div className="logo">
          <span className="logo-icon">∞</span>
          {isOpen && <span className="logo-text">FORTRESS</span>}
        </div>
      </div>
      
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            end={item.path === '/'}
          >
            <span className="nav-icon">{item.icon}</span>
            {isOpen && <span className="nav-label">{item.label}</span>}
          </NavLink>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <div className="version-info">
          {isOpen && (
            <>
              <div className="version">v26.1</div>
              <div className="codename">FORTRESS</div>
            </>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
