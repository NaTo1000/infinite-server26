import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));

// Hide loading screen
const loadingElement = document.getElementById('loading');
if (loadingElement) {
  setTimeout(() => {
    loadingElement.style.display = 'none';
  }, 1000);
}

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
