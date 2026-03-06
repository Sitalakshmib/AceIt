import React, { createContext, useState, useContext } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  // Load token and user from localStorage on init
  const storedToken = localStorage.getItem('aceit_access_token');
  const storedUser = localStorage.getItem('aceit_user');

  const [user, setUser] = useState(storedUser ? JSON.parse(storedUser) : null);
  const [token, setToken] = useState(storedToken);

  const login = async (email, password) => {
    try {
      console.log('Attempting login with:', { email, password: '***' });
      const response = await authAPI.login(email, password);
      console.log('Login response:', response.data);

      const { user: userData, access_token } = response.data;

      // Store both in state and localStorage
      setUser(userData);
      setToken(access_token);
      localStorage.setItem('aceit_access_token', access_token);
      localStorage.setItem('aceit_user', JSON.stringify(userData));

      return { success: true };
    } catch (error) {
      console.error('Login failed:', error);
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const register = async (userData) => {
    try {
      console.log('Attempting registration with:', userData);
      console.log('API Base URL:', import.meta.env.VITE_API_URL);
      const response = await authAPI.register(userData);
      console.log('Registration successful:', response.data);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Registration failed:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('aceit_access_token');
    localStorage.removeItem('aceit_user');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);