import React, { useState, useEffect } from 'react';
import { aptitudeAPI } from '../services/api';

/**
 * IndiaBIX-style Practice Mode Component
 * - One question at a time
 * - Instant feedback after answer selection
 * - No question repetition per user/topic
 * - No timer, pure learning mode
 */
const PracticeMode = () => {
    // Selection state
    const [categories, setCategories] = useState({});
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedTopic, setSelectedTopic] = useState('all');

    // Question state
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [questionStartTime, setQuestionStartTime] = useState(null);

    // Feedback state
    const [showFeedback, setShowFeedback] = useState(false);
    const [feedback, setFeedback] = useState(null);

    // Stats tracking
    const [sessionCount, setSessionCount] = useState(0);
    const [sessionCorrect, setSessionCorrect] = useState(0);

    // UI state
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [practiceStarted, setPracticeStarted] = useState(false);

    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        try {
            const response = await aptitudeAPI.getCategories();
            setCategories(response.data.categories || {});
        } catch (err) {
            console.error('Failed to fetch categories:', err);
            setError('Failed to load categories');
        }
    };

    const startPractice = async () => {
        if (!selectedCategory) {
            setError('Please select a category');
            return;
        }

        setPracticeStarted(true);
        setFeedback(null);
        setCurrentQuestion(null);
        setSessionCount(0);
        setSessionCorrect(0);

        await fetchNextQuestion(true);
    };

    const fetchNextQuestion = async (reset = false) => {
        try {
            setLoading(true);
            setError('');
            setShowFeedback(false);
            setSelectedAnswer(null);
            setFeedback(null);

            const topic = selectedTopic === 'all' ? null : selectedTopic;
            const response = await aptitudeAPI.getNextQuestion(selectedCategory, topic, reset);

            if (!response.data.has_more_questions) {
                setError(response.data.message || 'No more questions available');
                setCurrentQuestion(null);
                return;
            }

            setCurrentQuestion(response.data);
            setQuestionStartTime(Date.now());
        } catch (err) {
            console.error('Failed to fetch question:', err);
            setError('Failed to load question. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleAnswerSelect = (optionIndex) => {
        if (showFeedback) return;
        setSelectedAnswer(optionIndex);
    };

    const submitAnswer = async () => {
        if (selectedAnswer === null) {
            setError('Please select an answer');
            return;
        }

        try {
            setLoading(true);
            setError('');

            const timeSpent = Math.floor((Date.now() - questionStartTime) / 1000);
            const response = await aptitudeAPI.submitPracticeAnswer(
                currentQuestion.question_id,
                selectedAnswer,
                timeSpent,
                currentQuestion.options
            );

            setFeedback(response.data);
            setShowFeedback(true);

            // Update session stats
            setSessionCount(prev => prev + 1);
            if (response.data.is_correct) {
                setSessionCorrect(prev => prev + 1);
            }
        } catch (err) {
            console.error('Failed to submit answer:', err);
            setError('Failed to submit answer. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleNextQuestion = () => {
        fetchNextQuestion();
    };

    const resetPractice = () => {
        setPracticeStarted(false);
        setCurrentQuestion(null);
        setSelectedAnswer(null);
        setShowFeedback(false);
        setFeedback(null);
        setSelectedCategory('');
        setSelectedTopic('all');
    };

    // 1. Selection Screen
    if (!practiceStarted) {
        return (
            <div className="max-w-4xl mx-auto">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">Start Practice Session</h2>

                {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}

                <div className="grid md:grid-cols-2 gap-8">
                    <div>
                        <label className="block text-gray-700 font-semibold mb-3">Select Category</label>
                        <div className="space-y-3">
                            {Object.keys(categories).length === 0 ? (
                                <p className="text-gray-500 italic">Loading categories...</p>
                            ) : (
                                Object.keys(categories).map(cat => (
                                    <div
                                        key={cat}
                                        onClick={() => { setSelectedCategory(cat); setSelectedTopic('all'); }}
                                        className={`p-4 border rounded-lg cursor-pointer transition-all ${selectedCategory === cat
                                            ? 'bg-blue-50 border-blue-500 ring-2 ring-blue-200'
                                            : 'hover:bg-gray-50 border-gray-200'
                                            }`}
                                    >
                                        <h3 className="font-bold text-lg">{cat}</h3>
                                        <p className="text-sm text-gray-500">{categories[cat].length} Topics Available</p>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    <div className={selectedCategory ? 'opacity-100' : 'opacity-50 pointer-events-none'}>
                        <label className="block text-gray-700 font-semibold mb-3">Select Topic (Optional)</label>
                        <select
                            value={selectedTopic}
                            onChange={(e) => setSelectedTopic(e.target.value)}
                            className="w-full p-3 border rounded-lg bg-white focus:ring-2 focus:ring-blue-500 mb-6"
                            disabled={!selectedCategory}
                        >
                            <option value="all">All Topics in {selectedCategory}</option>
                            {selectedCategory && categories[selectedCategory]?.map(topic => (
                                <option key={topic} value={topic}>
                                    {topic.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                </option>
                            ))}
                        </select>

                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                            <h4 className="font-semibold text-blue-800 mb-2">Practice Mode Features:</h4>
                            <ul className="text-gray-600 text-sm space-y-1 mb-6">
                                <li>One question at a time</li>
                                <li>Instant feedback with explanations</li>
                                <li>No question repetition</li>
                                <li>Adaptive difficulty progression</li>
                                <li>No timer - learn at your pace</li>
                            </ul>

                            <button
                                onClick={startPractice}
                                disabled={!selectedCategory}
                                className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl flex items-center justify-center"
                            >
                                Start Practice
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    // 2. Loading State
    if (loading && !currentQuestion) {
        return (
            <div className="text-center py-12">
                <div className="animate-pulse text-gray-600">Loading question...</div>
            </div>
        );
    }

    // 3. No More Questions / Completed Topic
    if (!currentQuestion && !loading) {
        return (
            <div className="max-w-2xl mx-auto text-center">
                <div className="bg-green-50 border border-green-200 rounded-lg p-8">
                    <h2 className="text-2xl font-bold text-green-800 mb-2">Congratulations!</h2>
                    <p className="text-green-700 mb-6">{error || 'You\'ve completed all available questions!'}</p>
                    <button
                        onClick={resetPractice}
                        className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700"
                    >
                        Practice Another Topic
                    </button>
                </div>
            </div>
        );
    }

    // 4. Feedback View
    if (showFeedback && feedback) {
        const isCorrect = feedback.is_correct;
        const sessionAccuracy = sessionCount > 0 ? Math.round((sessionCorrect / sessionCount) * 100) : 0;

        return (
            <div className="max-w-3xl mx-auto">
                {/* Stats Summary Header */}
                <div className="flex justify-between items-center mb-6 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-3xl border border-blue-100 shadow-sm transition-all duration-500">
                    <div className="flex gap-8">
                        <div>
                            <span className="text-xs text-blue-500 block font-black uppercase tracking-widest mb-1">Session</span>
                            <div className="flex items-baseline">
                                <span className="text-2xl font-black text-blue-900">{sessionCount}</span>
                                <span className="text-xs text-blue-400 font-bold ml-2">Questions</span>
                            </div>
                        </div>
                        <div>
                            <span className="text-xs text-green-500 block font-black uppercase tracking-widest mb-1">Correct</span>
                            <div className="flex items-baseline">
                                <span className="text-2xl font-black text-green-600">{sessionCorrect}</span>
                                <span className="text-xs text-green-400 font-bold ml-2">Answers</span>
                            </div>
                        </div>
                        <div>
                            <span className="text-xs text-indigo-500 block font-black uppercase tracking-widest mb-1">Accuracy</span>
                            <div className="flex items-baseline">
                                <span className="text-2xl font-black text-indigo-700">{sessionAccuracy}%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className={`rounded-3xl p-6 mb-6 ${isCorrect ? 'bg-green-50 border-2 border-green-500' : 'bg-red-50 border-2 border-red-500'}`}>
                    <div className="flex items-center justify-center mb-4">
                        <div className={`px-3 py-1 rounded text-xs font-bold ${isCorrect ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                            {isCorrect ? 'PASS' : 'FAIL'}
                        </div>
                    </div>
                    <h2 className={`text-2xl font-bold text-center mb-2 ${isCorrect ? 'text-green-800' : 'text-red-800'}`}>
                        {isCorrect ? 'Correct!' : 'Incorrect'}
                    </h2>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                    <h3 className="font-semibold text-gray-700 mb-4">Question:</h3>
                    {currentQuestion.image_url && (
                        <div className="mb-4 text-center">
                            <img src={currentQuestion.image_url} alt="Problem Visualization" className="max-h-64 mx-auto border rounded shadow-sm" />
                        </div>
                    )}
                    <p className="text-gray-800 mb-6">{currentQuestion.question}</p>

                    <div className="space-y-2 mb-6">
                        {feedback.options?.map((option, idx) => (
                            <div key={idx} className={`p-3 rounded border ${idx === feedback.correct_answer ? 'bg-green-50 border-green-300' : idx === feedback.user_answer ? 'bg-red-50 border-red-300' : 'bg-gray-50'}`}>
                                <span className="font-bold mr-2">{String.fromCharCode(65 + idx)}.</span>
                                {option}
                                {idx === feedback.correct_answer && <span className="ml-2 text-green-600 font-semibold">(Correct)</span>}
                                {idx === feedback.user_answer && idx !== feedback.correct_answer && <span className="ml-2 text-red-600 font-semibold">(Your Answer)</span>}
                            </div>
                        ))}
                    </div>

                    <div className="bg-blue-50 p-4 rounded-lg">
                        <h4 className="font-semibold text-blue-800 mb-2">Explanation:</h4>
                        <p className="text-blue-900">{feedback.explanation}</p>
                    </div>
                </div>

                <div className="flex justify-center gap-4">
                    <button onClick={handleNextQuestion} className="px-8 py-3 bg-blue-600 text-white rounded-lg font-bold hover:bg-blue-700 transition-colors">
                        Next Question
                    </button>
                    <button onClick={resetPractice} className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
                        Change Topic
                    </button>
                </div>
            </div>
        );
    }

    // 5. Question View
    const sessionAccuracy = sessionCount > 0 ? Math.round((sessionCorrect / sessionCount) * 100) : 0;

    return (
        <div className="max-w-3xl mx-auto">
            <div className="flex justify-between items-center mb-6 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-3xl border border-blue-100 shadow-sm transition-all duration-500">
                <div className="flex gap-8">
                    <div>
                        <span className="text-xs text-blue-500 block font-black uppercase tracking-widest mb-1">Session</span>
                        <div className="flex items-baseline">
                            <span className="text-2xl font-black text-blue-900">{sessionCount}</span>
                            <span className="text-xs text-blue-400 font-bold ml-2">Questions</span>
                        </div>
                    </div>
                    <div>
                        <span className="text-xs text-green-500 block font-black uppercase tracking-widest mb-1">Correct</span>
                        <div className="flex items-baseline">
                            <span className="text-2xl font-black text-green-600">{sessionCorrect}</span>
                            <span className="text-xs text-green-400 font-bold ml-2">Answers</span>
                        </div>
                    </div>
                    <div>
                        <span className="text-xs text-indigo-500 block font-black uppercase tracking-widest mb-1">Accuracy</span>
                        <div className="flex items-baseline">
                            <span className="text-2xl font-black text-indigo-700">{sessionAccuracy}%</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mb-6 flex justify-between items-center">
                <div>
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-bold uppercase mr-2">
                        {currentQuestion.category} - {currentQuestion.difficulty}
                    </span>
                    <span className="text-sm text-gray-500">Topic: {currentQuestion.topic?.replace(/_/g, ' ')}</span>
                </div>
                <button onClick={resetPractice} className="text-gray-400 hover:text-gray-600 text-sm">Change</button>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                {currentQuestion.image_url && (
                    <div className="mb-6 text-center">
                        <img src={currentQuestion.image_url} alt="Problem Visualization" className="max-h-64 mx-auto border rounded shadow-sm" />
                    </div>
                )}
                <p className="text-lg font-medium text-gray-800 mb-6">{currentQuestion.question}</p>

                <div className="space-y-3">
                    {currentQuestion.options?.map((option, idx) => (
                        <button
                            key={idx}
                            onClick={() => handleAnswerSelect(idx)}
                            className={`w-full text-left p-4 rounded-lg border-2 transition-all ${selectedAnswer === idx ? 'border-blue-500 bg-blue-50' : 'border-gray-100 hover:border-blue-100'}`}
                        >
                            <span className="font-bold text-gray-400 mr-3">{String.fromCharCode(65 + idx)}.</span>
                            {option}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex justify-center">
                <button
                    onClick={submitAnswer}
                    disabled={selectedAnswer === null || loading}
                    className="px-8 py-3 bg-green-600 text-white rounded-lg font-bold hover:bg-green-700 disabled:bg-gray-300 shadow-lg"
                >
                    {loading ? 'Submitting...' : 'Submit Answer'}
                </button>
            </div>
        </div>
    );
};

export default PracticeMode;
