import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './Dashboard.css';

function Dashboard({ onLogout }) {
    const [healthSummary, setHealthSummary] = useState(null);
    const [healthRecords, setHealthRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('dashboard');
    const [user, setUser] = useState(null);

    useEffect(() => {
        loadDashboardData();
    }, []);

    const loadDashboardData = async () => {
        try {
            setLoading(true);

            // Load user infor
            const [userResponse, summaryResponse, recordsResponse] = await Promise.all([
                api.getCurrentUser(),
                api.getHealthSummary(),
                api.getHealthRecord({ limit: 10 })
            ]);

            setUser(userResponse);
            setHealthSummary(summaryResponse);
            setHealthRecords(recordsResponse);
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleRecordAdded = () => {
        // Refresh when new record added
        loadDashboardData();
    };

    if (loading) {
        return (
            <div className="dashboard-container">
                <div className="loading-card">
                    <div className="loading-spinner"></div>
                    <p>Loading your health data...</p>
            </div>
      </div>
        );
    }

    return (
        <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <h1>HealthSync</h1>
            {user && <p>Welcome back, {user.email}!</p>}
          </div>
          <button onClick={onLogout} className="logout-button">
            Logout
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="dashboard-nav">
        <button 
          className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={`nav-tab ${activeTab === 'add' ? 'active' : ''}`}
          onClick={() => setActiveTab('add')}
        >
          Add Data
        </button>
        <button 
          className={`nav-tab ${activeTab === 'records' ? 'active' : ''}`}
          onClick={() => setActiveTab('records')}
        >
          View Records
        </button>
      </nav>

      {/* Main Content */}
      <main className="dashboard-main">
        {activeTab === 'dashboard' && (
          <div className="dashboard-content">
            <h2>Health Overview</h2>
            
            {/* Summary Cards */}
            <div className="summary-grid">
              <div className="summary-card">
                <h3>Total Records</h3>
                <div className="summary-value">
                  {healthSummary?.total_records || 0}
                </div>
                <p>Health measurements tracked</p>
              </div>
              
              <div className="summary-card">
                <h3>Measurement Types</h3>
                <div className="summary-value">
                  {healthSummary?.measurement_types_count || 0}
                </div>
                <p>Different health metrics</p>
              </div>
              
              <div className="summary-card">
                <h3>Latest Entry</h3>
                <div className="summary-value">
                  {healthRecords.length > 0 ? 'Today' : 'None'}
                </div>
                <p>Most recent measurement</p>
              </div>
            </div>

            {/* Recent Records */}
            <div className="recent-records">
              <h3>Recent Measurements</h3>
              {healthRecords.length > 0 ? (
                <div className="records-list">
                  {healthRecords.slice(0, 5).map(record => (
                    <div key={record.id} className="record-item">
                      <div className="record-type">
                        {record.measurement_type.replace('_', ' ')}
                      </div>
                      <div className="record-value">
                        {record.value} {record.unit}
                      </div>
                      <div className="record-date">
                        {new Date(record.measured_at).toLocaleDateString()}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  <p>No health records yet. Start by adding your first measurement!</p>
                  <button 
                    className="primary-button"
                    onClick={() => setActiveTab('add')}
                  >
                    Add Your First Record
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* {activeTab === 'add' && (
          <AddHealthRecord onRecordAdded={handleRecordAdded} />
        )}

        {activeTab === 'records' && (
          <HealthRecordsList records={healthRecords} onRefresh={loadDashboardData} />
        )} */}
      </main>
    </div>

    )


}

export default Dashboard;