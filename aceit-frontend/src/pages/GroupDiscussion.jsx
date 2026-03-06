import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import GDPractice from '../components/GDPractice';
import GDTopicAnalysis from '../components/GDTopicAnalysis';
import { Users, MessageSquare, Search, ArrowLeft, Rocket, Target } from 'lucide-react';

const GroupDiscussion = () => {
    const navigate = useNavigate();
    const [activeView, setActiveView] = useState('intro'); // 'intro', 'practice', 'analysis'

    const handleNavigate = (view) => {
        setActiveView(view);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleBack = () => {
        setActiveView('intro');
    };

    const getPageTitle = () => {
        switch (activeView) {
            case 'practice': return 'Practice GD';
            case 'analysis': return 'Topic Analysis';
            default: return 'Group Discussion';
        }
    };

    const getActiveComponent = () => {
        switch (activeView) {
            case 'practice': return <GDPractice />;
            case 'analysis': return <GDTopicAnalysis />;
            default: return null;
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-purple-50 relative">
            {activeView === 'intro' ? (
                <div className="p-8 max-w-7xl mx-auto animate-in fade-in duration-500">
                    {/* Back to Dashboard Button */}
                    <button
                        onClick={() => navigate('/')}
                        className="absolute top-8 left-8 flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 text-gray-600 font-bold rounded-xl hover:bg-gray-50 hover:text-purple-600 transition-all shadow-sm group z-40"

                    >
                        <ArrowLeft className="h-5 w-5 group-hover:-translate-x-1 transition-transform" />
                        Dashboard
                    </button>

                    <div className="mb-12 text-center">
                        <div className="inline-block p-3 bg-purple-50 rounded-2xl mb-4">
                            <Users className="h-8 w-8 text-purple-600" />
                        </div>
                        <h1 className="text-4xl font-black text-gray-900 mb-4 tracking-tight">Group Discussion Mastery</h1>
                        <p className="text-lg text-gray-500 max-w-2xl mx-auto">
                            Elevate your communication skills with AI-powered practice and comprehensive topic analysis.
                            Perfect your GD performance for placements and MBA interviews.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
                        {/* Practice GD Card */}
                        <div
                            onClick={() => handleNavigate('practice')}
                            className="group relative bg-white p-8 rounded-[2rem] shadow-xl shadow-gray-100 border border-gray-100 hover:shadow-2xl hover:scale-[1.02] transition-all cursor-pointer overflow-hidden"
                        >
                            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-100 rounded-bl-[4rem] opacity-50 transition-transform group-hover:scale-110" />
                            <div className="relative z-10">
                                <div className="h-16 w-16 bg-purple-50 text-purple-600 rounded-2xl flex items-center justify-center mb-8 shadow-sm group-hover:bg-purple-600 group-hover:text-white transition-colors duration-300">
                                    <MessageSquare className="h-8 w-8" />
                                </div>
                                <h3 className="text-2xl font-bold text-gray-800 mb-6">Practice GD</h3>
                                <div className="space-y-2 text-sm text-gray-600 mb-8">
                                    <div className="flex items-center space-x-2">
                                        <Target className="w-4 h-4 text-purple-600" />
                                        <span>AI-generated discussion topics</span>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <Target className="w-4 h-4 text-purple-600" />
                                        <span>Timed practice sessions</span>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <Target className="w-4 h-4 text-purple-600" />
                                        <span>Detailed AI feedback & scoring</span>
                                    </div>
                                </div>
                                <span className="inline-flex items-center text-purple-600 font-bold group-hover:translate-x-2 transition-transform">
                                    Start Practicing <Rocket className="ml-2 h-4 w-4" />
                                </span>
                            </div>
                        </div>

                        {/* Topic Analysis Card */}
                        <div
                            onClick={() => handleNavigate('analysis')}
                            className="group relative bg-white p-8 rounded-[2rem] shadow-xl shadow-gray-100 border border-gray-100 hover:shadow-2xl hover:scale-[1.02] transition-all cursor-pointer overflow-hidden"
                        >
                            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-100 rounded-bl-[4rem] opacity-50 transition-transform group-hover:scale-110" />
                            <div className="relative z-10">
                                <div className="h-16 w-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mb-8 shadow-sm group-hover:bg-blue-600 group-hover:text-white transition-colors duration-300">
                                    <Search className="h-8 w-8" />
                                </div>
                                <h3 className="text-2xl font-bold text-gray-800 mb-6">Topic Analysis</h3>
                                <div className="space-y-2 text-sm text-gray-600 mb-8">
                                    <div className="flex items-center space-x-2">
                                        <Target className="w-4 h-4 text-blue-600" />
                                        <span>Custom topic analysis</span>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <Target className="w-4 h-4 text-blue-600" />
                                        <span>FOR & AGAINST arguments</span>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <Target className="w-4 h-4 text-blue-600" />
                                        <span>Copy-friendly reference points</span>
                                    </div>
                                </div>
                                <span className="inline-flex items-center text-blue-600 font-bold group-hover:translate-x-2 transition-transform">
                                    Analyze Topics <Rocket className="ml-2 h-4 w-4" />
                                </span>
                            </div>
                        </div>
                    </div>

                    {/* Info Footer */}
                    <div className="mt-12 max-w-5xl mx-auto bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6 border border-blue-200">
                        <div className="flex items-start space-x-3">
                            <Users className="w-5 h-5 text-purple-600 mt-1 flex-shrink-0" />
                            <div>
                                <h4 className="font-bold text-slate-800 mb-2">Why Practice Group Discussions?</h4>
                                <p className="text-sm text-slate-700 leading-relaxed">
                                    Group Discussions are a critical evaluation component in MBA admissions and placement interviews.
                                    They assess your communication skills, critical thinking, leadership qualities, and ability to work in teams.
                                    Regular practice helps you articulate ideas clearly, think on your feet, and present balanced arguments confidently.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="p-6 max-w-7xl mx-auto animate-in slide-in-from-right-10 fade-in duration-500">
                    <div className="mb-6 flex items-center">
                        <button
                            onClick={handleBack}
                            className="mr-4 p-2 rounded-xl text-gray-500 hover:bg-white hover:text-purple-600 transition-colors"
                            title="Back to Menu"
                        >
                            <ArrowLeft className="h-6 w-6" />
                        </button>
                        <div>
                            <button onClick={handleBack} className="text-sm font-semibold text-gray-500 hover:text-purple-600 mb-1 active:text-purple-700">
                                Group Discussion Module
                            </button>
                            <h2 className="text-2xl font-bold text-gray-800">{getPageTitle()}</h2>
                        </div>
                    </div>

                    <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-1">
                        {getActiveComponent()}
                    </div>
                </div>
            )}
        </div>
    );
};

export default GroupDiscussion;
