import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import api from './services/api';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const checkAuth = async () => {
      if (api.isAuthenticated()) {
        try {
          //  Verify token is sitll valid
          await api.getCurrentUser();
          setIsAuthenticated(true);
        } catch (error) {
          //  Token invalid, remove it
          localStorage.removeItem('token');
          setIsAuthenticated(false);
        }
      }
      setLoading(false);
    };
    checkAuth();
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    api.logout();
    setIsAuthenticated(false);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>HealthSync Dashboard</h1>
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </header>

      <main className="app-main">
        <div className="welcome-message">
          <h2>Welcome to HealthSync!</h2>
          <p>Backend APIs working</p>
        </div>
      </main>
    </div>
  );
}

export default App;
