import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './Dashboard.css';
import HealthRecordForm from './HealthRecordForm';

function Dashboard({ onLogout }) {
    const [healthSummary, setHealthSummary] = useState(null);
    const [healthRecords, setHealthRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('dashboard');
    const [user, setUser] = useState(null);
    const [showAddForm, setShowAddForm] = useState(false);

    useEffect(() => {
        loadDashboardData();
    }, []);

    const loadDashboardData = async () => {
        try {
            setLoading(true);

            // Load user info
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

    const refreshHealthData = async () => {
        try {
            const summaryResponse = await api.getHealthSummary();
            const recordsResponse = await api.getHealthRecord({ limit: 10 });

            setHealthSummary(summaryResponse);
            setHealthRecords(recordsResponse);
        } catch (error) {
            console.error('Failed to refresh health data:', error);
        }
    };

    const handleRecordAdded = async () => {
        // Close the form first
        setShowAddForm(false);
        
        // Refresh only the health data (skip user data since it doesn't change)
        try {
            // Add a small delay to ensure backend has processed the new record
            setTimeout(async () => {
                await refreshHealthData();
            }, 200);
        } catch (error) {
            console.error('Error refreshing dashboard:', error);
            // Fallback - reload after a longer delay
            setTimeout(() => {
                refreshHealthData();
            }, 1000);
        }
    };

    const handleAddRecord = () => {
      setShowAddForm(true);
    };

    const handleFormClose = () => {
      setShowAddForm(false);
    };

    const formatMeasurementType = (type) => {
      return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    };

    const formatDate = (dateString) => {
      return new  Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }

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
              
              {/* Navigation Tabs - now inline */}
              <nav className="dashboard-nav">
                <button 
                  className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
                  onClick={() => setActiveTab('dashboard')}
                >
                  Dashboard
                </button>
                <button 
                  className={`nav-tab ${activeTab === 'records' ? 'active' : ''}`}
                  onClick={() => setActiveTab('records')}
                >
                  View Records
                </button>
              </nav>
              
              <div className="header-actions">
                <button 
                    onClick={handleAddRecord}
                    className="add-record-button"
                >
                  <span className='btn-icon'>+</span>
                  Add Health Record
                </button>
                <button onClick={onLogout} className="logout-button">
                    Logout
                </button>
              </div>
            </div>
          </header>

      {/* Main Content */}
      <main className="dashboard-main">
        {activeTab === 'dashboard' && (
          <div className="dashboard-content">
            <div className='content-header'>
              <h2>Health Overview</h2>
              {healthRecords.length > 0 && (
                <button
                    onClick={handleAddRecord}
                    className='quick-add-button'
                >
                  + Quick Add
                </button>
              )}
            </div>
            
            {/* Summary Cards */}
            <div className="summary-grid">
                            <div className="summary-card">
                                <div className="card-icon">📊</div>
                                <div className="card-content">
                                    <h3>Total Records</h3>
                                    <div className="summary-value">
                                        {healthSummary?.total_records || 0}
                                    </div>
                                    <p>Health measurements tracked</p>
                                </div>
                            </div>
                            
                            <div className="summary-card">
                                <div className="card-icon">📈</div>
                                <div className="card-content">
                                    <h3>Measurement Types</h3>
                                    <div className="summary-value">
                                        {healthSummary?.measurement_types_count || 0}
                                    </div>
                                    <p>Different health metrics</p>
                                </div>
                            </div>
                            
                            <div className="summary-card">
                                <div className="card-icon">📅</div>
                                <div className="card-content">
                                    <h3>Days Tracking</h3>
                                    <div className="summary-value">
                                        {healthSummary?.date_range ? 
                                            Math.ceil((new Date() - new Date(healthSummary.date_range.earliest)) / (1000 * 60 * 60 * 24)) 
                                            : 0
                                        }
                                    </div>
                                    <p>Consecutive tracking</p>
                                </div>
                            </div>
                        </div>

                        {/* Recent Records */}
                        <div className="recent-records">
                            <h3>Recent Measurements</h3>
                            {healthRecords.length > 0 ? (
                                <div className="records-list">
                                    {healthRecords.slice(0, 5).map(record => (
                                        <div key={record.id} className="record-item">
                                            <div className="record-info">
                                                <div className="record-type">
                                                    {formatMeasurementType(record.measurement_type)}
                                                </div>
                                                <div className="record-value">
                                                    {record.value} {record.unit}
                                                </div>
                                                {record.notes && (
                                                    <div className="record-notes">{record.notes}</div>
                                                )}
                                            </div>
                                            <div className="record-date">
                                                {formatDate(record.measured_at)}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="empty-state">
                                    <div className="empty-icon">📝</div>
                                    <h4>No health records yet</h4>
                                    <p>Start tracking your health by adding your first measurement</p>
                                    <button 
                                        className="primary-button"
                                        onClick={handleAddRecord}
                                    >
                                        Add Your First Record
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {activeTab === 'records' && (
                    <div className="records-content">
                        <div className="content-header">
                            <h2>All Health Records</h2>
                            <button 
                                onClick={handleAddRecord}
                                className="add-record-button"
                            >
                                <span className="btn-icon">+</span>
                                Add Record
                            </button>
                        </div>
                        
                        {healthRecords.length > 0 ? (
                            <div className="all-records-list">
                                {healthRecords.map(record => (
                                    <div key={record.id} className="record-card">
                                        <div className="record-header">
                                            <h4>{formatMeasurementType(record.measurement_type)}</h4>
                                            <span className="record-date">{formatDate(record.measured_at)}</span>
                                        </div>
                                        <div className="record-body">
                                            <div className="record-value-large">
                                                {record.value} <span className="unit">{record.unit}</span>
                                            </div>
                                            {record.notes && (
                                                <div className="record-notes">{record.notes}</div>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="empty-state">
                                <div className="empty-icon">📊</div>
                                <h4>No records to display</h4>
                                <p>Add your first health measurement to get started</p>
                                <button 
                                    className="primary-button"
                                    onClick={handleAddRecord}
                                >
                                    Add Your First Record
                                </button>
                            </div>
                        )}
                    </div>
                )}
      </main>
                {/* Modal for Add Health Record Form */}
                {showAddForm && (
                  <div className="modal-overlay" onClick={handleFormClose}>
                      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                          <div className="modal-header">
                              <h2>Add Health Record</h2>
                              <button 
                                  className="modal-close-btn"
                                  onClick={handleFormClose}
                                  aria-label="Close"
                              >
                                  ×
                              </button>
                          </div>
                          <div className="modal-body">
                              <HealthRecordForm 
                                  onRecordAdded={handleRecordAdded}
                                  onCancel={handleFormClose}
                              />
                          </div>
                      </div>
                  </div>
              )}
          </div>

    )


}

export default Dashboard;