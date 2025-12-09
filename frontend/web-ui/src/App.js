import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Components
import Dashboard from './pages/Dashboard';
import AISystemsPage from './pages/AISystemsPage';
import SecurityPage from './pages/SecurityPage';
import BlockchainPage from './pages/BlockchainPage';
import ContainersPage from './pages/ContainersPage';
import SettingsPage from './pages/SettingsPage';
import Sidebar from './components/Sidebar';
import Header from './components/Header';

// Styles
import './styles/App.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [systemStatus, setSystemStatus] = useState({
    naydoe: 'online',
    jessicai: 'online',
    naiGail: 'online',
    niaVault: 'online'
  });

  useEffect(() => {
    // Fetch system status on mount
    fetchSystemStatus();
    
    // Set up polling for status updates
    const interval = setInterval(fetchSystemStatus, 5000);
    
    return () => clearInterval(interval);
  }, []);

  const fetchSystemStatus = async () => {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch('http://localhost:8000/api/status');
      // const data = await response.json();
      // setSystemStatus(data);
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    }
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <Router>
      <div className="app">
        <Sidebar isOpen={sidebarOpen} />
        <div className={`main-content ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
          <Header 
            toggleSidebar={toggleSidebar} 
            systemStatus={systemStatus}
          />
          <div className="content-wrapper">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/ai-systems" element={<AISystemsPage />} />
              <Route path="/security" element={<SecurityPage />} />
              <Route path="/blockchain" element={<BlockchainPage />} />
              <Route path="/containers" element={<ContainersPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        </div>
        <ToastContainer 
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="dark"
        />
      </div>
    </Router>
  );
}

export default App;
