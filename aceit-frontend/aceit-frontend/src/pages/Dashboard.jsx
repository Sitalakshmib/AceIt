import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const stats = [
    { title: 'Aptitude Score', value: '75%', color: 'bg-blue-500', path: '/aptitude' },
    { title: 'Coding Problems Solved', value: '12/20', color: 'bg-green-500', path: '/coding' },
    { title: 'Mock Interviews', value: '3', color: 'bg-purple-500', path: '/interview' },
    { title: 'Overall Progress', value: '60%', color: 'bg-orange-500', path: '/' },
  ];

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Welcome back, {user?.name}!</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <div 
            key={index} 
            className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => navigate(stat.path)}
          >
            <div className={`w-12 h-12 ${stat.color} rounded-full flex items-center justify-center text-white mb-4`}>
              {stat.value}
            </div>
            <h3 className="text-lg font-semibold text-gray-700">{stat.title}</h3>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Aptitude Practice</h3>
          <p className="text-gray-600 mb-4">Improve your quantitative and logical reasoning skills</p>
          <button 
            onClick={() => navigate('/aptitude')}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Start Practice
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Coding Challenges</h3>
          <p className="text-gray-600 mb-4">Solve coding problems with instant feedback</p>
          <button 
            onClick={() => navigate('/coding')}
            className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
          >
            Solve Problems
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Mock Interview</h3>
          <p className="text-gray-600 mb-4">Practice with AI-powered interview simulator</p>
          <button 
            onClick={() => navigate('/interview')}
            className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700"
          >
            Start Interview
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Resume Analyzer</h3>
          <p className="text-gray-600 mb-4">Get AI-powered feedback on your resume</p>
          <button 
            onClick={() => navigate('/resume')}
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
          >
            Analyze Resume
        </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;