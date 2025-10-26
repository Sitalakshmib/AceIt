import React, { createContext, useState, useContext } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('aceit_access_token'));

  const login = async (email, password) => {
    try {
      console.log('Attempting login with:', { email, password: '***' });
      console.log('API Base URL:', import.meta.env.VITE_API_URL);
      const response = await authAPI.login(email, password);
      console.log('Login response:', response.data);
      const { user: userData, access_token } = response.data;
      setUser(userData);
      setToken(access_token);
      localStorage.setItem('aceit_access_token', access_token);
      return { success: true };
    } catch (error) {
      console.error('Login failed:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
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
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);