import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { aptitudeAPI } from '../services/api';

const Aptitude = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [score, setScore] = useState(null);
  const [timeLeft, setTimeLeft] = useState(1800); // 30 minutes in seconds
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showExplanations, setShowExplanations] = useState(false);
  const [detailedResults, setDetailedResults] = useState([]);
  const [availableTopics, setAvailableTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState('all');
  const [testMode, setTestMode] = useState('mixed'); // 'mixed' or 'topic'
  const navigate = useNavigate();

  // Fetch available topics on component mount
  useEffect(() => {
    fetchTopics();
  }, []);

  // Fetch questions on component mount
  useEffect(() => {
    fetchQuestions();
  }, [selectedTopic]);

  // Timer effect
  useEffect(() => {
    if (timeLeft > 0 && questions.length > 0 && score === null && !showExplanations) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [timeLeft, questions.length, score, showExplanations]);

  const fetchTopics = async () => {
    try {
      const response = await aptitudeAPI.getTopics();
      setAvailableTopics(response.data.topics || []);
    } catch (err) {
      console.error('Failed to fetch topics:', err);
    }
  };

  const fetchQuestions = async () => {
    try {
      console.log('Fetching questions from backend...');
      setLoading(true);
      setError('');
      
      // Prepare query parameters
      const params = {};
      if (selectedTopic && selectedTopic !== 'all') {
        params.topic = selectedTopic;
      }
      
      // Don't include explanations during the test
      params.include_explanations = false;
      
      const response = await aptitudeAPI.getQuestions(params);
      console.log('Received questions:', response.data);
      setQuestions(response.data);
      setCurrentQuestion(0);
      setAnswers({});
      setScore(null);
      setShowExplanations(false);
      setDetailedResults([]);
      setTimeLeft(1800); // Reset timer
    } catch (err) {
      console.error('Failed to fetch questions:', err);
      setError('Failed to fetch questions: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (questionId, optionIndex) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: optionIndex
    }));
  };

  const calculateScore = async () => {
    try {
      // Submit answers to backend
      const response = await aptitudeAPI.submitAnswers(answers);
      
      const correct = Object.keys(answers).reduce((acc, questionId) => {
        const question = questions.find(q => q.id === questionId);
        return acc + (question && question.correct === answers[questionId] ? 1 : 0);
      }, 0);
      
      setScore({
        correct,
        total: questions.length,
        percentage: (correct / questions.length) * 100
      });
    } catch (err) {
      setError('Failed to submit answers: ' + (err.response?.data?.detail || err.message));
    }
  };

  const fetchDetailedResults = async () => {
    try {
      const response = await aptitudeAPI.getDetailedResults({ answers });
      setDetailedResults(response.data);
      setShowExplanations(true);
    } catch (err) {
      setError('Failed to fetch detailed results: ' + (err.response?.data?.detail || err.message));
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  if (loading) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="text-xl">Loading questions...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="text-xl text-red-600">Error: {error}</div>
          <button 
            onClick={fetchQuestions}
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (showExplanations) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-bold mb-4">Detailed Results with Explanations</h2>
          <div className="mb-4">
            <p className="text-lg">You scored {score.correct} out of {score.total} questions correctly ({score.percentage.toFixed(1)}%)</p>
          </div>
          
          <div className="space-y-6">
            {detailedResults.map((result, index) => (
              <div key={result.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold">Question {index + 1}</h3>
                  <span className={`px-2 py-1 rounded text-sm ${
                    result.is_correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {result.is_correct ? 'Correct' : 'Incorrect'}
                  </span>
                </div>
                
                <p className="mb-3 font-medium">{result.question}</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-3">
                  {result.options.map((option, optIndex) => (
                    <div 
                      key={optIndex}
                      className={`p-2 rounded ${
                        optIndex === result.correct_answer 
                          ? 'bg-green-100 border border-green-500' 
                          : optIndex === result.user_answer 
                            ? 'bg-red-100 border border-red-500' 
                            : 'bg-gray-50'
                      }`}
                    >
                      <span className="font-medium mr-2">
                        {String.fromCharCode(65 + optIndex)}.
                      </span>
                      {option}
                      {optIndex === result.correct_answer && (
                        <span className="ml-2 text-green-600 font-bold">✓</span>
                      )}
                      {optIndex === result.user_answer && optIndex !== result.correct_answer && (
                        <span className="ml-2 text-red-600 font-bold">✗</span>
                      )}
                    </div>
                  ))}
                </div>
                
                <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                  <p className="font-semibold mb-1">Explanation:</p>
                  <p className="text-gray-700">{result.explanation}</p>
                </div>
              </div>
            ))}
          </div>
          
          <div className="flex gap-4 mt-6">
            <button
              onClick={() => { 
                setScore(null); 
                setCurrentQuestion(0); 
                setAnswers({}); 
                setTimeLeft(1800); 
                setShowExplanations(false);
                setDetailedResults([]);
                fetchQuestions();
              }}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              Retake Test
            </button>
            <button
              onClick={() => navigate('/')}
              className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700"
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (score !== null) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className={`w-24 h-24 mx-auto mb-6 rounded-full flex items-center justify-center text-2xl font-bold ${
            score.percentage >= 70 ? 'bg-green-100 text-green-600' :
            score.percentage >= 50 ? 'bg-yellow-100 text-yellow-600' : 'bg-red-100 text-red-600'
          }`}>
            {score.percentage.toFixed(0)}%
          </div>

          <h2 className="text-3xl font-bold mb-4">Test Completed!</h2>
          <p className="text-xl text-gray-600 mb-6">
            You scored {score.correct} out of {score.total} questions correctly
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{score.correct}</div>
              <div className="text-gray-600">Correct</div>
            </div>
            <div className="bg-red-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-red-600">{score.total - score.correct}</div>
              <div className="text-gray-600">Incorrect</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{score.percentage.toFixed(1)}%</div>
              <div className="text-gray-600">Score</div>
            </div>
          </div>

          <div className="flex gap-4 justify-center">
            <button
              onClick={fetchDetailedResults}
              className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700"
            >
              View Explanations
            </button>
            <button
              onClick={() => { 
                setScore(null); 
                setCurrentQuestion(0); 
                setAnswers({}); 
                setTimeLeft(1800); 
                fetchQuestions();
              }}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              Retake Test
            </button>
            <button
              onClick={() => navigate('/')}
              className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700"
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (questions.length === 0 && !loading) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Select Topic for Aptitude Test</h2>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Choose Topic:
            </label>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Topics (Mixed)</option>
              {availableTopics.map(topic => (
                <option key={topic} value={topic}>
                  {topic.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
          </div>
          
          <button
            onClick={fetchQuestions}
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 font-semibold"
          >
            Start Test
          </button>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;
  
  return (
    <div className="p-6 max-w-4xl mx-auto">
      {/* Header with timer and progress */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-xl font-semibold">Aptitude Practice Test</h2>
            <p className="text-sm text-gray-600">
              {selectedTopic !== 'all' 
                ? `Topic: ${selectedTopic.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}` 
                : 'Mixed Topics'}
            </p>
          </div>
          <div className="bg-red-100 text-red-600 px-3 py-1 rounded-full font-semibold">
            Time: {formatTime(timeLeft)}
          </div>
        </div>

        <div className="flex justify-between items-center text-sm text-gray-600 mb-2">
          <span>Question {currentQuestion + 1} of {questions.length}</span>
          <span>{question.type.toUpperCase()}</span>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4">{question.question}</h3>
        <div className="space-y-3">
          {question.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswer(question.id, index)}
              className={`w-full text-left p-4 rounded-lg border transition-all ${
                answers[question.id] === index
                  ? 'bg-blue-100 border-blue-500 text-blue-700'
                  : 'border-gray-300 hover:bg-gray-50 hover:border-gray-400'
              }`}
            >
              <span className="font-medium mr-2">{String.fromCharCode(65 + index)}.</span>
              {option}
            </button>
          ))}
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="flex justify-between">
        <button
          onClick={() => setCurrentQuestion(prev => Math.max(0, prev - 1))}
          disabled={currentQuestion === 0}
          className="bg-gray-500 text-white px-6 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600"
        >
          Previous
        </button>

        {currentQuestion === questions.length - 1 ? (
          <button
            onClick={calculateScore}
            className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
          >
            Submit Test
          </button>
        ) : (
          <button
            onClick={() => setCurrentQuestion(prev => prev + 1)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Next Question
          </button>
        )}
      </div>
    </div>
  );
};

export default Aptitude;