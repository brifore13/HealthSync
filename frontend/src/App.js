import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import api from './services/api';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      if (api.isAuthenticated()) {
        try {
          await api.getCurrentUser();
          setIsAuthenticated(true);
        } catch (error) {
          localStorage.removeItem('token');
          setIsAuthenticated(false);
        }
      }
      setLoading(false);
    };
    checkAuth();
  }, []);

  const handleLoginSuccess = () => setIsAuthenticated(true);
  const handleLogout = () => {
    api.logout();
    setIsAuthenticated(false);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <Router>
      <div className="App">
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            {/* Add components here */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;