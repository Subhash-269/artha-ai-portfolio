import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = ({ setIsAuthenticated }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        // Store token and user info in localStorage
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify({
          id: data.user_id,
          username: data.username,
          email: data.email,
          first_name: data.first_name,
          last_name: data.last_name,
        }));
        
        setIsAuthenticated(true);
        navigate('/dashboard');
      } else {
        setError(data.error || 'Login failed. Please try again.');
      }
    } catch (err) {
      setError('Network error. Please check your connection.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '1rem',
    }}>
      <div style={{
        background: 'white',
        borderRadius: '1rem',
        boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
        padding: '2.5rem',
        maxWidth: '420px',
        width: '100%',
      }}>
        <h2 style={{
          fontSize: '2rem',
          fontWeight: '700',
          color: '#1a202c',
          marginBottom: '0.5rem',
          textAlign: 'center',
        }}>
          Welcome Back
        </h2>
        <p style={{
          color: '#718096',
          textAlign: 'center',
          marginBottom: '2rem',
        }}>
          Sign in to your account
        </p>

        {error && (
          <div style={{
            background: '#fed7d7',
            color: '#c53030',
            padding: '0.75rem',
            borderRadius: '0.5rem',
            marginBottom: '1.5rem',
            fontSize: '0.875rem',
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{
              display: 'block',
              color: '#4a5568',
              fontWeight: '600',
              marginBottom: '0.5rem',
              fontSize: '0.875rem',
            }}>
              Username
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '2px solid #e2e8f0',
                borderRadius: '0.5rem',
                fontSize: '1rem',
                transition: 'border-color 0.2s',
                outline: 'none',
              }}
              onFocus={(e) => e.target.style.borderColor = '#667eea'}
              onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{
              display: 'block',
              color: '#4a5568',
              fontWeight: '600',
              marginBottom: '0.5rem',
              fontSize: '0.875rem',
            }}>
              Password
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '2px solid #e2e8f0',
                borderRadius: '0.5rem',
                fontSize: '1rem',
                transition: 'border-color 0.2s',
                outline: 'none',
              }}
              onFocus={(e) => e.target.style.borderColor = '#667eea'}
              onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              background: loading ? '#a0aec0' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: '0.875rem',
              borderRadius: '0.5rem',
              border: 'none',
              fontSize: '1rem',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'transform 0.2s',
              marginBottom: '1rem',
            }}
            onMouseEnter={(e) => !loading && (e.target.style.transform = 'translateY(-2px)')}
            onMouseLeave={(e) => e.target.style.transform = 'translateY(0)'}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div style={{
          textAlign: 'center',
          color: '#718096',
          fontSize: '0.875rem',
        }}>
          Don't have an account?{' '}
          <a
            href="/signup"
            onClick={(e) => {
              e.preventDefault();
              navigate('/signup');
            }}
            style={{
              color: '#667eea',
              fontWeight: '600',
              textDecoration: 'none',
            }}
          >
            Sign up
          </a>
        </div>
      </div>
    </div>
  );
};

export default Login;
