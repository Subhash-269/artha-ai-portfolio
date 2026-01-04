import React from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = ({ children, setIsAuthenticated }) => {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    
    try {
      await fetch('http://localhost:8000/api/auth/logout/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
      });
    } catch (err) {
      console.error('Logout error:', err);
    }
    
    // Clear local storage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // Update auth state
    if (setIsAuthenticated) {
      setIsAuthenticated(false);
    }
    
    // Redirect to login
    navigate('/login');
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f3f4f6' }}>
      {/* Main Content (header is rendered inside DashboardDemo) */}
      <div style={{ padding: '0' }}>
        {React.cloneElement(children, { user, onLogout: handleLogout })}
      </div>
    </div>
  );
};

export default Dashboard;
