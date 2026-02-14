import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { LayoutDashboard, BrainCircuit, Code2, Video, FileText, LogOut, Menu, X, User, Settings, ChevronRight, Bell, HelpCircle, Users } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();

  const location = useLocation();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  const navItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/aptitude', label: 'Aptitude', icon: BrainCircuit },
    { path: '/coding', label: 'Coding', icon: Code2 },
    { path: '/group-discussion', label: 'Group Discussion', icon: Users },
    { path: '/interview', label: 'Mock Interview', icon: Video },
    { path: '/resume', label: 'Resume Analyzer', icon: FileText },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <>
      <nav className="bg-gradient-to-r from-slate-900 to-blue-900 shadow-xl sticky top-0 z-50 border-b border-amber-50/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and Brand */}
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <div className="w-10 h-10 bg-amber-50 rounded-xl flex items-center justify-center shadow-lg">
                  <span className="text-blue-900 font-bold text-lg">AI</span>
                </div>
                <div>
                  <h1 className="text-xl font-bold text-white">AceIt</h1>
                  <p className="text-amber-100 text-xs">Smart Placement Partner</p>
                </div>
              </div>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${location.pathname === item.path
                      ? 'bg-amber-50 text-blue-900 shadow-lg transform scale-105'
                      : 'text-amber-100 hover:bg-white/10 hover:text-white hover:shadow-md'
                      }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </div>

            {/* Profile Sidebar Trigger - Desktop */}
            <div className="hidden md:flex items-center space-x-4">
              <button
                onClick={() => setIsProfileOpen(true)}
                className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-700 rounded-full pl-1 pr-3 py-1 border border-slate-700 transition-all duration-200 group"
              >
                <div className="w-8 h-8 bg-amber-50 rounded-full flex items-center justify-center shadow-sm group-hover:bg-white transition-colors">
                  <span className="text-blue-900 text-sm font-bold">
                    {user?.username?.charAt(0) || user?.email?.charAt(0) || 'U'}
                  </span>
                </div>
                <span className="text-amber-50 text-sm font-medium group-hover:text-white">Profile</span>
              </button>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center space-x-2">
              <button
                onClick={toggleMobileMenu}
                className="text-amber-50 p-2 rounded-lg hover:bg-slate-800 transition-colors duration-200"
              >
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>

          {/* Mobile Navigation Menu */}
          {isMobileMenuOpen && (
            <div className="md:hidden bg-slate-900 rounded-2xl shadow-2xl mt-2 py-4 transform origin-top transition-all duration-300 border border-slate-800">
              <div className="px-4 space-y-2">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      onClick={() => setIsMobileMenuOpen(false)}
                      className={`flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${location.pathname === item.path
                        ? 'bg-amber-50 text-blue-900 shadow-lg'
                        : 'text-amber-100 hover:bg-slate-800'
                        }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}

                {/* Mobile Profile Trigger (just to open sidebar) */}
                <button
                  onClick={() => { setIsMobileMenuOpen(false); setIsProfileOpen(true); }}
                  className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-medium text-amber-100 hover:bg-slate-800 transition-all duration-200 mt-4 border-t border-slate-800 pt-4"
                >
                  <User className="w-5 h-5" />
                  <span>My Profile</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Profile Sidebar (Right Drawer) */}
      <div className={`fixed inset-0 z-[60] overflow-hidden ${isProfileOpen ? 'pointer-events-auto' : 'pointer-events-none'}`}>
        <div className="absolute inset-0 overflow-hidden">
          {/* Overlay */}
          <div
            className={`absolute inset-0 bg-slate-900/50 backdrop-blur-sm transition-opacity duration-300 ${isProfileOpen ? 'opacity-100' : 'opacity-0'}`}
            onClick={() => setIsProfileOpen(false)}
          />

          {/* Drawer Panel */}
          <div className={`fixed inset-y-0 right-0 max-w-md w-full flex pointer-events-auto transform transition-transform duration-300 ease-in-out ${isProfileOpen ? 'translate-x-0' : 'translate-x-full'}`}>
            <div className="w-full h-full bg-white shadow-2xl flex flex-col">

              {/* Header */}
              <div className="h-24 bg-gradient-to-r from-slate-900 to-blue-900 p-6 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-amber-50 rounded-full flex items-center justify-center shadow-lg border-2 border-slate-100">
                    <span className="text-blue-900 text-xl font-bold">
                      {user?.username?.charAt(0) || user?.email?.charAt(0) || 'U'}
                    </span>
                  </div>
                  <div>
                    <h2 className="text-white font-bold text-lg">{user?.username || 'User'}</h2>
                    <p className="text-blue-200 text-sm">{user?.email}</p>
                  </div>
                </div>
                <button
                  onClick={() => setIsProfileOpen(false)}
                  className="text-white/80 hover:text-white hover:bg-white/10 rounded-full p-2 transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {/* Body - Practice Motivation */}
              <div className="flex-1 overflow-y-auto p-6 bg-slate-50">
                <div className="space-y-4">
                  <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 pl-2">Practice Insights</h3>

                  <div className="bg-blue-50 border border-blue-100 rounded-2xl p-4 shadow-sm">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white">
                        <BrainCircuit className="w-5 h-5" />
                      </div>
                      <h4 className="font-bold text-blue-900 text-sm">Consistency is Key</h4>
                    </div>
                    <p className="text-blue-800 text-xs leading-relaxed">
                      Practicing for just 15 minutes every day can significantly improve your placement readiness!
                    </p>
                  </div>

                  <div className="bg-amber-50 border border-amber-100 rounded-2xl p-4 shadow-sm">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className="w-8 h-8 bg-amber-500 rounded-lg flex items-center justify-center text-white">
                        <Code2 className="w-5 h-5" />
                      </div>
                      <h4 className="font-bold text-amber-900 text-sm">Coding Tip</h4>
                    </div>
                    <p className="text-amber-800 text-xs leading-relaxed">
                      Try solving at least one medium-level problem today to keep your logic sharp.
                    </p>
                  </div>

                  <div className="bg-purple-50 border border-purple-100 rounded-2xl p-4 shadow-sm">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center text-white">
                        <Video className="w-5 h-5" />
                      </div>
                      <h4 className="font-bold text-purple-900 text-sm">Mock Interview</h4>
                    </div>
                    <p className="text-purple-800 text-xs leading-relaxed">
                      Record a mock interview session to analyze your body language and confidence level.
                    </p>
                  </div>

                </div>
              </div>

              {/* Footer / Logout */}
              <div className="p-6 bg-white border-t border-slate-200">
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center justify-center space-x-2 bg-red-50 text-red-600 px-4 py-3 rounded-xl text-sm font-bold hover:bg-red-100 transition-colors duration-200"
                >
                  <LogOut className="w-5 h-5" />
                  <span>Log Out</span>
                </button>
                <p className="text-center text-xs text-slate-400 mt-4">AceIt v1.0.0</p>
              </div>

            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Navbar;