import React, { useState, useEffect } from 'react';
import api from '../services/api';
// import './Dashboard.css';

function Dashboard({ onLogout }) {
    const [healthSummary, setHealthSummary] = useState(null);
    const [healthRecords, setHealthRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('dashboard');
    const [user, setUser] = useState(null);

    

}