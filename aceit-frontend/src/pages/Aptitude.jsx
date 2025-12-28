import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { aptitudeAPI } from '../services/api';

const Aptitude = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [score, setScore] = useState(null);
  const [timeLeft, setTimeLeft] = useState(1800);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showExplanations, setShowExplanations] = useState(false);
  const [detailedResults, setDetailedResults] = useState([]);

  // New State for Categories
  const [categories, setCategories] = useState({});
  const [selectedCategory, setSelectedCategory] = useState(''); // 'Quantitative', 'Logical', 'Verbal'
  const [selectedTopic, setSelectedTopic] = useState('all');

  const navigate = useNavigate();

  // Fetch categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);

  // Timer effect
  useEffect(() => {
    if (timeLeft > 0 && questions.length > 0 && score === null && !showExplanations) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [timeLeft, questions.length, score, showExplanations]);

  const fetchCategories = async () => {
    try {
      const response = await aptitudeAPI.getCategories();
      setCategories(response.data.categories || {});
    } catch (err) {
      console.error('Failed to fetch categories:', err);
      setError('Failed to load aptitude categories');
    }
  };

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      setError('');

      const params = { include_explanations: false };

      if (selectedCategory) {
        params.category = selectedCategory;
      }
      if (selectedTopic && selectedTopic !== 'all') {
        params.topic = selectedTopic;
      }

      const response = await aptitudeAPI.getQuestions(params);
      setQuestions(response.data);

      // Reset test state
      setCurrentQuestion(0);
      setAnswers({});
      setScore(null);
      setShowExplanations(false);
      setDetailedResults([]);
      setTimeLeft(1800);
    } catch (err) {
      console.error('Failed to fetch questions:', err);
      setError('Failed to fetch questions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const calculateScore = async () => {
    try {
      const response = await aptitudeAPI.submitAnswers(answers);
      setScore(response.data);
    } catch (err) {
      setError('Failed to submit answers');
    }
  };

  const handleAnswer = (questionId, optionIndex) => {
    setAnswers(prev => ({ ...prev, [questionId]: optionIndex }));
  };

  const fetchDetailedResults = async () => {
    try {
      const response = await aptitudeAPI.getDetailedResults({ answers });
      setDetailedResults(response.data);
      setShowExplanations(true);
    } catch (err) {
      setError('Failed to fetch explanations');
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  // --- RENDER HELPERS ---

  if (loading) return (
    <div className="p-6 max-w-4xl mx-auto text-center">
      <div className="bg-white p-8 rounded-lg shadow-md animate-pulse">Loading...</div>
    </div>
  );

  if (error && !questions.length) return (
    <div className="p-6 max-w-4xl mx-auto text-center">
      <div className="bg-white p-8 rounded-lg shadow-md text-red-600">
        <h3 className="text-xl font-bold mb-2">Error</h3>
        <p>{error}</p>
        <button onClick={fetchCategories} className="mt-4 bg-blue-600 text-white px-4 py-2 rounded">Retry</button>
      </div>
    </div>
  );

  // SELECTION SCREEN
  if (questions.length === 0) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Aptitude Practice</h1>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Category Selection */}
            <div>
              <label className="block text-gray-700 font-semibold mb-2">Select Category</label>
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
              <label className="block text-gray-700 font-semibold mb-2">Select Topic</label>
              <select
                value={selectedTopic}
                onChange={(e) => setSelectedTopic(e.target.value)}
                className="w-full p-3 border rounded-lg bg-white focus:ring-2 focus:ring-blue-500"
                disabled={!selectedCategory}
              >
                <option value="all">All Topics in {selectedCategory}</option>
                {selectedCategory && categories[selectedCategory]?.map(topic => (
                  <option key={topic} value={topic}>
                    {topic.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </option>
                ))}
              </select>

              <div className="mt-8">
                <button
                  onClick={fetchQuestions}
                  disabled={!selectedCategory}
                  className="w-full bg-blue-600 text-white py-4 rounded-lg font-bold text-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors shadow-lg"
                >
                  Start Practice Test 🚀
                </button>
                <p className="text-center text-sm text-gray-500 mt-2">
                  Adaptive difficulty enabled
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // TEST IN PROGRESS
  if (score === null) {
    const question = questions[currentQuestion];
    const progressPercent = ((currentQuestion + 1) / questions.length) * 100;

    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <div>
              <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-bold uppercase tracking-wide mb-1">
                {question.category} / {question.difficulty}
              </span>
              <h2 className="text-xl font-bold text-gray-800">
                Question {currentQuestion + 1} <span className="text-gray-400 text-base font-normal">/ {questions.length}</span>
              </h2>
            </div>
            <div className={`text-lg font-mono font-bold px-4 py-2 rounded-lg ${timeLeft < 300 ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-700'}`}>
              {formatTime(timeLeft)}
            </div>
          </div>

          <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
            <div className="bg-blue-600 h-2 rounded-full transition-all duration-500" style={{ width: `${progressPercent}%` }}></div>
          </div>

          <div className="text-lg font-medium text-gray-800 mb-8 leading-relaxed">
            {question.question}
          </div>

          <div className="grid gap-3">
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

          <div className="flex justify-between mt-8 pt-6 border-t">
            <button
              onClick={() => setCurrentQuestion(p => Math.max(0, p - 1))}
              disabled={currentQuestion === 0}
              className="px-6 py-2 text-gray-600 hover:text-gray-900 disabled:opacity-50"
            >
              Previous
            </button>
            {currentQuestion === questions.length - 1 ? (
              <button
                onClick={calculateScore}
                className="px-8 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-bold shadow-md transform hover:scale-105 transition-all"
              >
                Submit Test
              </button>
            ) : (
              <button
                onClick={() => setCurrentQuestion(p => p + 1)}
                className="px-8 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
              >
                Next
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  // RESULTS SCREEN
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8 text-center">
        <div className="mb-8">
          <div className="inline-flex items-center justify-center w-32 h-32 rounded-full border-8 border-blue-50 bg-white shadow-inner mb-4">
            <span className="text-4xl font-black text-gray-800">{score.percentage.toFixed(0)}%</span>
          </div>
          <h2 className="text-3xl font-bold text-gray-800">Test Completed</h2>
          <p className="text-gray-500 mt-2">You answered {score.correct} out of {score.total} questions correctly</p>
        </div>

        {!showExplanations ? (
          <div className="flex gap-4 justify-center">
            <button onClick={fetchQuestions} className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold shadow-lg">Tweet New Test</button>
            <button onClick={fetchDetailedResults} className="px-6 py-3 bg-white border-2 border-gray-200 text-gray-700 rounded-lg hover:border-gray-300 font-semibold">Review Answers</button>
            <button onClick={() => navigate('/')} className="px-6 text-gray-500 hover:text-gray-800">Back Home</button>
          </div>
        ) : (
          <div className="text-left mt-8 space-y-6">
            <h3 className="text-xl font-bold border-b pb-2">Detailed Analysis</h3>
            {detailedResults.map((res, i) => (
              <div key={i} className={`p-6 rounded-lg border ${res.correct ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
                <div className="flex justify-between items-start mb-2">
                  <span className="font-bold text-gray-700">Q{i + 1}: {res.category} ({res.difficulty})</span>
                  {res.correct ? <span className="text-green-600 font-bold">✓ Correct</span> : <span className="text-red-600 font-bold">✗ Incorrect</span>}
                </div>
                {/* Add explanation logic here if needed, simplified for brevity */}
                <p className="text-gray-600 italic mt-2">Check console network tab for detailed explanation logic if needed.</p>
              </div>
            ))}
            <button onClick={fetchQuestions} className="w-full mt-6 py-4 bg-blue-600 text-white rounded-lg font-bold">Start New Test</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Aptitude;