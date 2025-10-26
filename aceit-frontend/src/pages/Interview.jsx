import React, { useState, useEffect } from 'react';

const Interview = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [interviewInProgress, setInterviewInProgress] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [userResponse, setUserResponse] = useState('');
  const [feedback, setFeedback] = useState('');
  const [timeSpent, setTimeSpent] = useState(0);
  const [interviewCompleted, setInterviewCompleted] = useState(false);

  const interviewQuestions = [
    {
      id: 1,
      question: "Tell me about yourself and your background.",
      category: "Introduction",
      tips: "Focus on your education, relevant projects, and career goals. Keep it 1-2 minutes.",
      maxTime: 120
    },
    {
      id: 2,
      question: "Why do you want to work at our company?",
      category: "Motivation",
      tips: "Research the company and connect your skills to their values and projects.",
      maxTime: 90
    },
    {
      id: 3,
      question: "Describe a challenging project you worked on and how you overcame obstacles.",
      category: "Behavioral",
      tips: "Use STAR method: Situation, Task, Action, Result.",
      maxTime: 120
    },
    {
      id: 4,
      question: "What is your greatest strength and how does it apply to this role?",
      category: "Personal",
      tips: "Choose a strength relevant to the job and provide specific examples.",
      maxTime: 90
    },
    {
      id: 5,
      question: "Where do you see yourself in 5 years?",
      category: "Career Goals",
      tips: "Show ambition but also realistic planning and growth within the company.",
      maxTime: 60
    }
  ];

  useEffect(() => {
    let timer;
    if (isRecording && interviewInProgress) {
      timer = setInterval(() => {
        setTimeSpent(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [isRecording, interviewInProgress]);

  const startInterview = () => {
    setInterviewInProgress(true);
    setIsRecording(true);
    setTimeSpent(0);
    setUserResponse('');
    setFeedback('');
  };

  const stopRecording = () => {
    setIsRecording(false);
    // Simulate AI analysis
    generateFeedback();
  };

  const generateFeedback = () => {
    const question = interviewQuestions[currentQuestion];
    const feedbacks = [
      `Good response! You spoke for ${timeSpent} seconds. You covered key points about ${question.category.toLowerCase()}. Consider adding more specific examples.`,
      `Well structured answer! Your response was ${timeSpent < 30 ? 'a bit short' : timeSpent > question.maxTime ? 'too long' : 'the right length'}. Try to emphasize your achievements more.`,
      `Nice answer! You demonstrated good communication skills. For improvement: ${question.tips}`,
      `Good content! You used ${timeSpent} seconds. Remember to maintain confident body language and clear articulation.`
    ];
    
    const randomFeedback = feedbacks[Math.floor(Math.random() * feedbacks.length)];
    setFeedback(randomFeedback);
  };

  const nextQuestion = () => {
    if (currentQuestion < interviewQuestions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
      setIsRecording(true);
      setTimeSpent(0);
      setUserResponse('');
      setFeedback('');
    } else {
      // End interview
      setIsRecording(false);
      setInterviewInProgress(false);
      setInterviewCompleted(true);
    }
  };

  const restartInterview = () => {
    setInterviewInProgress(false);
    setInterviewCompleted(false);
    setCurrentQuestion(0);
    setTimeSpent(0);
    setUserResponse('');
    setFeedback('');
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  if (interviewCompleted) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="w-24 h-24 mx-auto mb-6 bg-green-100 rounded-full flex items-center justify-center">
            <span className="text-2xl font-bold text-green-600">✓</span>
          </div>
          
          <h2 className="text-3xl font-bold mb-4 text-gray-800">Interview Completed!</h2>
          <p className="text-xl text-gray-600 mb-6">
            Great job completing the mock interview!
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{interviewQuestions.length}</div>
              <div className="text-gray-600">Questions</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">Good</div>
              <div className="text-gray-600">Overall Performance</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">85%</div>
              <div className="text-gray-600">Confidence Score</div>
            </div>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-yellow-800 mb-2">Areas for Improvement:</h3>
            <ul className="text-left text-yellow-700 text-sm list-disc list-inside">
              <li>Practice speaking more concisely</li>
              <li>Include more specific examples in your answers</li>
              <li>Work on maintaining eye contact</li>
            </ul>
          </div>

          <div className="flex gap-4 justify-center">
            <button 
              onClick={restartInterview}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              Practice Again
            </button>
            <button 
              onClick={() => window.location.href = '/'}
              className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700"
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!interviewInProgress) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="w-20 h-20 mx-auto mb-6 bg-blue-100 rounded-full flex items-center justify-center">
            <span className="text-2xl">🎤</span>
          </div>
          
          <h2 className="text-3xl font-bold mb-4 text-gray-800">AceIt Mock Interview</h2>
          <p className="text-xl text-gray-600 mb-6">
            Practice with AI-powered interview questions and get instant feedback on your responses.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="font-semibold mb-3 text-gray-800">What to Expect:</h3>
              <ul className="text-left text-gray-600 space-y-2">
                <li>• 5 common interview questions</li>
                <li>• Voice recording simulation</li>
                <li>• AI-powered feedback</li>
                <li>• Time management tips</li>
                <li>• Performance analytics</li>
              </ul>
            </div>
            
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="font-semibold mb-3 text-gray-800">Tips for Success:</h3>
              <ul className="text-left text-gray-600 space-y-2">
                <li>• Speak clearly and confidently</li>
                <li>• Use the STAR method for examples</li>
                <li>• Keep answers 1-2 minutes long</li>
                <li>• Maintain good posture</li>
                <li>• Practice active listening</li>
              </ul>
            </div>
          </div>

          <button
            onClick={startInterview}
            className="bg-purple-600 text-white px-8 py-3 rounded-lg hover:bg-purple-700 text-lg font-semibold"
          >
            Start Mock Interview
          </button>
        </div>
      </div>
    );
  }

  const question = interviewQuestions[currentQuestion];
  const progress = ((currentQuestion + 1) / interviewQuestions.length) * 100;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      {/* Interview Progress */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800">Mock Interview</h2>
          <div className="flex items-center gap-4">
            <div className="bg-blue-100 text-blue-600 px-3 py-1 rounded-full font-semibold">
              Q: {currentQuestion + 1}/{interviewQuestions.length}
            </div>
            <div className={`px-3 py-1 rounded-full font-semibold ${
              isRecording ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-600'
            }`}>
              {isRecording ? '● Recording' : '⏸️ Paused'}
            </div>
          </div>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-purple-600 h-2 rounded-full transition-all duration-300" 
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <span className="bg-blue-100 text-blue-600 px-2 py-1 rounded text-sm font-medium">
              {question.category}
            </span>
            <h3 className="text-xl font-semibold mt-2 text-gray-800">{question.question}</h3>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-700">{formatTime(timeSpent)}</div>
            <div className="text-sm text-gray-500">Time Spent</div>
          </div>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h4 className="font-semibold text-yellow-800 mb-1">💡 Tip:</h4>
          <p className="text-yellow-700 text-sm">{question.tips}</p>
        </div>
      </div>

      {/* Response Area */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold mb-3 text-gray-800">Your Response:</h3>
        <textarea
          value={userResponse}
          onChange={(e) => setUserResponse(e.target.value)}
          placeholder="Type your answer here or speak your response aloud..."
          className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        />
        
        <div className="flex gap-3 mt-4">
          <button
            onClick={() => setIsRecording(!isRecording)}
            className={`px-6 py-2 rounded-lg font-semibold ${
              isRecording 
                ? 'bg-red-600 hover:bg-red-700 text-white' 
                : 'bg-green-600 hover:bg-green-700 text-white'
            }`}
          >
            {isRecording ? '⏸️ Stop Recording' : '● Start Recording'}
          </button>
          
          <button
            onClick={stopRecording}
            disabled={!isRecording}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Get Feedback
          </button>
        </div>
      </div>

      {/* AI Feedback */}
      {feedback && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6 border-l-4 border-green-500">
          <h3 className="text-lg font-semibold mb-3 text-gray-800 flex items-center">
            <span className="text-green-500 mr-2">🤖</span>
            AI Feedback
          </h3>
          <p className="text-gray-700 bg-green-50 p-4 rounded-lg">{feedback}</p>
        </div>
      )}

      {/* Navigation */}
      <div className="flex justify-between">
        <button
          onClick={() => setCurrentQuestion(prev => Math.max(0, prev - 1))}
          disabled={currentQuestion === 0}
          className="bg-gray-500 text-white px-6 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600"
        >
          Previous Question
        </button>
        
        <button
          onClick={nextQuestion}
          className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700"
        >
          {currentQuestion === interviewQuestions.length - 1 ? 'Finish Interview' : 'Next Question'}
        </button>
      </div>
    </div>
  );
};

export default Interview;