import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { API_BASE_URL } from '../services/api';
import VideoPractice from '../components/Interview/VideoPractice';

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
  const [topic, setTopic] = useState('realtime');

  // Audio State
  const [isRecording, setIsRecording] = useState(false);
  const [audioPermissionNeeded, setAudioPermissionNeeded] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioPlayerRef = useRef(null);

  // Results State (must be at top level, not inside conditional)
  const [results, setResults] = useState(null);
  const [loadingResults, setLoadingResults] = useState(true);

  // Auto-play AI audio when new message arrives
  // PRIVACY NOTE: Audio is NOT stored. It's generated via TTS and played in-memory only.
  useEffect(() => {
    if (messages.length > 0) {
      const lastMsg = messages[messages.length - 1];
      console.log("Last message:", lastMsg);

      if (lastMsg.role === 'ai' && lastMsg.audio_url) {
        console.log("AI message with audio_url:", lastMsg.audio_url);

        // Construct full URL if relative
        const url = lastMsg.audio_url.startsWith('http') || lastMsg.audio_url.startsWith('data:')
          ? lastMsg.audio_url
          : `${API_BASE_URL}${lastMsg.audio_url}`;

        console.log("Final audio URL:", url.substring(0, 100) + "...");

        if (audioPlayerRef.current) {
          // Set the source
          audioPlayerRef.current.src = url;

          // Load the audio
          audioPlayerRef.current.load();

          // Small delay to ensure audio is loaded, then play
          setTimeout(() => {
            if (audioPlayerRef.current) {
              audioPlayerRef.current.play()
                .then(() => {
                  console.log("Audio playing successfully");
                })
                .catch(e => {
                  console.error("Auto-play blocked by browser:", e);
                  // Show one-time prompt to enable audio
                  setAudioPermissionNeeded(true);
                });
            }
          }, 200);
        } else {
          console.error("Audio player ref is null");
        }
      }
    }
  }, [messages]);

  // Fetch results when view changes to 'completed'
  useEffect(() => {
    const fetchResults = async () => {
      if (view !== 'completed' || !sessionId) return;

      setLoadingResults(true);
      try {
        const res = await fetch(`${API_BASE_URL}/interview/results/${sessionId}`);
        if (res.ok) {
          const data = await res.json();
          setResults(data);
        }
      } catch (err) {
        console.error("Failed to fetch results:", err);
      } finally {
        setLoadingResults(false);
      }
    };

    fetchResults();
  }, [view, sessionId]);

  // Handle user enabling audio after browser block
  const enableAudio = () => {
    if (audioPlayerRef.current && audioPlayerRef.current.src) {
      audioPlayerRef.current.play().then(() => {
        setAudioPermissionNeeded(false);
      }).catch(e => {
        console.error("Failed to play audio:", e);
      });
    }
  };

  const handleStart = async () => {
    if (interviewType === 'video-practice') {
      setView('video-practice');
      return;
    }

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
          interview_type: interviewType,
          topic: topic
        })
      });

      if (!res.ok) throw new Error('Failed to start interview');

      const data = await res.json();
      setSessionId(data.session_id);
      // Include audio_url in message
      setMessages([{ role: 'ai', text: data.text, audio_url: data.audio_url }]);
      setView('chat');
    } catch (err) {
      alert('Error: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await handleSendAnswer(null, audioBlob);

        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
      alert("Could not access microphone.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleSendAnswer = async (manualText = null, audioBlob = null) => {
    if (isLoading) return;

    const textToSend = manualText || userInput.trim();
    if (!textToSend && !audioBlob) return;

    // Optimistic UI update for text
    if (textToSend) {
      setMessages(prev => [...prev, { role: 'user', text: textToSend }]);
      setUserInput('');
    } else if (audioBlob) {
      setMessages(prev => [...prev, { role: 'user', text: '🎤 [Audio Answer Sent]' }]);
    }

    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('session_id', sessionId);

      if (textToSend) formData.append('text_answer', textToSend);
      // PRIVACY NOTE: Audio blob is sent for transcription only and is NOT stored.
      // Backend processes it in-memory and deletes the temporary file immediately.
      if (audioBlob) formData.append('audio_file', audioBlob, 'answer.webm');

      const res = await fetch(`${API_BASE_URL}/interview/answer`, {
        method: 'POST',
        body: formData
      });

      if (!res.ok) throw new Error('Failed to process answer');

      const data = await res.json();

      // Handle Feedback (if available) - Assuming backend sends it in 'feedback' field, or just text
      // data.text usually contains the next question.
      // data.audio_url contains TTS.

      setMessages(prev => [...prev, {
        role: 'ai',
        text: data.text,
        audio_url: data.audio_url,
        feedback: data.feedback // Capture feedback if present
      }]);

      if (data.is_completed) {
        // Wait for audio to finish playing (approx 3 seconds)
        setTimeout(() => setView('completed'), 3000);
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', text: '❌ Error: ' + err.message }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Video Practice View
  if (view === 'video-practice') {
    return <VideoPractice onBack={() => setView('setup')} />;
  }

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
                  <div className="text-xs text-gray-600 mt-1">Theory, concepts, explanation-based</div>
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
                <button
                  type="button"
                  onClick={() => setInterviewType('video-practice')}
                  className={`p-4 border-2 rounded-lg transition-all col-span-2 sm:col-span-1 ${interviewType === 'video-practice'
                    ? 'border-green-500 bg-green-50 ring-2 ring-green-200'
                    : 'border-gray-300 hover:border-green-300'
                    }`}
                >
                  <div className="text-3xl mb-2">📹</div>
                  <div className="font-semibold text-gray-800">Video Presence</div>
                  <div className="text-xs text-gray-600 mt-1">Eye contact & body language practice</div>
                </button>
              </div>
            </div>

            {/* Topic Selection for Technical Interview */}
            {interviewType === 'technical' && (
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Select Practice Mode *
                </label>
                <select
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none bg-white"
                >
                  <option value="realtime">Real-Time Adaptive (Context-Aware)</option>
                  <option value="python">Python Practice</option>
                  <option value="java">Java Practice</option>
                  <option value="sql">SQL / Database Practice</option>
                  <option value="dotnet">.NET Core Practice</option>
                </select>
                <p className="text-xs text-gray-500 mt-2">
                  {topic === 'realtime'
                    ? '💡 Adaptive interview that builds questions from your answers. Starts with introduction.'
                    : '💡 Focused practice on specific topic. Starts directly with concepts, no introduction.'}
                </p>
              </div>
            )}



            {interviewType !== 'video-practice' && (
              <>
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
              </>
            )}

            <button
              onClick={handleStart}
              disabled={isLoading || (interviewType !== 'video-practice' && !resumeText.trim())}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold py-4 rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
            >
              {isLoading ? 'Starting Interview...' : 'Start Interview 🚀'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Completed View - Fetch and display comprehensive results
  if (view === 'completed') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-900 via-teal-900 to-blue-900 p-6 overflow-y-auto">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="bg-white rounded-2xl shadow-2xl p-8 mb-6 text-center">
            <div className="text-6xl mb-4">🎉</div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Interview Completed!</h1>
            <p className="text-gray-600">Great job! Here's your performance summary.</p>
          </div>

          {loadingResults ? (
            <div className="bg-white rounded-2xl shadow-2xl p-12 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Analyzing your performance...</p>
            </div>
          ) : results ? (
            <>
              {/* Overall Score */}
              <div className="bg-white rounded-2xl shadow-2xl p-8 mb-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Overall Performance</h2>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-5xl font-bold text-blue-600">{results.overall_score}</p>
                    <p className="text-gray-600 mt-2">{results.performance_rating}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-gray-600">Questions Answered</p>
                    <p className="text-2xl font-semibold text-gray-800">{results.questions_answered}</p>
                  </div>
                </div>
              </div>

              {/* Strengths */}
              {results.strengths && results.strengths.length > 0 && (
                <div className="bg-white rounded-2xl shadow-2xl p-8 mb-6">
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">💪 Strengths</h2>
                  <ul className="space-y-2">
                    {results.strengths.map((strength, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-green-500 mt-1">✓</span>
                        <span className="text-gray-700">{strength}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Recommendations */}
              {results.recommendations && results.recommendations.length > 0 && (
                <div className="bg-white rounded-2xl shadow-2xl p-8 mb-6">
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">💡 Recommendations</h2>
                  <ul className="space-y-2">
                    {results.recommendations.map((rec, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-blue-500 mt-1">→</span>
                        <span className="text-gray-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Model Answers - Learning Opportunities */}
              {results.model_answers && results.model_answers.length > 0 && (
                <div className="bg-white rounded-2xl shadow-2xl p-8 mb-6">
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">📝 Learning Opportunities</h2>
                  <p className="text-gray-600 mb-6">
                    Here are ideal answers for questions where you can improve. Use these as learning references.
                  </p>

                  <div className="space-y-6">
                    {results.model_answers.map((item, idx) => (
                      <div key={idx} className="border-l-4 border-yellow-400 pl-4 py-2">
                        <p className="font-semibold text-gray-800 mb-2">
                          Question: {item.question}
                        </p>
                        <p className="text-sm text-gray-600 mb-1">
                          Your Score: <span className="font-semibold text-red-600">{item.your_score}/100</span>
                        </p>

                        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mt-3">
                          <p className="text-sm font-semibold text-green-800 mb-2">
                            💡 How you could answer this better in an interview:
                          </p>
                          <p className="text-gray-700 leading-relaxed">{item.model_answer}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Button */}
              <div className="text-center">
                <button
                  onClick={() => {
                    setView('setup');
                    setMessages([]);
                    setSessionId(null);
                    setResumeText('');
                    setJdText('');
                    setResults(null);
                  }}
                  className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 font-semibold shadow-lg"
                >
                  Start New Interview
                </button>
              </div>
            </>
          ) : (
            <div className="bg-white rounded-2xl shadow-2xl p-12 text-center">
              <p className="text-gray-600 mb-4">Unable to load results</p>
              <button
                onClick={() => {
                  setView('setup');
                  setMessages([]);
                  setSessionId(null);
                }}
                className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 font-semibold"
              >
                Start New Interview
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Chat View
  return (
    <div className="h-screen bg-gray-100 flex flex-col">
      {/* Hidden Audio Player */}
      <audio ref={audioPlayerRef} className="hidden" controls />

      {/* Audio Permission Prompt - appears when auto-play is blocked */}
      {audioPermissionNeeded && (
        <div className="bg-yellow-50 border-b-2 border-yellow-400 p-3 shadow-md">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-2xl">🔊</span>
              <p className="text-sm text-gray-800">
                <strong>Enable Audio:</strong> Tap the button to hear the AI interviewer's voice
              </p>
            </div>
            <button
              onClick={enableAudio}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-semibold text-sm transition-all shadow-md"
            >
              Enable Audio
            </button>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 shadow-lg">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">AI Interview Session</h1>
            <p className="text-sm text-blue-100">Powered by Gemini AI & Whisper</p>
          </div>
          <button
            onClick={() => {
              if (confirm('Are you sure you want to end the interview?')) {
                // Show results instead of just resetting
                setView('completed');
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
                  <div>
                    <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
                    {/* Display Audio Indicator if message has audio */}
                    {msg.audio_url && (
                      <button
                        onClick={() => {
                          if (audioPlayerRef.current) {
                            if (msg.audio_url.startsWith('data:') || msg.audio_url.startsWith('http')) {
                              audioPlayerRef.current.src = msg.audio_url;
                            } else {
                              audioPlayerRef.current.src = `${API_BASE_URL}${msg.audio_url}`;
                            }
                            audioPlayerRef.current.play();
                          }
                        }}
                        className="mt-2 text-xs flex items-center gap-1 text-blue-500 hover:text-blue-700"
                      >
                        🔊 Replay Audio
                      </button>
                    )}
                    {/* Display Feedback if present */}
                    {msg.feedback && msg.feedback.score !== undefined && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <div className="flex items-center gap-2 mb-1">
                          <span className={`text-xs font-bold px-2 py-1 rounded ${msg.feedback.score >= 80 ? 'bg-green-100 text-green-700' :
                            msg.feedback.score >= 60 ? 'bg-yellow-100 text-yellow-700' :
                              'bg-red-100 text-red-700'
                            }`}>
                            Score: {msg.feedback.score}/100
                          </span>
                          <span className="text-xs text-gray-500">{msg.feedback.quality}</span>
                        </div>
                        <p className="text-sm text-gray-600 italic">{msg.feedback.feedback_text}</p>
                      </div>
                    )}
                  </div>
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
        <div className="max-w-4xl mx-auto flex gap-3 items-center">

          {/* Microphone Button */}
          <button
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isLoading}
            className={`p-4 rounded-full transition-all shadow-md ${isRecording
              ? 'bg-red-500 text-white animate-pulse ring-4 ring-red-200'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            title={isRecording ? "Stop Recording" : "Start Recording"}
          >
            {isRecording ? (
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="6" y="6" width="12" height="12" rx="2" ry="2"></rect></svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
            )}
          </button>

          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendAnswer()}
            placeholder={isRecording ? "Listening..." : "Type your answer here..."}
            disabled={isLoading || isRecording}
            className="flex-1 px-6 py-3 border-2 border-gray-300 rounded-full focus:border-blue-500 focus:outline-none disabled:bg-gray-100 transition-all"
          />

          <button
            onClick={() => handleSendAnswer()}
            disabled={isLoading || (!userInput.trim() && !isRecording)} // Disable if empty stats
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