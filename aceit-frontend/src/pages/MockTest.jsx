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
    const [questionStartTime, setQuestionStartTime] = useState(Date.now());

    // Results state
    const [results, setResults] = useState(null);

    const navigate = useNavigate();

    // Timer effect
    useEffect(() => {
        if (view === 'test' && timeLeft > 0) {
            const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
            return () => clearTimeout(timer);
        } else if (view === 'test' && timeLeft === 0 && questions.length > 0) {
            // Auto-submit when time runs out
            handleCompleteTest();
        }
    }, [timeLeft, view]);

    // Categories state
    const [categories, setCategories] = useState({});

    // Fetch categories on mount
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const response = await aptitudeAPI.getCategories();
                setCategories(response.data.categories || {});
            } catch (err) {
                console.error('Failed to fetch categories:', err);
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
            setDuration(response.data.duration_minutes * 60);
            setTimeLeft(response.data.duration_minutes * 60);
            setView('test');
            setQuestionStartTime(Date.now());
        } catch (err) {
            console.error('Failed to start test:', err);
            setError('Failed to start test. Please try again.');
        }
    };

    const handleAnswer = async (questionId, optionIndex) => {
        const timeSpent = Math.floor((Date.now() - questionStartTime) / 1000);

        // Submit answer to backend
        try {
            await mockTestAPI.submitAnswer(testId, attemptId, questionId, optionIndex, timeSpent);
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
                                    <p className="text-sm text-gray-600">100 questions</p>
                                    <p className="text-sm text-gray-600">90 minutes</p>
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
                                    onClick={() => setTestType('topic_wise')}
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
                                    >
                                        <option value="">-- Choose Category --</option>
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
                                            disabled={!selectedCategory}
                                        >
                                            <option value="">-- Choose Topic --</option>
                                            {selectedCategory && categories[selectedCategory]?.map(topic => (
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
                            {loading ? 'Generating Test...' : 'Start Mock Test 🚀'}
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
                    {/* Header */}
                    <div className="flex justify-between items-center mb-4">
                        <div>
                            <span className="inline-block px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-bold uppercase tracking-wide mb-1">
                                Mock Test - {question.category}
                            </span>
                            <h2 className="text-xl font-bold text-gray-800">
                                Question {currentQuestion + 1} <span className="text-gray-400 text-base font-normal">/ {questions.length}</span>
                            </h2>
                        </div>
                        <div className={`text-lg font-mono font-bold px-4 py-2 rounded-lg ${timeLeft < 300 ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-gray-100 text-gray-700'
                            }`}>
                            ⏱️ {formatTime(timeLeft)}
                        </div>
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
                    </div>

                    {/* Options */}
                    <div className="grid gap-3 mb-8">
                        {question.options.map((opt, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleAnswer(question.id, idx)}
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
                        <button
                            onClick={handlePrevious}
                            disabled={currentQuestion === 0}
                            className="px-6 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50"
                        >
                            ← Previous
                        </button>

                        {currentQuestion === questions.length - 1 ? (
                            <button
                                onClick={handleCompleteTest}
                                className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-bold shadow-md"
                            >
                                Submit Test ✓
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
            </div>
        );
    }

    // Results Screen
    if (view === 'results' && results) {
        return (
            <div className="p-6 max-w-4xl mx-auto">
                <div className="bg-white rounded-lg shadow-xl p-8">
                    <div className="text-center mb-8">
                        <div className="inline-flex items-center justify-center w-32 h-32 rounded-full border-8 border-blue-50 bg-white shadow-inner mb-4">
                            <span className="text-4xl font-black text-gray-800">{results.accuracy.toFixed(0)}%</span>
                        </div>
                        <h2 className="text-3xl font-bold text-gray-800">Mock Test Completed!</h2>
                        <p className="text-gray-500 mt-2">
                            You scored {results.score} out of {results.total} questions
                        </p>
                        <p className="text-sm text-gray-400 mt-1">
                            Time taken: {formatTime(results.time_taken)}
                        </p>
                    </div>

                    {/* Category Performance */}
                    {results.category_performance && (
                        <div className="mb-8">
                            <h3 className="text-xl font-bold mb-4">Category-wise Performance</h3>
                            <div className="grid md:grid-cols-2 gap-4">
                                {Object.entries(results.category_performance).map(([category, stats]) => (
                                    <div key={category} className="bg-gray-50 p-4 rounded-lg">
                                        <h4 className="font-semibold text-gray-700 mb-2">{category}</h4>
                                        <div className="flex justify-between text-sm">
                                            <span>Accuracy:</span>
                                            <span className="font-bold">{stats.accuracy.toFixed(1)}%</span>
                                        </div>
                                        <div className="flex justify-between text-sm text-gray-600">
                                            <span>Correct:</span>
                                            <span>{stats.correct}/{stats.total}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    <div className="flex gap-4 justify-center">
                        <button
                            onClick={() => {
                                setView('selection');
                                setTestId(null);
                                setAttemptId(null);
                                setQuestions([]);
                                setAnswers({});
                                setResults(null);
                            }}
                            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold shadow-lg"
                        >
                            Take Another Test
                        </button>
                        <button
                            onClick={() => navigate('/')}
                            className="px-6 py-3 bg-white border-2 border-gray-200 text-gray-700 rounded-lg hover:border-gray-300 font-semibold"
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
