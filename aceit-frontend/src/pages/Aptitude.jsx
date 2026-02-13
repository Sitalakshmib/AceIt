import React, { useState } from 'react';
import { analyticsAPI, mockTestAPI } from '../services/api';
import PracticeMode from '../components/PracticeMode';
import MockTestSection from './MockTest';
import AnalyticsSection from './Analytics';
import AICoachChat from '../components/AICoachChat';
import { BookOpen, Award, BarChart2, ArrowLeft, Target, Rocket, Brain } from 'lucide-react';

const Aptitude = () => {
  const [activeView, setActiveView] = useState('intro'); // 'intro', 'practice', 'mock-test', 'analytics'

  const handleNavigate = (view) => {
    setActiveView(view);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handeBack = () => {
    setActiveView('intro');
  };

  const getPageTitle = () => {
    switch (activeView) {
      case 'practice': return 'Practice Mode';
      case 'mock-test': return 'Mock Tests';
      case 'analytics': return 'Performance Analytics';
      default: return 'Aptitude Module';
    }
  };

  const getActiveComponent = () => {
    switch (activeView) {
      case 'practice': return <PracticeMode />;
      case 'mock-test': return <MockTestSection />;
      case 'analytics': return <AnalyticsSection />;
      default: return null;
    }
  };

  return (
    <div className="min-h-screen">
      {activeView === 'intro' ? (
        <div className="p-8 max-w-7xl mx-auto animate-in fade-in duration-500">
          <div className="mb-12 text-center">
            <div className="inline-block p-3 bg-blue-50 rounded-2xl mb-4">
              <Target className="h-8 w-8 text-blue-600" />
            </div>
            <h1 className="text-4xl font-black text-gray-900 mb-4 tracking-tight">Aptitude Mastery</h1>
            <p className="text-lg text-gray-500 max-w-2xl mx-auto">
              Your personalized path to cracking aptitude tests. Practice with adaptive questions, simulate real exams, and track your AI-driven growth.
            </p>

            {/* Analytics Entry Button */}
            <div className="mt-6 flex justify-center">
              <button
                onClick={() => handleNavigate('analytics')}
                className="flex items-center gap-2 px-6 py-3 bg-white border border-gray-200 text-gray-700 font-semibold rounded-full hover:bg-gray-50 hover:border-gray-300 transition-all shadow-sm group"
              >
                <BarChart2 className="h-5 w-5 text-blue-600 group-hover:scale-110 transition-transform" />
                View Performance Analytics
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Practice Card */}
            <div
              onClick={() => handleNavigate('practice')}
              className="group relative bg-white p-8 rounded-[2rem] shadow-xl shadow-gray-100 border border-gray-100 hover:shadow-2xl hover:scale-[1.02] transition-all cursor-pointer overflow-hidden"
            >
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-100 rounded-bl-[4rem] opacity-50 transition-transform group-hover:scale-110" />
              <div className="relative z-10">
                <div className="h-16 w-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mb-8 shadow-sm group-hover:bg-blue-600 group-hover:text-white transition-colors duration-300">
                  <BookOpen className="h-8 w-8" />
                </div>
                <h3 className="text-2xl font-bold text-gray-800 mb-3">Practice Mode</h3>
                <p className="text-gray-500 mb-8 leading-relaxed">Master topics one by one with our adaptive question engine. Perfect for daily learning.</p>
                <span className="inline-flex items-center text-blue-600 font-bold group-hover:translate-x-2 transition-transform">
                  Start Practicing <Rocket className="ml-2 h-4 w-4" />
                </span>
              </div>
            </div>

            {/* Mock Test Card */}
            <div
              onClick={() => handleNavigate('mock-test')}
              className="group relative bg-white p-8 rounded-[2rem] shadow-xl shadow-gray-100 border border-gray-100 hover:shadow-2xl hover:scale-[1.02] transition-all cursor-pointer overflow-hidden"
            >
              <div className="absolute top-0 right-0 w-32 h-32 bg-purple-100 rounded-bl-[4rem] opacity-50 transition-transform group-hover:scale-110" />
              <div className="relative z-10">
                <div className="h-16 w-16 bg-purple-50 text-purple-600 rounded-2xl flex items-center justify-center mb-8 shadow-sm group-hover:bg-purple-600 group-hover:text-white transition-colors duration-300">
                  <Award className="h-8 w-8" />
                </div>
                <h3 className="text-2xl font-bold text-gray-800 mb-3">Mock Tests</h3>
                <p className="text-gray-500 mb-8 leading-relaxed">Simulate real exam conditions with timed full-length tests and instant scoring.</p>
                <span className="inline-flex items-center text-purple-600 font-bold group-hover:translate-x-2 transition-transform">
                  Take a Test <Rocket className="ml-2 h-4 w-4" />
                </span>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-6 max-w-7xl mx-auto animate-in slide-in-from-right-10 fade-in duration-500">
          <div className="mb-6 flex items-center">
            <button
              onClick={handeBack}
              className="mr-4 p-2 rounded-xl text-gray-500 hover:bg-gray-100 hover:text-blue-600 transition-colors"
              title="Back to Menu"
            >
              <ArrowLeft className="h-6 w-6" />
            </button>
            <div>
              <button onClick={handeBack} className="text-sm font-semibold text-gray-500 hover:text-blue-600 mb-1 active:text-blue-700">
                Aptitude Module
              </button>
              <h2 className="text-2xl font-bold text-gray-800">{getPageTitle()}</h2>
            </div>
          </div>

          <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-1">
            {getActiveComponent()}
          </div>
        </div>
      )}

      {/* AI Coach Overlay - Available on Intro and Practice pages. Hidden in mock-test to prevent cheating. */}
      {(activeView === 'intro' || activeView === 'practice') && <AICoachChat compact={activeView === 'practice'} />}
    </div>
  );
};

export default Aptitude;