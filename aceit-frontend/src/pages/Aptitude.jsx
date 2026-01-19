import React, { useState } from 'react';
import { analyticsAPI, mockTestAPI } from '../services/api';
import PracticeMode from '../components/PracticeMode';
import MockTestSection from './MockTest';
import AnalyticsSection from './Analytics';

const Aptitude = () => {
  const [activeTab, setActiveTab] = useState('practice');

  const tabs = [
    { id: 'practice', label: 'Practice Mode', icon: '🎯' },
    { id: 'mock-test', label: 'Mock Tests', icon: '📝' },
    { id: 'analytics', label: 'Analytics', icon: '📈' }
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Aptitude Module</h1>
        <p className="text-gray-600">Adaptive learning powered by AI - Practice, Test, and Track your progress</p>
      </div>

      <div className="bg-white rounded-lg shadow-md mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 py-4 px-6 text-center font-medium text-sm transition-all ${activeTab === tab.id
                  ? 'border-b-2 border-blue-500 text-blue-600 bg-blue-50'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                  }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'practice' && <PracticeMode />}
          {activeTab === 'mock-test' && <MockTestSection />}
          {activeTab === 'analytics' && <AnalyticsSection />}
        </div>
      </div>
    </div>
  );
};

export default Aptitude;