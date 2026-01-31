import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { mockTestAPI, aptitudeAPI } from '../services/api';

const MockTest = () => {
    const [view, setView] = useState('selection'); // 'selection', 'test', 'results'
    const [testType, setTestType] = useState('full_length');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedTopic, setSelectedTopic] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // Test state
    const [testId, setTestId] = useState(null);
    const [attemptId, setAttemptId] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [answers, setAnswers] = useState({});
    const [timeLeft, setTimeLeft] = useState(0);
    const [duration, setDuration] = useState(0);
    const [testStartTime, setTestStartTime] = useState(null);
    const [questionStartTime, setQuestionStartTime] = useState(Date.now());

    // Results state
    const [results, setResults] = useState(null);

    const navigate = useNavigate();

    // Timer effect - STRICT Logic
    useEffect(() => {
        if (view === 'test' && testStartTime) {
            const interval = setInterval(() => {
                const elapsedSeconds = Math.floor((Date.now() - testStartTime) / 1000);
                const remaining = Math.max(0, duration - elapsedSeconds);
                setTimeLeft(remaining);

                if (remaining <= 0) {
                    clearInterval(interval);
                    console.log("Time's Up! Auto-submitting test.");
                    handleCompleteTest();
                }
            }, 1000);
            return () => clearInterval(interval);
        }
    }, [view, testStartTime, duration]);

    // Categories state
    const [categories, setCategories] = useState({});
    const [catsLoading, setCatsLoading] = useState(false);

    // Fetch categories on mount
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                setCatsLoading(true);
                const response = await aptitudeAPI.getCategories();
                setCategories(response.data.categories || {});
            } catch (err) {
                console.error('Failed to fetch categories:', err);
                setError('Failed to load categories. Please refresh the page.');
            } finally {
                setCatsLoading(false);
            }
        };
        fetchCategories();
    }, []);

    const generateTest = async () => {
        try {
            setLoading(true);
            setError('');

            const response = await mockTestAPI.generateTest(
                testType,
                (testType === 'section_wise' || testType === 'topic_wise') ? selectedCategory : null,
                testType === 'topic_wise' ? selectedTopic : null
            );

            setTestId(response.data.test_id);
            await startTest(response.data.test_id);
        } catch (err) {
            console.error('Failed to generate test:', err);
            setError('Failed to generate test. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const startTest = async (id) => {
        try {
            const response = await mockTestAPI.startTest(id);
            setAttemptId(response.data.attempt_id);
            setQuestions(response.data.questions);
            setAnswers({}); // Reset answers for new test
            setCurrentQuestion(0); // Reset to first question index

            const totalSeconds = response.data.duration_minutes * 60;
            setDuration(totalSeconds);
            setTimeLeft(totalSeconds);
            setTestStartTime(Date.now()); // Mark start time for strict tracking

            setView('test');
            setQuestionStartTime(Date.now());
        } catch (err) {
            console.error('Failed to start test:', err);
            setError('Failed to start test. Please try again.');
        }
    };

    const handleAnswer = async (questionId, optionIndex, optionText) => {
        const timeSpent = Math.floor((Date.now() - questionStartTime) / 1000);

        // Submit answer to backend
        try {
            await mockTestAPI.submitAnswer(testId, attemptId, questionId, optionIndex, timeSpent, optionText);
            setAnswers(prev => ({ ...prev, [questionId]: optionIndex }));
        } catch (err) {
            console.error('Failed to submit answer:', err);
        }
    };

    const handleNext = () => {
        if (currentQuestion < questions.length - 1) {
            setCurrentQuestion(currentQuestion + 1);
            setQuestionStartTime(Date.now());
        }
    };

    const handlePrevious = () => {
        if (currentQuestion > 0) {
            setCurrentQuestion(currentQuestion - 1);
            setQuestionStartTime(Date.now());
        }
    };

    const handleCompleteTest = async () => {
        try {
            setLoading(true);
            const response = await mockTestAPI.completeTest(testId, attemptId);
            setResults(response.data);
            setView('results');
        } catch (err) {
            console.error('Failed to complete test:', err);
            setError('Failed to complete test. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    };

    // Selection Screen
    if (view === 'selection') {
        return (
            <div className="p-6 max-w-4xl mx-auto">
                <div className="bg-white rounded-lg shadow-lg p-8">
                    <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Mock Aptitude Test</h1>

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
                            {error}
                        </div>
                    )}

                    <div className="space-y-6">
                        {/* Test Type Selection */}
                        <div>
                            <label className="block text-gray-700 font-semibold mb-3">Select Test Type</label>
                            <div className="grid md:grid-cols-3 gap-4">
                                <div
                                    onClick={() => {
                                        setTestType('full_length');
                                        setSelectedCategory('');
                                        setSelectedTopic('');
                                    }}
                                    className={`p-6 border-2 rounded-lg cursor-pointer transition-all ${testType === 'full_length'
                                        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                                        : 'border-gray-200 hover:border-blue-300'
                                        }`}
                                >
                                    <h3 className="font-bold text-lg mb-2">Full-Length Test</h3>
                                    <p className="text-sm text-gray-600">30 questions</p>
                                    <p className="text-sm text-gray-600">30 minutes</p>
                                    <p className="text-xs text-gray-500 mt-2">All categories</p>
                                </div>

                                <div
                                    onClick={() => {
                                        setTestType('section_wise');
                                        setSelectedTopic('');
                                    }}
                                    className={`p-6 border-2 rounded-lg cursor-pointer transition-all ${testType === 'section_wise'
                                        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                                        : 'border-gray-200 hover:border-blue-300'
                                        }`}
                                >
                                    <h3 className="font-bold text-lg mb-2">Section Test</h3>
                                    <p className="text-sm text-gray-600">30 questions</p>
                                    <p className="text-sm text-gray-600">30 minutes</p>
                                    <p className="text-xs text-gray-500 mt-2">Single category</p>
                                </div>

                                <div
                                    onClick={() => {
                                        setTestType('topic_wise');
                                        // Don't reset category if already selected, but reset topic
                                        setSelectedTopic('');
                                    }}
                                    className={`p-6 border-2 rounded-lg cursor-pointer transition-all ${testType === 'topic_wise'
                                        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                                        : 'border-gray-200 hover:border-blue-300'
                                        }`}
                                >
                                    <h3 className="font-bold text-lg mb-2">Topic Test</h3>
                                    <p className="text-sm text-gray-600">20 questions</p>
                                    <p className="text-sm text-gray-600">20 minutes</p>
                                    <p className="text-xs text-gray-500 mt-2">Single topic</p>
                                </div>
                            </div>
                        </div>

                        {/* Category/Topic Selection for section/topic tests */}
                        {testType !== 'full_length' && (
                            <div className="grid md:grid-cols-2 gap-4 bg-gray-50 p-6 rounded-lg">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Select Category</label>
                                    <select
                                        value={selectedCategory}
                                        onChange={(e) => {
                                            setSelectedCategory(e.target.value);
                                            setSelectedTopic('');
                                        }}
                                        className="w-full p-3 border rounded-lg bg-white"
                                        disabled={catsLoading}
                                    >
                                        <option value="">{catsLoading ? 'Loading Categories...' : '-- Choose Category --'}</option>
                                        {Object.keys(categories).map(cat => (
                                            <option key={cat} value={cat}>{cat}</option>
                                        ))}
                                    </select>
                                </div>

                                {testType === 'topic_wise' && (
                                    <div>
                                        <label className="block text-sm font-semibold text-gray-700 mb-2">Select Topic</label>
                                        <select
                                            value={selectedTopic}
                                            onChange={(e) => setSelectedTopic(e.target.value)}
                                            className="w-full p-3 border rounded-lg bg-white"
                                            disabled={!selectedCategory || catsLoading}
                                        >
                                            <option value="">-- Choose Topic --</option>
                                            {selectedCategory && (categories[selectedCategory] || []).map(topic => (
                                                <option key={topic} value={topic}>
                                                    {topic.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                )}
                            </div>
                        )}

                        <button
                            onClick={generateTest}
                            disabled={loading || (testType === 'section_wise' && !selectedCategory) || (testType === 'topic_wise' && (!selectedCategory || !selectedTopic))}
                            className="w-full bg-blue-600 text-white py-4 rounded-lg font-bold text-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors shadow-lg"
                        >
                            {loading ? 'Generating Test...' : 'Start Mock Test'}
                        </button>
                    </div>
                </div>
            </div>
        );
    }


    // Test Screen
    if (view === 'test' && questions.length > 0) {
        const question = questions[currentQuestion];
        const progressPercent = ((currentQuestion + 1) / questions.length) * 100;
        const timePercent = (timeLeft / duration) * 100;

        return (
            <div className="p-6 max-w-4xl mx-auto">
                <div className="bg-white rounded-lg shadow-md p-6">
                    {/* Header with Stats */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 p-4 bg-gray-50 rounded-xl border border-gray-100">
                        {/* Time Left */}
                        <div className="flex flex-col items-center justify-center p-2 bg-white rounded-lg shadow-sm border border-gray-100">
                            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Time Left</span>
                            <span className={`text-xl font-mono font-bold ${timeLeft < 300 ? 'text-red-600 animate-pulse' : 'text-blue-600'}`}>
                                {formatTime(timeLeft)}
                            </span>
                        </div>

                        {/* Questions Attempted */}
                        <div className="flex flex-col items-center justify-center p-2 bg-white rounded-lg shadow-sm border border-gray-100">
                            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Attempted</span>
                            <span className="text-xl font-bold text-green-600">
                                {Object.keys(answers).length}
                            </span>
                        </div>

                        {/* Questions Left */}
                        <div className="flex flex-col items-center justify-center p-2 bg-white rounded-lg shadow-sm border border-gray-100">
                            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Remaining</span>
                            <span className="text-xl font-bold text-orange-500">
                                {questions.length - Object.keys(answers).length}
                            </span>
                        </div>

                        {/* Current Question */}
                        <div className="flex flex-col items-center justify-center p-2 bg-white rounded-lg shadow-sm border border-gray-100">
                            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Question</span>
                            <span className="text-xl font-bold text-gray-800">
                                {currentQuestion + 1} <span className="text-sm text-gray-400 font-normal">/ {questions.length}</span>
                            </span>
                        </div>
                    </div>

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6 text-center font-medium">
                            {error}
                        </div>
                    )}

                    {/* Test Title / Context Header */}
                    <div className="mb-6 pb-2 border-b border-gray-100">
                        {testType === 'full_length' && (
                            <div>
                                <h2 className="text-2xl font-bold text-gray-800">Full-Length Mock Test</h2>
                                <div className="flex gap-2 mt-1">
                                    <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded font-medium">Mixed Categories</span>
                                    <span className="px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded font-medium">
                                        Current Section: {question.category}
                                    </span>
                                </div>
                            </div>
                        )}
                        {testType === 'section_wise' && (
                            <div>
                                <h2 className="text-2xl font-bold text-gray-800">Section Test</h2>
                                <span className="inline-block mt-1 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-bold">
                                    {question.category}
                                </span>
                            </div>
                        )}
                        {testType === 'topic_wise' && (
                            <div>
                                <h2 className="text-2xl font-bold text-gray-800">Topic Test</h2>
                                <div className="flex gap-2 items-center mt-1">
                                    <span className="text-gray-500 text-sm">{question.category}</span>
                                    <span className="text-gray-300">•</span>
                                    <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-bold capitalize">
                                        {(question.topic || '').replace(/_/g, ' ')}
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Progress Bar */}
                    <div className="mb-6">
                        <div className="flex justify-between text-xs text-gray-500 mb-1">
                            <span>Progress</span>
                            <span>{Math.round(progressPercent)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                            <div className="bg-blue-600 h-2 rounded-full transition-all duration-500" style={{ width: `${progressPercent}%` }}></div>
                        </div>
                    </div>

                    {/* Question */}
                    <div className="text-lg font-medium text-gray-800 mb-8 leading-relaxed">
                        {question.question}
                        {question.image_url && (
                            <div className="mt-6 mb-4 flex justify-center">
                                <img
                                    src={question.image_url}
                                    alt="Question Diagram"
                                    className="max-w-full h-auto max-h-96 rounded-lg border border-gray-200 shadow-sm object-contain"
                                    onError={(e) => {
                                        e.target.style.display = 'none';
                                        console.error('Failed to load question image:', question.image_url);
                                    }}
                                />
                            </div>
                        )}
                    </div>

                    {/* Options */}
                    <div className="grid gap-3 mb-8">
                        {question.options.map((opt, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleAnswer(question.id, idx, opt)}
                                className={`text-left p-4 rounded-lg border-2 transition-all ${answers[question.id] === idx
                                    ? 'border-blue-500 bg-blue-50 text-blue-800'
                                    : 'border-gray-200 hover:border-blue-200 hover:bg-gray-50'
                                    }`}
                            >
                                <span className="inline-block w-8 font-bold text-gray-400">{String.fromCharCode(65 + idx)}</span>
                                {opt}
                            </button>
                        ))}
                    </div>

                    {/* Navigation */}
                    <div className="flex justify-between pt-6 border-t">
                        {testType !== 'full_length' ? (
                            <button
                                onClick={handlePrevious}
                                disabled={currentQuestion === 0}
                                className="px-6 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50"
                            >
                                ← Previous
                            </button>
                        ) : (
                            <div />
                        )}

                        {currentQuestion === questions.length - 1 ? (
                            <button
                                onClick={handleCompleteTest}
                                disabled={loading}
                                className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-bold shadow-md disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
                            >
                                {loading ? (
                                    <>
                                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                                        Submitting...
                                    </>
                                ) : 'Submit Test'}
                            </button>
                        ) : (
                            <button
                                onClick={handleNext}
                                className="px-8 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
                            >
                                Next →
                            </button>
                        )}
                    </div>
                </div>

                {/* Submission Loading Overlay */}
                {loading && (
                    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
                        <div className="bg-white p-8 rounded-2xl shadow-2xl flex flex-col items-center max-w-sm w-full mx-4">
                            <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-600 border-t-transparent mb-6"></div>
                            <h3 className="text-xl font-bold text-gray-800 mb-2 text-center">Submitting Your Results</h3>
                            <p className="text-gray-500 text-center">Please wait while we calculate your personalized performance insights...</p>
                        </div>
                    </div>
                )}
            </div>
        );
    }

    // Results Screen
    if (view === 'results' && results) {
        return (
            <div className="p-6 max-w-4xl mx-auto">
                <div className="bg-white rounded-lg shadow-xl p-8">
                    <div className="text-center mb-10">
                        <h2 className="text-3xl font-bold text-gray-800 mb-2">Mock Test Completed!</h2>
                        <p className="text-gray-500">Here's how you performed</p>
                    </div>

                    {/* Stat Cards Grid */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
                        {/* Overall Score */}
                        <div className="bg-blue-50 p-6 rounded-xl border border-blue-100 flex flex-col items-center">
                            <span className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">Score</span>
                            <span className="text-3xl font-black text-blue-600">{results.score} <span className="text-lg text-gray-400 font-medium">/ {results.total}</span></span>
                        </div>

                        {/* Accuracy */}
                        <div className="bg-green-50 p-6 rounded-xl border border-green-100 flex flex-col items-center">
                            <span className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">Accuracy</span>
                            <span className="text-3xl font-black text-green-600">{results.accuracy.toFixed(0)}%</span>
                        </div>

                        {/* Average Time */}
                        <div className="bg-orange-50 p-6 rounded-xl border border-orange-100 flex flex-col items-center">
                            <span className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">Avg Time</span>
                            <span className="text-3xl font-black text-orange-600">
                                {(() => {
                                    const val = results.average_time_per_question || (results.time_taken / results.total) || 0;
                                    const minutes = Math.floor(val / 60);
                                    const seconds = Math.round(val % 60);
                                    if (minutes > 0) return `${minutes}m ${seconds}s`;
                                    return `${seconds}s`;
                                })()}
                            </span>
                            <span className="text-xs text-center text-gray-400 mt-1">per question</span>
                        </div>

                        {/* Performance Rating */}
                        {(() => {
                            let rating = 'Poor';
                            let colorClass = 'bg-red-50 border-red-100 text-red-600';

                            if (results.accuracy >= 90) {
                                rating = 'Excellent';
                                colorClass = 'bg-purple-50 border-purple-100 text-purple-600';
                            } else if (results.accuracy >= 75) {
                                rating = 'Good';
                                colorClass = 'bg-green-50 border-green-100 text-green-600';
                            } else if (results.accuracy >= 50) {
                                rating = 'Average';
                                colorClass = 'bg-yellow-50 border-yellow-100 text-yellow-600';
                            }

                            return (
                                <div className={`${colorClass} p-6 rounded-xl border flex flex-col items-center`}>
                                    <span className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">Performance</span>
                                    <span className="text-3xl font-black">{rating}</span>
                                </div>
                            );
                        })()}
                    </div>

                    {/* Topic or Category Breakdown */}
                    {results.topic_performance && Object.keys(results.topic_performance).length > 0 && (
                        <div className="mb-8">
                            <h3 className="text-xl font-bold mb-4 text-gray-800">Topic-wise Performance</h3>
                            <div className="grid md:grid-cols-2 gap-4">
                                {Object.entries(results.topic_performance).map(([topic, stats]) => (
                                    <div key={topic} className="bg-gray-50 p-4 rounded-lg flex justify-between items-center">
                                        <div>
                                            <h4 className="font-semibold text-gray-700 capitalize">{topic.replace(/_/g, ' ')}</h4>
                                            <div className="text-xs text-gray-500 mt-1">
                                                {stats.correct} / {stats.total} Correct
                                            </div>
                                        </div>
                                        <div className="bg-white px-3 py-1 rounded shadow-sm border text-sm font-bold text-gray-700">
                                            {stats.accuracy.toFixed(0)}%
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Fallback to Category if Topic not available (e.g. old tests) */}
                    {(!results.topic_performance || Object.keys(results.topic_performance).length === 0) && results.category_performance && (
                        <div className="mb-8">
                            <h3 className="text-xl font-bold mb-4 text-gray-800">Category-wise Performance</h3>
                            <div className="grid md:grid-cols-2 gap-4">
                                {Object.entries(results.category_performance).map(([category, stats]) => (
                                    <div key={category} className="bg-gray-50 p-4 rounded-lg flex justify-between items-center">
                                        <div>
                                            <h4 className="font-semibold text-gray-700">{category}</h4>
                                            <div className="text-xs text-gray-500 mt-1">
                                                {stats.correct} / {stats.total} Correct
                                            </div>
                                        </div>
                                        <div className="bg-white px-3 py-1 rounded shadow-sm border text-sm font-bold text-gray-700">
                                            {stats.accuracy.toFixed(0)}%
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    <div className="flex gap-4 justify-center mt-10">
                        <button
                            onClick={() => {
                                setView('selection');
                                setTestId(null);
                                setAttemptId(null);
                                setQuestions([]);
                                setAnswers({});
                                setCurrentQuestion(0);
                                setResults(null);
                                setError('');
                                // Reset selection states
                                setTestType('full_length');
                                setSelectedCategory('');
                                setSelectedTopic('');
                            }}
                            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-bold shadow-lg transition-transform hover:-translate-y-0.5"
                        >
                            Take Another Test
                        </button>
                        <button
                            onClick={() => navigate('/')}
                            className="px-8 py-3 bg-white border-2 border-gray-200 text-gray-700 rounded-lg hover:border-gray-300 font-bold hover:bg-gray-50 transition-colors"
                        >
                            Back to Dashboard
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="p-6 max-w-4xl mx-auto text-center">
            <div className="bg-white p-8 rounded-lg shadow-md animate-pulse">Loading...</div>
        </div>
    );
};

export default MockTest;
