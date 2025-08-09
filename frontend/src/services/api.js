import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

class HealthSyncAPI {
    constructor() {
        this.api = axios.create({
            baseURL: API_BASE_URL,
            headers: {
                'Content-Type': 'application/json'
            },
        });

        // Add token to requests automatically
        this.api.interceptors.request.use(
            (config) => {
                const token = localStorage.getItem('token');
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
                return config;
            },
            (error) => {
                return Promise.reject(error);
            }
        );

        // Handle auth errors
        this.api.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response?.status === 401) {
                    // Token expired/invalid
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                }
                return Promise.reject(error);
            }
        );
    }

    // Authentication methods
    async login(email, password) {
        try {
            const response = await this.api.post('/auth/login', { email, password });
            const { access_token } = response.data;
            localStorage.setItem('token', access_token);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Login failed');
        }
    }

    async register(userData) {
        try {
            const response = await this.api.post('/auth/register', userData);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Registration failed');
        }
    }

    async getCurrentUser() {
        try {
            const response = await this.api.get('/auth/me');
            return response.data;
        } catch(error) {
            throw new Error('Failed to get user info');
        }
    }

    logout() {
        localStorage.removeItem('token');
        window.location.href='/login';
    }

    isAuthenticated() {
        return !!localStorage.getItem('token');
    }


    // Health data methods
    async addHealthRecord(recordData) {
        try {
            const response = await this.api.post('/health/records', recordData);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Failed to add health record');
        }
    }

    async quickAddHealthRecords(quickData) {
        try {
            const response = await this.api.post('/health/quick-add', quickData);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Failed to add health records');
        }
    }

    async getHealthRecord(params = {}) {
        try {
            const response = await this.api.get('/health/records', { params });
            return response.data;
        } catch (error) {
            throw new Error('Failed to fetch health records');
        }
    }

    async getHealthSummary() {
        try {
            const response = await this.api.get('/health/summary');
            return response.data;
        } catch (error) {
            throw new Error('Failed to fetch health summary');
        }
    }
}

const api = new HealthSyncAPI()
export default api;