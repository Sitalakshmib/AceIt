import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import {
  TrendingUp, Target, Clock, Award, Brain, Users,
  Calendar, Zap, Star, AlertCircle, Trophy,
  BarChart3, PieChart as PieChartIcon, Activity, LayoutDashboard,
  Code, Cpu, Camera
} from 'lucide-react';

import { analyticsAPI } from '../services/api';
import GDPracticeWidget from '../components/Dashboard/GDPracticeWidget';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [progressData, setProgressData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setLoading(true);
        // Unified API handles userId internally (session fallback)
        const response = await analyticsAPI.getUnifiedAnalytics();
        if (response.data && response.data.data) {
          setProgressData(response.data.data);
        } else {
          setProgressData(response.data);
        }
      } catch (err) {
        console.error('Failed to fetch unified dashboard data:', err);
        setError('Failed to load dashboard.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, [user]);

  if (loading) {
    return (
      <div className="p-8 min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
          <div className="text-xl font-bold text-gray-800">Loading your performance...</div>
        </div>
      </div>
    );
  }

  if (!progressData) {
    return (
      <div className="p-8 min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-[2rem] shadow-xl p-12 text-center max-w-lg">
          <AlertCircle className="h-12 w-12 text-orange-500 mx-auto mb-4" />
          <h2 className="text-2xl font-black mb-4">No Analytics Yet</h2>
          <p className="text-gray-600 mb-8">Start practicing to see your performance breakdown here!</p>
          <button onClick={() => navigate('/aptitude')} className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold">
            Start Learning
          </button>
        </div>
      </div>
    );
  }

  const { overall_summary, module_performance, recent_activity } = progressData;

  // Calculate Overall Score (Average of Aptitude, Coding, and Technical/HR/Video Interviews)
  // Higher weight for modules that actually have data
  const scoringModules = module_performance.filter(m => m.has_data);
  const averageScore = scoringModules.length > 0
    ? Math.round(scoringModules.reduce((acc, m) => acc + m.performance_score, 0) / scoringModules.length)
    : 0;

  const getModuleIcon = (name) => {
    switch (name) {
      case 'Aptitude': return <Brain className="h-6 w-6" />;
      case 'Coding': return <Code className="h-6 w-6" />;
      case 'Technical Interview': return <Cpu className="h-6 w-6" />;
      case 'HR Interview': return <Users className="h-6 w-6" />;
      case 'Video Presence': return <Camera className="h-6 w-6" />;
      default: return <BarChart3 className="h-6 w-6" />;
    }
  };

  const getModuleColor = (name) => {
    switch (name) {
      case 'Aptitude': return 'from-blue-500 to-indigo-600';
      case 'Coding': return 'from-purple-500 to-pink-600';
      case 'Technical Interview': return 'from-orange-500 to-red-600';
      case 'HR Interview': return 'from-emerald-500 to-teal-600';
      case 'Video Presence': return 'from-cyan-500 to-blue-600';
      default: return 'from-gray-500 to-slate-600';
    }
  };

  return (
    <div className="p-8 min-h-screen bg-gray-50">
      {/* 1. OVERALL PERFORMANCE HEADER */}
      <div className="max-w-7xl mx-auto mb-10">
        <div className="bg-white rounded-[2.5rem] shadow-xl shadow-gray-200/50 p-8 md:p-10 border border-gray-100 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-bl-full opacity-60"></div>

          <div className="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
            {/* User Intro */}
            <div className="text-center md:text-left">
              <div className="inline-block p-4 bg-blue-100 text-blue-600 rounded-2xl mb-4">
                <LayoutDashboard className="h-8 w-8" />
              </div>
              <h1 className="text-3xl md:text-4xl font-black text-gray-900 leading-tight">
                Hey, {user?.username || 'Learner'}!
              </h1>
              <p className="text-gray-500 mt-2 font-medium">Ready to master your skills today?</p>
            </div>

            {/* Overall Analytics Circle */}
            <div className="flex justify-center">
              <div className="relative w-40 h-40">
                <svg className="w-full h-full transform -rotate-90">
                  <circle
                    cx="80" cy="80" r="70"
                    stroke="currentColor" strokeWidth="12" fill="transparent"
                    className="text-gray-100"
                  />
                  <circle
                    cx="80" cy="80" r="70"
                    stroke="currentColor" strokeWidth="12" fill="transparent"
                    strokeDasharray={440}
                    strokeDashoffset={440 - (440 * averageScore) / 100}
                    strokeLinecap="round"
                    className="text-blue-600 transition-all duration-1000 ease-out"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-3xl font-black text-gray-900">{averageScore}%</span>
                  <span className="text-[10px] uppercase font-bold text-gray-400 tracking-widest">Overall</span>
                </div>
              </div>
            </div>

            {/* Summary Stats */}
            <div className="flex flex-col gap-4">
              <div className="bg-green-50 rounded-2xl p-4 flex items-center justify-between border border-green-100">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 text-green-600 rounded-lg mr-3">
                    <Zap className="h-5 w-5" />
                  </div>
                  <span className="font-bold text-gray-700">Current Streak</span>
                </div>
                <span className="text-2xl font-black text-green-600">{overall_summary.practice_streak} Days</span>
              </div>

              <div className="bg-purple-50 rounded-2xl p-4 flex items-center justify-between border border-purple-100">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 text-purple-600 rounded-lg mr-3">
                    <Clock className="h-5 w-5" />
                  </div>
                  <span className="font-bold text-gray-700">Total Practice</span>
                </div>
                <span className="text-2xl font-black text-purple-600">{overall_summary.total_time_hours}h</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto">
        <h2 className="text-2xl font-black text-gray-900 mb-8 flex items-center">
          <Trophy className="h-6 w-6 text-yellow-500 mr-3" />
          Performance Breakdown
        </h2>

        {/* 2. MODULE BREAKDOWN GRID */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {module_performance.filter(m => ['Aptitude', 'Coding', 'Technical Interview', 'HR Interview', 'Video Presence'].includes(m.module)).map((module, index) => (
            <div
              key={index}
              className={`bg-white rounded-[2.5rem] shadow-xl shadow-gray-100 border border-gray-100 p-8 flex flex-col h-full hover:scale-[1.02] transition-all duration-300 relative overflow-hidden ${!module.has_data ? 'opacity-70' : ''}`}
            >
              {/* Module Header */}
              <div className="flex justify-between items-start mb-6">
                <div className={`p-4 rounded-2xl bg-gradient-to-br ${getModuleColor(module.module)} text-white shadow-lg`}>
                  {getModuleIcon(module.module)}
                </div>
                <div className="text-right">
                  <span className={`text-xs font-black uppercase tracking-wider px-3 py-1 rounded-full ${module.performance_level === 'Good' ? 'bg-green-100 text-green-600' :
                    module.performance_level === 'Moderate' ? 'bg-orange-100 text-orange-600' :
                      'bg-gray-100 text-gray-400'
                    }`}>
                    {module.performance_level}
                  </span>
                </div>
              </div>

              <h3 className="text-xl font-black text-gray-900 mb-2">{module.module}</h3>
              <p className="text-sm text-gray-500 mb-6 font-medium">
                {module.sessions} sessions completed
              </p>

              {/* Progress Section */}
              <div className="mt-auto">
                <div className="flex justify-between items-end mb-2">
                  <span className="text-sm font-bold text-gray-400">
                    {module.module === 'Coding' ? 'Progress' : 'Success Rate'}
                  </span>
                  <span className="text-2xl font-black text-gray-900">
                    {Math.round(module.module === 'Coding' && module.progress_percentage !== undefined
                      ? module.progress_percentage
                      : module.performance_score)}%
                  </span>
                </div>
                <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full bg-gradient-to-r ${getModuleColor(module.module)} transition-all duration-1000`}
                    style={{
                      width: `${module.module === 'Coding' && module.progress_percentage !== undefined
                        ? module.progress_percentage
                        : module.performance_score}%`
                    }}
                  ></div>
                </div>
              </div>

              {/* Action Button */}
              <button
                onClick={() => navigate(`/${module.module.toLowerCase().replace(' interview', '').replace(' presence', '')}`)}
                className="mt-8 flex items-center justify-center w-full py-4 rounded-2xl font-bold border-2 border-gray-100 text-gray-600 hover:border-gray-200 hover:bg-gray-50 transition-all"
              >
                Go to Module
              </button>
            </div>
          ))}
        </div>

        {/* 3. RECENT ACTIVITY & TRENDS */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Activity Timeline */}
          <div className="lg:col-span-2 bg-white rounded-[2.5rem] shadow-xl shadow-gray-100 p-10 border border-gray-100">
            <h3 className="text-2xl font-black text-gray-900 mb-8 flex items-center">
              <Calendar className="h-6 w-6 text-blue-600 mr-3" />
              Recent Activity
            </h3>

            <div className="space-y-6">
              {recent_activity.length > 0 ? recent_activity.map((activity, idx) => (
                <div key={idx} className="flex items-center p-5 rounded-3xl bg-gray-50/50 border border-gray-100/50 hover:bg-white hover:shadow-lg transition-all">
                  <div className={`p-4 rounded-2xl mr-5 ${activity.module === 'Aptitude' ? 'bg-blue-100 text-blue-600' :
                    activity.module === 'Coding' ? 'bg-green-100 text-green-600' :
                      'bg-purple-100 text-purple-600'
                    }`}>
                    {getModuleIcon(activity.module)}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-900">{activity.type}</h4>
                    <p className="text-sm text-gray-500">{new Date(activity.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-black text-gray-900">{activity.result}</span>
                    <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest mt-1">Status</p>
                  </div>
                </div>
              )) : (
                <div className="text-center py-10 text-gray-400">
                  No recent activity found.
                </div>
              )}
            </div>
          </div>

          {/* Tips Section */}
          <div className="bg-gradient-to-br from-indigo-600 to-blue-700 rounded-[2.5rem] shadow-xl p-10 text-white relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-bl-full"></div>
            <div className="relative z-10 flex flex-col h-full">
              <div className="p-3 bg-white/20 rounded-xl w-fit mb-6">
                <Brain className="h-6 w-6" />
              </div>
              <h3 className="text-2xl font-black mb-4">Daily Tip</h3>
              <p className="text-blue-50 text-lg leading-relaxed mb-10">
                "{progressData.weak_areas?.[0]?.suggestion || "Focus on consistency to see rapid improvement in your mock interview scores."}"
              </p>

              <div className="mt-auto pt-8 border-t border-white/10">
                <button
                  onClick={() => navigate('/aptitude')}
                  className="w-full bg-white text-blue-600 py-4 rounded-2xl font-black shadow-lg hover:scale-105 transition-all"
                >
                  Quick Practice
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
