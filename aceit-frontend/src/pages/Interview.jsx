import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { API_BASE_URL } from '../services/api';

const Interview = () => {
  const { user } = useAuth();
  const [view, setView] = useState('setup'); // 'setup', 'chat', 'completed'
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [resumeText, setResumeText] = useState('');
  const [jdText, setJdText] = useState('');
  const [interviewType, setInterviewType] = useState('technical'); // 'technical' or 'hr'

  const handleStart = async () => {
    if (!resumeText.trim()) {
      alert('Please enter your resume summary');
      return;
    }

    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/interview/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user?.id || 'demo_user',
          resume_text: resumeText,
          jd_text: jdText || 'General Software Developer position',
          interview_type: interviewType
        })
      });

      if (!res.ok) throw new Error('Failed to start interview');

      const data = await res.json();
      setSessionId(data.session_id);
      setMessages([{ role: 'ai', text: data.text }]);
      setView('chat');
    } catch (err) {
      alert('Error: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendAnswer = async () => {
    if (!userInput.trim() || isLoading) return;

    const userMessage = userInput.trim();
    setMessages(prev => [...prev, { role: 'user', text: userMessage }]);
    setUserInput('');
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('session_id', sessionId);
      formData.append('text_answer', userMessage);

      const res = await fetch(`${API_BASE_URL}/interview/answer`, {
        method: 'POST',
        body: formData
      });

      if (!res.ok) throw new Error('Failed to process answer');

      const data = await res.json();
      setMessages(prev => [...prev, { role: 'ai', text: data.text }]);

      if (data.is_completed) {
        setTimeout(() => setView('completed'), 1000);
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', text: '❌ Error: ' + err.message }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Setup View
  if (view === 'setup') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center p-6">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">🤖 AI Interview</h1>
            <p className="text-gray-600">Chat-based mock interview powered by Gemini AI</p>
          </div>

          <div className="space-y-6">
            {/* Interview Type Selection */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                Interview Type *
              </label>
              <div className="grid grid-cols-2 gap-4">
                <button
                  type="button"
                  onClick={() => setInterviewType('technical')}
                  className={`p-4 border-2 rounded-lg transition-all ${interviewType === 'technical'
                      ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                      : 'border-gray-300 hover:border-blue-300'
                    }`}
                >
                  <div className="text-3xl mb-2">💻</div>
                  <div className="font-semibold text-gray-800">Technical</div>
                  <div className="text-xs text-gray-600 mt-1">Coding, algorithms, system design</div>
                </button>
                <button
                  type="button"
                  onClick={() => setInterviewType('hr')}
                  className={`p-4 border-2 rounded-lg transition-all ${interviewType === 'hr'
                      ? 'border-purple-500 bg-purple-50 ring-2 ring-purple-200'
                      : 'border-gray-300 hover:border-purple-300'
                    }`}
                >
                  <div className="text-3xl mb-2">👔</div>
                  <div className="font-semibold text-gray-800">HR/Behavioral</div>
                  <div className="text-xs text-gray-600 mt-1">Soft skills, experience, culture fit</div>
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Your Resume Summary *
              </label>
              <textarea
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="E.g., Experienced Python Developer with 3 years in backend development, skilled in FastAPI, PostgreSQL..."
                className="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none resize-none"
                rows="4"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Job Description (Optional)
              </label>
              <textarea
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
                placeholder="E.g., Looking for a Backend Engineer with Python expertise..."
                className="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none resize-none"
                rows="3"
              />
            </div>

            <button
              onClick={handleStart}
              disabled={isLoading || !resumeText.trim()}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold py-4 rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
            >
              {isLoading ? 'Starting Interview...' : 'Start Interview 🚀'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Completed View
  if (view === 'completed') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-900 via-teal-900 to-blue-900 flex items-center justify-center p-6">
        <div className="bg-white rounded-2xl shadow-2xl p-12 max-w-md w-full text-center">
          <div className="text-6xl mb-6">🎉</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-4">Interview Completed!</h1>
          <p className="text-gray-600 mb-8">Great job! You've completed the mock interview.</p>
          <button
            onClick={() => {
              setView('setup');
              setMessages([]);
              setSessionId(null);
              setResumeText('');
              setJdText('');
            }}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 font-semibold"
          >
            Start New Interview
          </button>
        </div>
      </div>
    );
  }

  // Chat View
  return (
    <div className="h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 shadow-lg">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">AI Interview Session</h1>
            <p className="text-sm text-blue-100">Powered by Gemini AI</p>
          </div>
          <button
            onClick={() => {
              if (confirm('Are you sure you want to end the interview?')) {
                setView('setup');
                setMessages([]);
                setSessionId(null);
              }
            }}
            className="bg-white bg-opacity-20 hover:bg-opacity-30 px-4 py-2 rounded-lg text-sm font-semibold"
          >
            End Interview
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 max-w-4xl mx-auto w-full">
        <div className="space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-2xl px-6 py-4 rounded-2xl shadow-md ${msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-800 border border-gray-200'
                  }`}
              >
                <div className="flex items-start gap-3">
                  <span className="text-2xl flex-shrink-0">
                    {msg.role === 'user' ? '👤' : '🤖'}
                  </span>
                  <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white px-6 py-4 rounded-2xl shadow-md border border-gray-200">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">🤖</span>
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 p-4 shadow-lg">
        <div className="max-w-4xl mx-auto flex gap-3">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendAnswer()}
            placeholder="Type your answer here..."
            disabled={isLoading}
            className="flex-1 px-6 py-3 border-2 border-gray-300 rounded-full focus:border-blue-500 focus:outline-none disabled:bg-gray-100"
          />
          <button
            onClick={handleSendAnswer}
            disabled={isLoading || !userInput.trim()}
            className="bg-blue-600 text-white px-8 py-3 rounded-full hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-all shadow-md"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Interview;