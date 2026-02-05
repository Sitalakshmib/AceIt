import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { mockTestAPI, aptitudeAPI } from '../services/api';

const MockTest = () => {
    const [view, setView] = useState('selection'); // 'selection', 'test', 'results', 'review'
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

    // Results/Review state
    const [results, setResults] = useState(null);
    const [reviewData, setReviewData] = useState(null);

    const navigate = useNavigate();

    // Timer effect
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
            setAnswers({});
            setCurrentQuestion(0);

            const totalSeconds = response.data.duration_minutes * 60;
            setDuration(totalSeconds);
            setTimeLeft(totalSeconds);
            setTestStartTime(Date.now());

            setView('test');
            setQuestionStartTime(Date.now());
        } catch (err) {
            console.error('Failed to start test:', err);
            setError('Failed to start test. Please try again.');
        }
    };

    const handleAnswer = async (questionId, optionIndex, optionText) => {
        const timeSpent = Math.floor((Date.now() - questionStartTime) / 1000);
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

    const handleViewReview = async () => {
        try {
            console.log('[MockTest] handleViewReview clicked', { testId, attemptId });
            setLoading(true);
            const response = await mockTestAPI.getResults(testId, attemptId);
            console.log('[MockTest] Review data received:', response.data);
            setReviewData(response.data);
            setView('review');
            window.scrollTo(0, 0);
        } catch (err) {
            console.error('[MockTest] Failed to fetch review data:', err);
            setError('Failed to load detailed review. Please try again.');
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
                        <div>
                            <label className="block text-gray-700 font-semibold mb-3">Select Test Type</label>
                            <div className="grid md:grid-cols-3 gap-4">
                                <div onClick={() => { setTestType('full_length'); setSelectedCategory(''); setSelectedTopic(''); }}
                                    className={`p-6 border-2 rounded-lg cursor-pointer transition-all ${testType === 'full_length' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-blue-300'}`}>
                                    <h3 className="font-bold text-lg mb-2">Full-Length Test</h3>
                                    <p className="text-sm text-gray-600">30 questions</p>
                                    <p className="text-sm text-gray-600">30 minutes</p>
                                </div>
                                <div onClick={() => { setTestType('section_wise'); setSelectedTopic(''); }}
                                    className={`p-6 border-2 rounded-lg cursor-pointer transition-all ${testType === 'section_wise' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-blue-300'}`}>
                                    <h3 className="font-bold text-lg mb-2">Section Test</h3>
                                    <p className="text-sm text-gray-600">30 questions</p>
                                    <p className="text-sm text-gray-600">30 minutes</p>
                                </div>
                                <div onClick={() => { setTestType('topic_wise'); setSelectedTopic(''); }}
                                    className={`p-6 border-2 rounded-lg cursor-pointer transition-all ${testType === 'topic_wise' ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' : 'border-gray-200 hover:border-blue-300'}`}>
                                    <h3 className="font-bold text-lg mb-2">Topic Test</h3>
                                    <p className="text-sm text-gray-600">20 questions</p>
                                    <p className="text-sm text-gray-600">20 minutes</p>
                                </div>
                            </div>
                        </div>

                        {testType !== 'full_length' && (
                            <div className="grid md:grid-cols-2 gap-4 bg-gray-50 p-6 rounded-lg">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Select Category</label>
                                    <select value={selectedCategory} onChange={(e) => { setSelectedCategory(e.target.value); setSelectedTopic(''); }}
                                        className="w-full p-3 border rounded-lg bg-white" disabled={catsLoading}>
                                        <option value="">{catsLoading ? 'Loading Categories...' : '-- Choose Category --'}</option>
                                        {Object.keys(categories).map(cat => <option key={cat} value={cat}>{cat}</option>)}
                                    </select>
                                </div>
                                {testType === 'topic_wise' && (
                                    <div>
                                        <label className="block text-sm font-semibold text-gray-700 mb-2">Select Topic</label>
                                        <select value={selectedTopic} onChange={(e) => setSelectedTopic(e.target.value)}
                                            className="w-full p-3 border rounded-lg bg-white" disabled={!selectedCategory || catsLoading}>
                                            <option value="">-- Choose Topic --</option>
                                            {selectedCategory && (categories[selectedCategory] || []).map(topic => (
                                                <option key={topic} value={topic}>{topic.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</option>
                                            ))}
                                        </select>
                                    </div>
                                )}
                            </div>
                        )}

                        <button onClick={generateTest} disabled={loading || (testType === 'section_wise' && !selectedCategory) || (testType === 'topic_wise' && (!selectedCategory || !selectedTopic))}
                            className="w-full bg-blue-600 text-white py-4 rounded-lg font-bold text-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors shadow-lg">
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

        return (
            <div className="p-6 max-w-4xl mx-auto">
                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 p-4 bg-gray-50 rounded-xl border border-gray-100">
                        <div className="flex flex-col items-center justify-center p-2 bg-white rounded-lg shadow-sm border border-gray-100">
                            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Time Left</span>
                            <span className={`text-xl font-mono font-bold ${timeLeft < 300 ? 'text-red-600 animate-pulse' : 'text-blue-600'}`}>
                                {formatTime(timeLeft)}
                            </span>
                        </div>
                        <div className="flex flex-col items-center justify-center p-2 bg-white rounded-lg shadow-sm border border-gray-100">
                            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Attempted</span>
                            <span className="text-xl font-bold text-green-600">{Object.keys(answers).length}</span>
                        </div>
                        <div className="flex flex-col items-center justify-center p-2 bg-white rounded-lg shadow-sm border border-gray-100">
                            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Remaining</span>
                            <span className="text-xl font-bold text-orange-500">{questions.length - Object.keys(answers).length}</span>
                        </div>
                        <div className="flex flex-col items-center justify-center p-2 bg-white rounded-lg shadow-sm border border-gray-100">
                            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Question</span>
                            <span className="text-xl font-bold text-gray-800">{currentQuestion + 1}<span className="text-sm text-gray-400 font-normal"> / {questions.length}</span></span>
                        </div>
                    </div>

                    <div className="mb-6 pb-2 border-b border-gray-100">
                        <h2 className="text-2xl font-bold text-gray-800 capitalize">
                            {testType.replace(/_/g, ' ')}
                            <span className="ml-3 px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">{question.category}</span>
                        </h2>
                    </div>

                    <div className="mb-6">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                            <div className="bg-blue-600 h-2 rounded-full transition-all duration-500" style={{ width: `${progressPercent}%` }}></div>
                        </div>
                    </div>

                    <div className="text-lg font-medium text-gray-800 mb-8 leading-relaxed">
                        {question.question}
                        {question.image_url && (
                            <div className="mt-6 mb-4 flex justify-center">
                                <img src={question.image_url} alt="Question Diagram" className="max-w-full h-auto max-h-96 rounded-lg border shadow-sm object-contain" />
                            </div>
                        )}
                    </div>

                    <div className="grid gap-3 mb-8">
                        {question.options.map((opt, idx) => (
                            <button key={idx} onClick={() => handleAnswer(question.id, idx, opt)}
                                className={`text-left p-4 rounded-lg border-2 transition-all ${answers[question.id] === idx ? 'border-blue-500 bg-blue-50 text-blue-800' : 'border-gray-200 hover:border-blue-200 hover:bg-gray-50'}`}>
                                <span className="inline-block w-8 font-bold text-gray-400">{String.fromCharCode(65 + idx)}</span>
                                {opt}
                            </button>
                        ))}
                    </div>

                    <div className="flex justify-between pt-6 border-t">
                        <button onClick={handlePrevious} disabled={currentQuestion === 0} className="px-6 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50">← Previous</button>
                        {currentQuestion === questions.length - 1 ? (
                            <button onClick={handleCompleteTest} disabled={loading} className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-bold shadow-md">
                                {loading ? 'Submitting...' : 'Submit Test'}
                            </button>
                        ) : (
                            <button onClick={handleNext} className="px-8 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold">Next →</button>
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
                    <div className="text-center mb-10">
                        <h2 className="text-3xl font-bold text-gray-800 mb-2">Mock Test Completed!</h2>
                        <p className="text-gray-500">Here's how you performed</p>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
                        <div className="bg-blue-50 p-6 rounded-xl border border-blue-100 flex flex-col items-center">
                            <span className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">Score</span>
                            <span className="text-3xl font-black text-blue-600">{results.score} / {results.total}</span>
                        </div>
                        <div className="bg-green-50 p-6 rounded-xl border border-green-100 flex flex-col items-center">
                            <span className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">Accuracy</span>
                            <span className="text-3xl font-black text-green-600">{results.accuracy.toFixed(0)}%</span>
                        </div>
                        <div className="bg-orange-50 p-6 rounded-xl border border-orange-100 flex flex-col items-center">
                            <span className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">Avg Time</span>
                            <span className="text-3xl font-black text-orange-600">{Math.round(results.average_time_per_question || 0)}s</span>
                        </div>
                        <div className="bg-purple-50 p-6 rounded-xl border border-purple-100 flex flex-col items-center">
                            <span className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">Rating</span>
                            <span className="text-2xl font-black text-purple-600">{results.accuracy >= 75 ? 'Good' : results.accuracy >= 50 ? 'Average' : 'Poor'}</span>
                        </div>
                    </div>

                    {results.topic_performance && (
                        <div className="mb-8">
                            <h3 className="text-xl font-bold mb-4 text-gray-800">Topic Performance</h3>
                            <div className="grid md:grid-cols-2 gap-4">
                                {Object.entries(results.topic_performance).map(([topic, stats]) => (
                                    <div key={topic} className="bg-gray-50 p-4 rounded-lg flex justify-between items-center border border-gray-100">
                                        <span className="font-semibold text-gray-700 capitalize">{topic.replace(/_/g, ' ')}</span>
                                        <div className="text-right">
                                            <div className={`font-bold text-lg ${stats.accuracy >= 75 ? 'text-green-600' : 'text-orange-600'}`}>{stats.accuracy.toFixed(0)}%</div>
                                            <div className="text-xs text-gray-500 font-medium">{stats.correct} / {stats.total} Correct</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    <div className="flex flex-wrap gap-4 justify-center mt-10">
                        <button onClick={handleViewReview} className="px-8 py-3 bg-indigo-600 text-white rounded-lg font-bold shadow-lg hover:bg-indigo-700 transition-all">Review Detailed Answers</button>
                        <button onClick={() => setView('selection')} className="px-8 py-3 bg-blue-600 text-white rounded-lg font-bold shadow-lg hover:bg-blue-700 transition-all">Take Another Test</button>
                        <button onClick={() => navigate('/')} className="px-8 py-3 bg-white border border-gray-200 text-gray-700 rounded-lg font-bold hover:bg-gray-50 transition-all">Back to Dashboard</button>
                    </div>
                </div>
            </div>
        );
    }

    // Review Screen
    if (view === 'review' && reviewData) {
        return (
            <div className="p-6 max-w-5xl mx-auto">
                <div className="flex justify-between items-center mb-8 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
                    <button onClick={() => setView('results')} className="text-blue-600 font-bold flex items-center gap-2 hover:underline">← Back to Summary</button>
                    <h2 className="text-xl font-black text-gray-800">Detailed Review</h2>
                    <div className="font-bold text-gray-500">{reviewData.score} / {reviewData.total}</div>
                </div>

                <div className="space-y-6">
                    {reviewData.detailed_results.map((item, idx) => (
                        <div key={idx} className={`bg-white rounded-2xl shadow-sm border-2 overflow-hidden ${item.is_correct ? 'border-green-100' : 'border-red-100'}`}>
                            <div className={`px-6 py-2 flex justify-between items-center ${item.is_correct ? 'bg-green-50' : 'bg-red-50'}`}>
                                <span className={`text-[10px] font-black uppercase tracking-widest ${item.is_correct ? 'text-green-600' : 'text-red-600'}`}>Question {idx + 1} • {item.topic}</span>
                                <span className={`text-[10px] font-black ${item.is_correct ? 'text-green-600' : 'text-red-600'}`}>{item.is_correct ? 'CORRECT' : 'INCORRECT'}</span>
                            </div>
                            <div className="p-6">
                                <p className="text-2xl text-gray-800 font-medium mb-6 leading-relaxed">{item.question_text}</p>
                                {item.image_url && <img src={item.image_url} alt="" className="mb-6 max-h-64 mx-auto rounded border" />}

                                <div className="grid gap-3 mb-8">
                                    {item.options && item.options.map((opt, optIdx) => {
                                        let statusClass = "border-gray-200 bg-white text-gray-600";
                                        const isSelected = item.your_answer === opt;
                                        const isCorrect = item.correct_answer === opt;

                                        if (isCorrect) {
                                            statusClass = "border-green-500 bg-green-50 text-green-800 font-bold";
                                        } else if (isSelected && !isCorrect) {
                                            statusClass = "border-red-500 bg-red-50 text-red-800 font-bold";
                                        }

                                        return (
                                            <div key={optIdx} className={`p-4 rounded-lg border-2 flex items-center gap-3 ${statusClass}`}>
                                                <span className="font-bold text-sm w-6 h-6 flex items-center justify-center rounded-full border border-current opacity-60">
                                                    {String.fromCharCode(65 + optIdx)}
                                                </span>
                                                <span className="text-lg">{opt}</span>
                                                {isCorrect && <span className="ml-auto text-green-600 font-bold text-sm">✓ Correct Answer</span>}
                                                {isSelected && !isCorrect && <span className="ml-auto text-red-600 font-bold text-sm">✗ Your Answer</span>}
                                            </div>
                                        );
                                    })}
                                </div>

                                <div className="grid md:grid-cols-2 gap-4 mb-6">
                                    <div className={`p-4 rounded-xl border ${item.is_correct ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                                        <span className="text-[10px] text-gray-400 block font-black uppercase mb-1">Your Selected Answer</span>
                                        <p className="font-bold text-lg">{item.your_answer}</p>
                                    </div>
                                    {!item.is_correct && (
                                        <div className="p-4 rounded-xl border border-blue-200 bg-blue-50">
                                            <span className="text-[10px] text-gray-400 block font-black uppercase mb-1">Correct Answer</span>
                                            <p className="font-bold text-blue-800 text-lg">{item.correct_answer}</p>
                                        </div>
                                    )}
                                </div>
                                <div className="bg-gray-50 rounded-xl p-5 border border-gray-100">
                                    <span className="text-[10px] text-blue-500 font-black uppercase mb-2 block">Explanation</span>
                                    <p className="text-lg text-gray-700 leading-relaxed whitespace-pre-wrap">{item.explanation}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
                <div className="text-center py-10">
                    <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} className="text-blue-600 font-bold hover:underline">Back to Top</button>
                </div>
            </div>
        );
    }

    return (
        <div className="flex items-center justify-center min-h-[400px]">
            <div className="animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
        </div>
    );
};

export default MockTest;
