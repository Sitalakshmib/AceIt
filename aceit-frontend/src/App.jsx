import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext.jsx';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Aptitude from './pages/Aptitude';
import Coding from './pages/Coding';
import Navbar from './components/Layout/Navbar';
import Resume from './pages/Resume';
import UnifiedAnalytics from './pages/UnifiedAnalytics';
import Interview from './pages/Interview';
import GroupDiscussion from './pages/GroupDiscussion';


const ProtectedRoute = ({ children }) => {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-100 relative">
          <div className="absolute inset-0 tech-pattern opacity-60 pointer-events-none" />
          <div className="relative z-10">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/" element={
                <ProtectedRoute>
                  <Navbar />
                  <Dashboard />
                </ProtectedRoute>
              } />
              <Route path="/aptitude" element={
                <ProtectedRoute>
                  <Navbar />
                  <Aptitude />
                </ProtectedRoute>
              } />
              <Route path="/coding" element={
                <ProtectedRoute>
                  <Navbar />
                  <Coding />
                </ProtectedRoute>
              } />
              <Route path="/group-discussion" element={
                <ProtectedRoute>
                  <Navbar />
                  <GroupDiscussion />
                </ProtectedRoute>
              } />
              <Route path="/resume" element={
                <ProtectedRoute>
                  <Navbar />
                  <Resume />
                </ProtectedRoute>
              } />
              <Route path="/interview" element={
                <ProtectedRoute>
                  <Navbar />
                  <Interview />
                </ProtectedRoute>
              } />
              <Route path="/analytics/unified" element={
                <ProtectedRoute>
                  <Navbar />
                  <UnifiedAnalytics />
                </ProtectedRoute>
              } />
            </Routes>
          </div>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;