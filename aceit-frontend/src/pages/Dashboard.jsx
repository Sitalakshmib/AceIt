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
  BarChart3, PieChart as PieChartIcon, Activity
} from 'lucide-react';

import { analyticsAPI } from '../services/api';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [progressData, setProgressData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      if (!user?.id) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await analyticsAPI.getDashboard();
        setProgressData(response.data);
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard. Showing limited info.');
        // Fallback or empty state handled by progressData being null
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, [user]);

  if (loading) {
    return (
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">Welcome back, {user?.email || 'User'}!</h1>
        <div className="text-center py-20">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500"></div>
          <p className="mt-4 text-gray-600">Loading your personalized dashboard...</p>
        </div>
      </div>
    );
  }

  if (!progressData) {
    return (
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">Welcome to AceIt!</h1>
        <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
          <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <Brain className="h-12 w-12 text-blue-600" />
          </div>
          <h2 className="text-2xl font-bold mb-4">Start Your Learning Journey</h2>
          <p className="text-gray-600 mb-8">No progress data yet. Start practicing to track your improvement!</p>
          <button
            onClick={() => navigate('/aptitude')}
            className="bg-blue-600 text-white px-8 py-3 rounded-xl font-medium hover:bg-blue-700"
          >
            Begin First Lesson
          </button>
        </div>
      </div>
    );
  }

  // Color palettes
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];
  const SKILL_COLORS = ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B', '#EF4444', '#06B6D4'];

  // Prepare weekly activity data for chart
  const weeklyData = progressData.weekly_activity.map(day => ({
    day: new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' }),
    aptitude: day.aptitude,
    coding: day.coding,
    score: day.score
  }));

  // Prepare skill data for chart
  const skillData = progressData.skill_distribution;

  // Stats cards
  const stats = [
    {
      title: 'Overall Score',
      value: `${progressData.overall_score}%`,
      color: 'bg-gradient-to-r from-blue-500 to-cyan-500',
      icon: <TrendingUp className="h-6 w-6" />,
      description: 'Your overall performance'
    },
    {
      title: 'Daily Streak',
      value: `${progressData.daily_streak} days`,
      color: 'bg-gradient-to-r from-green-500 to-emerald-500',
      icon: <Zap className="h-6 w-6" />,
      description: 'Consecutive practice days'
    },
    {
      title: 'Total Practice',
      value: `${Math.round(progressData.total_time_spent / 60)}h`,
      color: 'bg-gradient-to-r from-purple-500 to-pink-500',
      icon: <Clock className="h-6 w-6" />,
      description: 'Time spent learning'
    },
    {
      title: 'Accuracy',
      value: `${progressData.aptitude.accuracy}%`,
      color: 'bg-gradient-to-r from-orange-500 to-red-500',
      icon: <Award className="h-6 w-6" />,
      description: 'Average success rate'
    },
  ];

  const moduleStats = [
    {
      title: 'Aptitude',
      score: progressData.aptitude.average_score,
      total: progressData.aptitude.tests_taken,
      color: 'bg-blue-100 text-blue-600',
      icon: '🧠',
      path: '/aptitude'
    },
    {
      title: 'Coding',
      score: progressData.coding.average_success_rate,
      total: progressData.coding.problems_attempted,
      color: 'bg-green-100 text-green-600',
      icon: '💻',
      path: '/coding'
    },
    {
      title: 'Interviews',
      score: 65,
      total: 3,
      color: 'bg-purple-100 text-purple-600',
      icon: '🎤',
      path: '/interview'
    },
  ];

  return (
    <div className="p-4 md:p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.username || user?.email || 'Learner'}! 👋</h1>
          <p className="text-gray-600 mt-2">
            Your personalized learning dashboard
            {progressData.overall_score === 0 && (
              <span className="ml-2 text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                Start Practicing!
              </span>
            )}
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex items-center space-x-2">
          <div className="text-sm text-gray-500">
            Last updated: {new Date().toLocaleDateString()}
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-gray-500 text-sm font-medium">{stat.title}</p>
                <p className="text-3xl font-bold mt-2">{stat.value}</p>
                <p className="text-gray-400 text-sm mt-1">{stat.description}</p>
              </div>
              <div className={`p-3 rounded-full ${stat.color} text-white`}>
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Weekly Activity Chart */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <div className="flex items-center mb-6">
            <Activity className="h-5 w-5 text-blue-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Weekly Activity</h3>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="day" stroke="#666" />
                <YAxis stroke="#666" />
                <Tooltip />
                <Legend />
                <Bar dataKey="aptitude" fill="#3B82F6" name="Aptitude Qs" />
                <Bar dataKey="coding" fill="#10B981" name="Coding Problems" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Skill Distribution Chart */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <div className="flex items-center mb-6">
            <PieChartIcon className="h-5 w-5 text-green-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Skill Distribution</h3>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={skillData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, score }) => `${name}: ${score}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="score"
                >
                  {skillData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={SKILL_COLORS[index % SKILL_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [`${value}%`, 'Score']} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Module Performance & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* Module Performance */}
        <div className="bg-white rounded-2xl shadow-lg p-6 lg:col-span-2">
          <div className="flex items-center mb-6">
            <BarChart3 className="h-5 w-5 text-purple-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Module Performance</h3>
          </div>
          <div className="space-y-4">
            {moduleStats.map((module, index) => (
              <div
                key={index}
                onClick={() => navigate(module.path)}
                className="flex items-center justify-between p-4 rounded-xl hover:bg-gray-50 cursor-pointer transition-colors border border-gray-100"
              >
                <div className="flex items-center">
                  <span className="text-2xl mr-4">{module.icon}</span>
                  <div>
                    <h4 className="font-medium text-gray-900">{module.title}</h4>
                    <div className="flex items-center mt-1">
                      <div className="w-48 bg-gray-200 rounded-full h-2">
                        <div
                          className="h-full rounded-full"
                          style={{
                            width: `${module.score}%`,
                            backgroundColor: module.color.split(' ')[1].replace('text-', 'bg-')
                          }}
                        ></div>
                      </div>
                      <span className="ml-3 text-sm font-medium">{module.score}%</span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold">{module.total}</div>
                  <div className="text-sm text-gray-500">attempts</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <div className="flex items-center mb-6">
            <Calendar className="h-5 w-5 text-orange-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
          </div>
          <div className="space-y-4">
            {progressData.recent_activity.length > 0 ? (
              progressData.recent_activity.map((activity, index) => (
                <div key={index} className="flex items-start p-3 rounded-lg bg-gray-50">
                  <div className="flex-shrink-0 mt-1">
                    {activity.type === 'aptitude_test' && (
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <Brain className="h-4 w-4 text-blue-600" />
                      </div>
                    )}
                    {activity.type === 'coding_problem' && (
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                        <Target className="h-4 w-4 text-green-600" />
                      </div>
                    )}
                    {activity.type === 'mock_interview' && (
                      <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                        <Users className="h-4 w-4 text-purple-600" />
                      </div>
                    )}
                  </div>
                  <div className="ml-3">
                    <p className="font-medium text-gray-900">
                      {activity.type === 'coding_problem' ? activity.problem :
                        activity.type === 'aptitude_test' ? 'Aptitude Test' : 'Mock Interview'}
                    </p>
                    <p className="text-sm text-gray-500">
                      Score: {activity.score}%
                      {activity.success !== undefined && (
                        <span className={`ml-2 px-1 rounded text-xs ${activity.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                          {activity.success ? '✓' : '✗'}
                        </span>
                      )}
                    </p>
                    <p className="text-xs text-gray-400 mt-1">{activity.date}</p>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <AlertCircle className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-500">No recent activity</p>
                <p className="text-sm text-gray-400 mt-1">Start practicing to see your progress</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <div className="flex items-center mb-6">
          <Star className="h-5 w-5 text-indigo-500 mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">Personalized Recommendations</h3>
        </div>
        <div className="space-y-4">
          {progressData.recommendations.map((recommendation, index) => (
            <div key={index} className="flex items-start p-3 rounded-lg bg-indigo-50">
              <div className="flex-shrink-0 mt-1">
                <div className="w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center">
                  <span className="text-indigo-600 text-sm font-bold">{index + 1}</span>
                </div>
              </div>
              <p className="ml-3 text-sm text-gray-700">{recommendation}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Action Buttons */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <button
          onClick={() => navigate('/aptitude')}
          className="bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-4 rounded-xl font-medium hover:shadow-lg transition-all flex items-center justify-center"
        >
          <Brain className="h-5 w-5 mr-2" />
          Practice Aptitude
        </button>
        <button
          onClick={() => navigate('/coding')}
          className="bg-gradient-to-r from-green-600 to-emerald-700 text-white py-3 px-4 rounded-xl font-medium hover:shadow-lg transition-all flex items-center justify-center"
        >
          <Target className="h-5 w-5 mr-2" />
          Solve Problems
        </button>
        <button
          onClick={() => navigate('/interview')}
          className="bg-gradient-to-r from-purple-600 to-purple-700 text-white py-3 px-4 rounded-xl font-medium hover:shadow-lg transition-all flex items-center justify-center"
        >
          <Users className="h-5 w-5 mr-2" />
          Mock Interview
        </button>
        <button
          onClick={() => navigate('/resume')}
          className="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white py-3 px-4 rounded-xl font-medium hover:shadow-lg transition-all flex items-center justify-center"
        >
          <Award className="h-5 w-5 mr-2" />
          Analyze Resume
        </button>
      </div>
    </div>
  );
};

export default Dashboard;