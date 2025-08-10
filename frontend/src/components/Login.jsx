import React, { use, useState } from "react";
import api from '../services/api';
import './Login.css'

function Login({ onLoginSuccess }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const result = await api.login(email, password);
            console.log('Login successful:', result);

            // Call parent component to handle successful login
            if (onLoginSuccess) {
                onLoginSuccess(result);
            }
        } catch (error) {
            console.error('Login error:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h2>HealthSync</h2>
          <p>Sign in to your account</p>
        </div>

        <form onSubmit={handleLogin} className="login-form">
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={loading || !email || !password}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="login-footer">
          <p>
            Don't have an account?{' '}
            <button className="link-button" type="button">
              Sign up
            </button>
          </p>
        </div>
      </div>
    </div>
    );
}

export default Login