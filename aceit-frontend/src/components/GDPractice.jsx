import React, { useState, useEffect, useRef } from 'react';
import { API_BASE_URL } from '../services/api';
import { Target, RefreshCw, CheckCircle2, Lightbulb, Send } from 'lucide-react';

const GDPractice = () => {
    const [topic, setTopic] = useState('');
    const [userResponse, setUserResponse] = useState('');
    const [timeSpent, setTimeSpent] = useState(0);
    const [isLoading, setIsLoading] = useState(false);
    const [feedback, setFeedback] = useState(null);
    const [timerRunning, setTimerRunning] = useState(false);
    const timerRef = useRef(null);

    // Timer logic
    useEffect(() => {
        if (timerRunning) {
            timerRef.current = setInterval(() => {
                setTimeSpent(prev => prev + 1);
            }, 1000);
        } else {
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        }
        return () => {
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        };
    }, [timerRunning]);

    const generateTopic = async () => {
        setIsLoading(true);
        setFeedback(null);
        setUserResponse('');
        setTimeSpent(0);
        setTimerRunning(false);

        try {
            const res = await fetch(`${API_BASE_URL}/gd-practice/topic`);
            const data = await res.json();
            setTopic(data.topic);
        } catch (error) {
            console.error('Error generating topic:', error);
            alert('Failed to generate topic. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const submitResponse = async () => {
        if (!userResponse.trim()) {
            alert('Please write your response before submitting.');
            return;
        }

        setTimerRunning(false);
        setIsLoading(true);

        try {
            const res = await fetch(`${API_BASE_URL}/gd-practice/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic,
                    user_input: userResponse,
                    time_taken: timeSpent
                })
            });

            const data = await res.json();
            setFeedback(data);
        } catch (error) {
            console.error('Error submitting response:', error);
            alert('Failed to submit response. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleTextAreaFocus = () => {
        if (!timerRunning && !feedback) {
            setTimerRunning(true);
        }
    };

    const wordCount = userResponse.trim().split(/\s+/).filter(word => word.length > 0).length;

    return (
        <div className="p-6">
            {/* Top Section - About and Instructions */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                {/* About Group Discussion */}
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-3xl p-6 border border-blue-200">
                    <div className="flex items-center mb-4">
                        <div className="bg-blue-500 rounded-full p-2 mr-3">
                            <CheckCircle2 className="h-6 w-6 text-white" />
                        </div>
                        <h2 className="text-xl font-bold text-gray-900">About Group Discussion</h2>
                    </div>
                    <p className="text-gray-700 mb-4 leading-relaxed">
                        Group Discussion (GD) is a crucial component of placement interviews and MBA admissions. It evaluates
                        your communication skills, critical thinking, teamwork, and ability to articulate ideas effectively in a group setting.
                    </p>
                    <div className="space-y-2">
                        <div className="flex items-center text-gray-800">
                            <CheckCircle2 className="h-5 w-5 text-green-600 mr-2 flex-shrink-0" />
                            <span><strong>Communication:</strong> Express ideas clearly and concisely</span>
                        </div>
                        <div className="flex items-center text-gray-800">
                            <CheckCircle2 className="h-5 w-5 text-green-600 mr-2 flex-shrink-0" />
                            <span><strong>Critical Thinking:</strong> Analyze topics from multiple perspectives</span>
                        </div>
                        <div className="flex items-center text-gray-800">
                            <CheckCircle2 className="h-5 w-5 text-green-600 mr-2 flex-shrink-0" />
                            <span><strong>Confidence:</strong> Present arguments with conviction</span>
                        </div>
                    </div>
                </div>

                {/* GD Tips - Always Visible */}
                <div className="bg-gradient-to-br from-amber-50 to-yellow-50 rounded-3xl p-6 border border-amber-200">
                    <div className="flex items-center mb-4">
                        <Lightbulb className="h-6 w-6 text-amber-600 mr-2" />
                        <h3 className="text-xl font-bold text-gray-900">GD Tips</h3>
                    </div>
                    <div className="space-y-3">
                        {[
                            { title: 'Be Clear:', desc: 'Express your ideas concisely and logically' },
                            { title: 'Support Arguments:', desc: 'Use facts, examples, and data' },
                            { title: 'Structure Well:', desc: 'Introduction, body, conclusion' },
                            { title: 'Be Respectful:', desc: 'Consider different viewpoints' },
                            { title: 'Stay Relevant:', desc: 'Keep focus on the topic' },
                            { title: 'Use Examples:', desc: 'Real-world cases strengthen points' }
                        ].map((tip, idx) => (
                            <div key={idx} className="flex items-start">
                                <div className="bg-amber-500 rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mr-3 mt-0.5">
                                    <span className="text-white text-xs font-bold">{idx + 1}</span>
                                </div>
                                <div>
                                    <p className="text-sm font-semibold text-gray-900">{tip.title}</p>
                                    <p className="text-xs text-gray-700">{tip.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="space-y-6">
                {/* Main Content Area */}
                <div className="space-y-6">
                    {/* Topic Generation */}
                    {!topic && !feedback && (
                        <div className="text-center py-12">
                            <button
                                onClick={generateTopic}
                                disabled={isLoading}
                                className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-2xl hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 transition-all font-bold text-lg shadow-lg"
                            >
                                {isLoading ? (
                                    <span className="flex items-center">
                                        <RefreshCw className="h-5 w-5 mr-2 animate-spin" />
                                        Generating...
                                    </span>
                                ) : (
                                    <span className="flex items-center">
                                        <RefreshCw className="h-5 w-5 mr-2" />
                                        Generate Topic
                                    </span>
                                )}
                            </button>
                        </div>
                    )}

                    {/* Topic Display & Response */}
                    {topic && !feedback && (
                        <>
                            <div className="bg-gradient-to-r from-purple-100 to-blue-100 rounded-2xl p-6 border-l-4 border-purple-600">
                                <h3 className="text-sm font-semibold text-purple-800 mb-2">Topic</h3>
                                <p className="text-lg font-bold text-gray-900">{topic}</p>
                            </div>

                            <div className="bg-white rounded-3xl shadow-sm border border-gray-200 p-6">
                                <h3 className="text-xl font-bold text-gray-900 mb-4">Your Response</h3>
                                <textarea
                                    value={userResponse}
                                    onChange={(e) => setUserResponse(e.target.value)}
                                    onFocus={handleTextAreaFocus}
                                    placeholder="Start typing your thoughts on the topic... Focus on clarity, logical arguments, and persuasive communication."
                                    className="w-full h-64 p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none resize-none text-gray-800"
                                />
                                <div className="flex items-center justify-between mt-4">
                                    <span className="text-sm text-gray-600 font-medium">{wordCount} words</span>
                                    <button
                                        onClick={submitResponse}
                                        disabled={isLoading || !userResponse.trim()}
                                        className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 transition-all font-bold flex items-center shadow-md"
                                    >
                                        {isLoading ? (
                                            <>
                                                <RefreshCw className="h-5 w-5 mr-2 animate-spin" />
                                                Analyzing...
                                            </>
                                        ) : (
                                            <>
                                                <CheckCircle2 className="h-5 w-5 mr-2" />
                                                Submit Response
                                            </>
                                        )}
                                    </button>
                                </div>
                            </div>
                        </>
                    )}

                    {/* AI Feedback */}
                    {feedback && (
                        <div className="space-y-6">
                            {/* Topic */}
                            <div className="bg-gradient-to-r from-purple-100 to-blue-100 rounded-2xl p-6 border-l-4 border-purple-600">
                                <h3 className="text-sm font-semibold text-purple-800 mb-2">Topic</h3>
                                <p className="text-lg font-bold text-gray-900">{topic}</p>
                            </div>

                            {/* Scores */}
                            <div className="bg-white rounded-3xl shadow-sm border border-gray-200 p-6">
                                <h3 className="text-xl font-bold text-gray-900 mb-6">AI Feedback</h3>

                                <div className="grid grid-cols-3 gap-4 mb-6">
                                    {[
                                        { label: 'Clarity', score: feedback.clarity_score, color: 'blue' },
                                        { label: 'Coherence', score: feedback.coherence_score, color: 'purple' },
                                        { label: 'Relevance', score: feedback.relevance_score, color: 'green' }
                                    ].map(({ label, score, color }) => (
                                        <div key={label} className={`bg-${color}-50 rounded-2xl p-5 border border-${color}-200 text-center`}>
                                            <p className="text-sm font-semibold text-gray-600 mb-2">{label}</p>
                                            <p className={`text-4xl font-bold text-${color}-600 mb-2`}>{score}/10</p>
                                            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full bg-${color}-500`}
                                                    style={{ width: `${score * 10}%` }}
                                                />
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div className="bg-gray-50 rounded-2xl p-5 mb-4">
                                    <p className="text-gray-700 leading-relaxed">{feedback.feedback}</p>
                                </div>

                                {/* Strengths and Improvements - Two Column Layout */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                                    {/* Strengths */}
                                    {feedback.strengths && feedback.strengths.length > 0 && (
                                        <div className="bg-green-50 rounded-2xl p-5 border border-green-200">
                                            <h4 className="font-bold text-green-800 mb-3 flex items-center">
                                                <CheckCircle2 className="h-5 w-5 mr-2" />
                                                Strengths
                                            </h4>
                                            <ul className="space-y-2">
                                                {feedback.strengths.map((strength, idx) => (
                                                    <li key={idx} className="flex items-start text-gray-700">
                                                        <span className="text-green-600 mr-2">✓</span>
                                                        {strength}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}

                                    {/* Weaknesses */}
                                    {feedback.improvements && feedback.improvements.length > 0 && (
                                        <div className="bg-red-50 rounded-2xl p-5 border border-red-200">
                                            <h4 className="font-bold text-red-800 mb-3 flex items-center">
                                                <Target className="h-5 w-5 mr-2" />
                                                Weaknesses
                                            </h4>
                                            <ul className="space-y-2">
                                                {feedback.improvements.map((improvement, idx) => (
                                                    <li key={idx} className="flex items-start text-gray-700">
                                                        <span className="text-red-600 mr-2">✗</span>
                                                        {improvement}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>


                                {/* Topic Study Points - Only shown after feedback */}
                                {feedback.topic_points && feedback.topic_points.length > 0 && (
                                    <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-6 mb-6 border-2 border-indigo-300">
                                        <div className="flex items-center mb-4">
                                            <Lightbulb className="h-6 w-6 text-indigo-600 mr-2" />
                                            <h4 className="text-xl font-bold text-indigo-900">Relevant Points to Study for This Topic</h4>
                                        </div>
                                        <p className="text-sm text-gray-600 mb-4">Key concepts and points you should know about this topic:</p>
                                        <div className="grid grid-cols-1 gap-3">
                                            {feedback.topic_points.map((point, idx) => (
                                                <div key={idx} className="bg-white rounded-xl p-4 shadow-sm border border-indigo-200 hover:shadow-md transition-shadow">
                                                    <div className="flex items-start">
                                                        <div className="bg-indigo-600 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mr-3">
                                                            <span className="text-white text-sm font-bold">{idx + 1}</span>
                                                        </div>
                                                        <p className="text-gray-800 leading-relaxed pt-1">{point}</p>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                <button
                                    onClick={generateTopic}
                                    className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-2xl hover:from-blue-700 hover:to-indigo-700 transition-all font-bold"
                                >
                                    Practice with New Topic
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default GDPractice;
