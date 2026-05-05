import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { login, loginWithGoogle } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const result = await login(email, password);

    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }

    setIsLoading(false);
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    setIsLoading(true);
    setError('');
    const result = await loginWithGoogle(credentialResponse.credential);

    if (result.success) {
      navigate('/');
    } else {
      setError(result.error || 'Google login failed');
    }
    setIsLoading(false);
  };

  const handleGoogleError = () => {
    setError('Google Login Failed');
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center relative overflow-hidden"
      style={{
        backgroundImage: "url('/login-bg.png')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
      }}
    >
      {/* Dark gradient overlay for readability */}
      <div
        className="absolute inset-0"
        style={{
          background: 'linear-gradient(135deg, rgba(10,15,40,0.78) 0%, rgba(40,10,80,0.68) 60%, rgba(10,30,60,0.75) 100%)',
        }}
      />

      {/* Glassmorphism card */}
      <div
        className="relative max-w-md w-full rounded-2xl p-8 mx-4"
        style={{
          background: 'rgba(255, 255, 255, 0.10)',
          backdropFilter: 'blur(18px)',
          WebkitBackdropFilter: 'blur(18px)',
          border: '1px solid rgba(255,255,255,0.22)',
          boxShadow: '0 8px 48px rgba(80,0,200,0.22), 0 1.5px 8px rgba(0,0,0,0.18)',
        }}
      >
        {/* Logo/brand area */}
        <div className="flex flex-col items-center mb-6">
          <div
            className="w-14 h-14 rounded-full flex items-center justify-center mb-3"
            style={{
              background: 'linear-gradient(135deg, #6C63FF 0%, #3ECFDF 100%)',
              boxShadow: '0 4px 20px rgba(108,99,255,0.5)',
            }}
          >
            <span style={{ fontSize: 26 }}>🎯</span>
          </div>
          <h2
            className="text-3xl font-bold text-center"
            style={{
              background: 'linear-gradient(90deg, #a78bfa 0%, #38bdf8 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              letterSpacing: '0.02em',
            }}
          >
            Login to AceIt
          </h2>
          <p className="text-sm mt-1" style={{ color: 'rgba(200,210,255,0.75)' }}>
            Your placement preparation partner
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <div className="mb-6 flex justify-center">
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={handleGoogleError}
            useOneTap
          />
        </div>

        <div className="relative mb-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t" style={{ borderColor: 'rgba(255,255,255,0.2)' }}></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2" style={{ background: 'transparent', color: 'rgba(200,210,255,0.7)' }}>
              Or continue with email
            </span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium" style={{ color: 'rgba(220,230,255,0.90)' }}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full rounded-md p-2 border focus:outline-none focus:ring-2"
              style={{
                background: 'rgba(255,255,255,0.12)',
                border: '1px solid rgba(255,255,255,0.22)',
                color: '#fff',
                focusRingColor: '#6C63FF',
              }}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium" style={{ color: 'rgba(220,230,255,0.90)' }}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full rounded-md p-2 border focus:outline-none focus:ring-2"
              style={{
                background: 'rgba(255,255,255,0.12)',
                border: '1px solid rgba(255,255,255,0.22)',
                color: '#fff',
              }}
              required
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full text-white py-2 px-4 rounded-md transition duration-200 disabled:opacity-50"
            style={{
              background: 'linear-gradient(90deg, #6C63FF 0%, #3ECFDF 100%)',
              boxShadow: '0 4px 18px rgba(108,99,255,0.4)',
              fontWeight: 600,
              letterSpacing: '0.03em',
            }}
          >
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
          <p className="text-center text-sm mt-4" style={{ color: 'rgba(200,210,255,0.75)' }}>
            Don't have an account?{' '}
            <a href="/register" className="hover:underline font-semibold" style={{ color: '#a78bfa' }}>
              Register here
            </a>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Login;