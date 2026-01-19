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
        await fetchNextQuestion();
    };

    const fetchNextQuestion = async () => {
        try {
            setLoading(true);
            setError('');
            setShowFeedback(false);
            setSelectedAnswer(null);
            setFeedback(null);

            const topic = selectedTopic === 'all' ? null : selectedTopic;
            const response = await aptitudeAPI.getNextQuestion(selectedCategory, topic);

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
        if (showFeedback) return; // Prevent changing answer after submission
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
                timeSpent
            );

            setFeedback(response.data);
            setShowFeedback(true);
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

    // Selection Screen
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
                    {/* Category Selection */}
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

                    {/* Topic Selection */}
                    <div className={`transition-opacity ${selectedCategory ? 'opacity-100' : 'opacity-50 pointer-events-none'}`}>
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
                            <h4 className="font-semibold text-blue-800 mb-2">📚 Practice Mode Features:</h4>
                            <ul className="text-sm text-blue-900 space-y-1">
                                <li>✓ One question at a time</li>
                                <li>✓ Instant feedback with explanations</li>
                                <li>✓ No question repetition</li>
                                <li>✓ Adaptive difficulty progression</li>
                                <li>✓ No timer - learn at your pace</li>
                            </ul>
                        </div>

                        <button
                            onClick={startPractice}
                            disabled={!selectedCategory}
                            className="w-full bg-blue-600 text-white py-4 rounded-lg font-bold text-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors shadow-lg"
                        >
                            Start Practice 🚀
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    // Loading State
    if (loading && !currentQuestion) {
        return (
            <div className="text-center py-12">
                <div className="animate-pulse text-gray-600">Loading question...</div>
            </div>
        );
    }

    // No More Questions
    if (!currentQuestion && !loading) {
        return (
            <div className="max-w-2xl mx-auto text-center">
                <div className="bg-green-50 border border-green-200 rounded-lg p-8">
                    <div className="text-6xl mb-4">🎉</div>
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

    // Question Display (Before Feedback)
    if (currentQuestion && !showFeedback) {
        return (
            <div className="max-w-3xl mx-auto">
                {/* Header */}
                <div className="mb-6">
                    <div className="flex justify-between items-center mb-2">
                        <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-bold uppercase">
                            {currentQuestion.category} • {currentQuestion.difficulty}
                        </span>
                        <button
                            onClick={resetPractice}
                            className="text-gray-500 hover:text-gray-700 text-sm"
                        >
                            ← Change Topic
                        </button>
                    </div>
                    <h3 className="text-sm text-gray-600">
                        Topic: {currentQuestion.topic?.replace(/_/g, ' ')}
                    </h3>
                </div>

                {/* Question */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                    <div className="text-lg font-medium text-gray-800 mb-6 leading-relaxed">
                        {currentQuestion.question}
                    </div>

                    {/* Options */}
                    <div className="space-y-3">
                        {currentQuestion.options?.map((option, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleAnswerSelect(idx)}
                                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${selectedAnswer === idx
                                        ? 'border-blue-500 bg-blue-50 text-blue-800'
                                        : 'border-gray-200 hover:border-blue-200 hover:bg-gray-50'
                                    }`}
                            >
                                <span className="inline-block w-8 font-bold text-gray-400">
                                    {String.fromCharCode(65 + idx)}.
                                </span>
                                {option}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Submit Button */}
                <div className="flex justify-center">
                    <button
                        onClick={submitAnswer}
                        disabled={selectedAnswer === null || loading}
                        className="px-8 py-3 bg-green-600 text-white rounded-lg font-bold text-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors shadow-lg"
                    >
                        {loading ? 'Submitting...' : 'Submit Answer'}
                    </button>
                </div>

                {error && (
                    <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded text-center">
                        {error}
                    </div>
                )}
            </div>
        );
    }

    // Feedback Display (After Submission)
    if (showFeedback && feedback) {
        const isCorrect = feedback.is_correct;

        return (
            <div className="max-w-3xl mx-auto">
                {/* Result Banner */}
                <div className={`rounded-lg p-6 mb-6 ${isCorrect ? 'bg-green-50 border-2 border-green-500' : 'bg-red-50 border-2 border-red-500'
                    }`}>
                    <div className="flex items-center justify-center mb-4">
                        <div className={`text-6xl ${isCorrect ? 'text-green-600' : 'text-red-600'}`}>
                            {isCorrect ? '✓' : '✗'}
                        </div>
                    </div>
                    <h2 className={`text-2xl font-bold text-center mb-2 ${isCorrect ? 'text-green-800' : 'text-red-800'
                        }`}>
                        {isCorrect ? 'Correct!' : 'Incorrect'}
                    </h2>
                    <p className={`text-center ${isCorrect ? 'text-green-700' : 'text-red-700'}`}>
                        {isCorrect ? 'Great job! Keep it up!' : 'Don\'t worry, learn from the explanation below.'}
                    </p>
                </div>

                {/* Question Review */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                    <h3 className="font-semibold text-gray-700 mb-4">Question:</h3>
                    <p className="text-gray-800 mb-6">{currentQuestion.question}</p>

                    {/* Options with Correct Answer Highlighted */}
                    <div className="space-y-2 mb-6">
                        {feedback.options?.map((option, idx) => (
                            <div
                                key={idx}
                                className={`p-3 rounded border ${idx === feedback.correct_answer
                                        ? 'bg-green-100 border-green-400 text-green-800'
                                        : idx === feedback.user_answer && !isCorrect
                                            ? 'bg-red-100 border-red-400 text-red-800'
                                            : 'bg-gray-50 border-gray-200'
                                    }`}
                            >
                                <span className="font-bold mr-2">{String.fromCharCode(65 + idx)}.</span>
                                {option}
                                {idx === feedback.correct_answer && (
                                    <span className="ml-2 text-green-600 font-semibold">✓ Correct Answer</span>
                                )}
                                {idx === feedback.user_answer && idx !== feedback.correct_answer && (
                                    <span className="ml-2 text-red-600 font-semibold">← Your Answer</span>
                                )}
                            </div>
                        ))}
                    </div>

                    {/* Explanation */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h4 className="font-semibold text-blue-800 mb-2">💡 Explanation:</h4>
                        <p className="text-blue-900">{feedback.explanation || 'No explanation available.'}</p>
                    </div>
                </div>

                {/* Adaptive Feedback */}
                {feedback.adaptive_feedback && (
                    <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
                        <h4 className="font-semibold text-purple-800 mb-2">📊 Your Progress:</h4>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                                <span className="text-purple-700">Overall Accuracy:</span>
                                <span className="ml-2 font-bold text-purple-900">
                                    {feedback.adaptive_feedback.overall_accuracy}%
                                </span>
                            </div>
                            <div>
                                <span className="text-purple-700">Questions Attempted:</span>
                                <span className="ml-2 font-bold text-purple-900">
                                    {feedback.adaptive_feedback.questions_attempted}
                                </span>
                            </div>
                        </div>
                        {feedback.adaptive_feedback.message && (
                            <div className="mt-3 p-2 bg-purple-100 rounded text-purple-800 text-sm">
                                🎯 {feedback.adaptive_feedback.message}
                            </div>
                        )}
                    </div>
                )}

                {/* Next Question Button */}
                <div className="flex justify-center gap-4">
                    <button
                        onClick={handleNextQuestion}
                        className="px-8 py-3 bg-blue-600 text-white rounded-lg font-bold text-lg hover:bg-blue-700 transition-colors shadow-lg"
                    >
                        Next Question →
                    </button>
                    <button
                        onClick={resetPractice}
                        className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                    >
                        Change Topic
                    </button>
                </div>
            </div>
        );
    }

    return null;
};

export default PracticeMode;
