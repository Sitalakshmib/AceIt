import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { API_BASE_URL } from '../services/api';
import VideoPractice from '../components/Interview/VideoPractice';
const aiAvatar = "/ai-avatar.png"; // Use public asset directly
import {
  Users, Briefcase, Video, Mic, MessageSquare, Rocket, Target,
  Cpu, BookOpen, Clock, Activity, Award, ArrowRight, Zap, Play, Square,
  CheckCircle2, AlertCircle, X, Volume2, MicOff, Camera, BarChart2, ArrowLeft
} from 'lucide-react';
import InterviewAnalytics from '../components/Interview/InterviewAnalytics';

// Motivational quotes for timeout modal
const MOTIVATIONAL_QUOTES = [
  "Every expert was once a beginner. Keep practicing!",
  "Success is the sum of small efforts repeated day in and day out.",
  "The only way to do great work is to love what you do.",
  "Believe you can and you're halfway there.",
  "Your limitation—it's only your imagination.",
  "Push yourself, because no one else is going to do it for you.",
  "Great things never come from comfort zones.",
  "Dream it. Wish it. Do it.",
  "Success doesn't just find you. You have to go out and get it.",
  "The harder you work for something, the greater you'll feel when you achieve it.",
  "Don't stop when you're tired. Stop when you're done.",
  "Wake up with determination. Go to bed with satisfaction.",
  "Do something today that your future self will thank you for.",
  "Little things make big days.",
  "It's going to be hard, but hard does not mean impossible.",
  "Don't wait for opportunity. Create it.",
  "Sometimes we're tested not to show our weaknesses, but to discover our strengths.",
  "The key to success is to focus on goals, not obstacles.",
  "Dream bigger. Do bigger.",
  "Don't be afraid to fail. Be afraid not to try."
];

const Interview = () => {
  const navigate = useNavigate();
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

  // Visual Panel State (New)
  const [isAiSpeaking, setIsAiSpeaking] = useState(false);
  const videoRef = useRef(null);
  const [cameraError, setCameraError] = useState(false);

  // Timer State (New)
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes in seconds
  const [showEndConfirmation, setShowEndConfirmation] = useState(false);
  const [showTimeoutModal, setShowTimeoutModal] = useState(false);
  const [timeoutQuote, setTimeoutQuote] = useState('');

  // Results State (must be at top level, not inside conditional)
  const [results, setResults] = useState(null);
  const [loadingResults, setLoadingResults] = useState(true);

  // Timer Logic
  useEffect(() => {
    let timerId;
    if (view === 'chat' && timeLeft > 0) {
      timerId = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            clearInterval(timerId);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else if (view === 'chat' && timeLeft === 0 && !showTimeoutModal) {
      // Time's up! Show custom modal with motivational quote
      const randomQuote = MOTIVATIONAL_QUOTES[Math.floor(Math.random() * MOTIVATIONAL_QUOTES.length)];
      setTimeoutQuote(randomQuote);
      setShowTimeoutModal(true);

      // Play audio announcement
      playTimeoutAudio();
    }

    return () => clearInterval(timerId);
  }, [view, timeLeft, showTimeoutModal]);

  // Format time for display (MM:SS)
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Camera Logic for Visual Panel (Visual Only)
  useEffect(() => {
    if (view === 'chat' && (interviewType === 'technical' || interviewType === 'hr')) {
      let stream = null;
      const startCamera = async () => {
        try {
          stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            // Explicitly play to avoid black screen issues
            await videoRef.current.play().catch(e => console.error("Video auto-play failed:", e));
          }
          setCameraError(false);
        } catch (err) {
          console.error("Camera access denied for visual panel:", err);
          setCameraError(true);
        }
      };
      startCamera();

      return () => {
        if (stream) {
          stream.getTracks().forEach(track => track.stop());
        }
      };
    }
  }, [view, interviewType]);


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

  const playTimeoutAudio = () => {
    // Use browser's Speech Synthesis API for timeout announcement
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(
        "Time is up! Thank you for your dedication to practicing the interview."
      );
      utterance.rate = 0.9; // Slightly slower for clarity
      utterance.pitch = 1.0;
      utterance.volume = 1.0;
      window.speechSynthesis.speak(utterance);
    }
  };

  const handleStart = async () => {
    if (interviewType === 'video-practice') {
      setView('video-practice');
      return;
    }

    // Simplified start: No longer require manual summary/JD entry
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/interview/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user?.id || 'guest_user',
          resume_text: resumeText || 'Software Developer Candidate',
          jd_text: jdText || 'General Software Engineering Role',
          interview_type: interviewType,
          topic: topic
        })
      });

      if (!res.ok) throw new Error('Failed to start interview');

      const data = await res.json();
      setSessionId(data.session_id);
      // Include audio_url in message
      setMessages([{ role: 'ai', text: data.text, audio_url: data.audio_url }]);
      setTimeLeft(600); // 10 minutes
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
      setMessages(prev => [...prev, { role: 'user', text: '[Audio Answer Sent]' }]);
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
      setMessages(prev => [...prev, { role: 'ai', text: 'Error: ' + err.message }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Video Practice View
  if (view === 'video-practice') {
    return (
      <VideoPractice
        userId={user?.id || 'guest_user'}
        onBack={() => setView('setup')}
        onComplete={() => setView('completed')}
      />
    );
  }

  // Setup View
  if (view === 'setup') {
    return (
      <div className="min-h-screen bg-gray-50 p-6 md:p-12 relative">
        {/* Back to Dashboard Button */}
        <button
          onClick={() => navigate('/')}
          className="absolute top-8 left-8 flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 text-gray-600 font-bold rounded-xl hover:bg-gray-50 hover:text-indigo-600 transition-all shadow-sm group z-50"
        >
          <ArrowLeft className="h-5 w-5 group-hover:-translate-x-1 transition-transform" />
          Dashboard
        </button>

        <div className="max-w-7xl mx-auto animate-in fade-in duration-500">

          {/* Header Section */}
          <div className="mb-12 text-center">
            <div className="inline-block p-3 bg-indigo-50 rounded-2xl mb-4">
              <Users className="h-8 w-8 text-indigo-600" />
            </div>
            <h1 className="text-4xl font-black text-gray-900 mb-4 tracking-tight">Interview Mastery</h1>
            <p className="text-lg text-gray-500 max-w-2xl mx-auto">
              Simulate real-world interviews with AI-driven testing. Practice technical concepts, behavioral questions, and boost your confidence.
            </p>

            {/* Analytics Entry Button */}
            <div className="mt-6 flex justify-center">
              <button
                onClick={() => setView('analytics')}
                className="flex items-center gap-2 px-6 py-3 bg-white border border-gray-200 text-gray-700 font-semibold rounded-full hover:bg-gray-50 hover:border-gray-300 transition-all shadow-sm group"
              >
                <BarChart2 className="h-5 w-5 text-indigo-600 group-hover:scale-110 transition-transform" />
                View Performance Analytics
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">

            {/* Left Column: Interview Type Selection */}
            <div className="lg:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Technical Card */}
              <div
                onClick={() => setInterviewType('technical')}
                className={`group relative p-6 rounded-[2rem] border transition-all cursor-pointer overflow-hidden ${interviewType === 'technical'
                  ? 'bg-white border-blue-500 ring-2 ring-blue-100 shadow-xl'
                  : 'bg-white border-gray-100 hover:border-blue-200 hover:shadow-lg'
                  }`}
              >
                <div className="absolute top-0 right-0 w-32 h-32 bg-blue-100 rounded-bl-[4rem] opacity-50 transition-transform group-hover:scale-110" />
                <div className={`relative h-14 w-14 rounded-2xl flex items-center justify-center mb-4 transition-colors ${interviewType === 'technical' ? 'bg-blue-600 text-white' : 'bg-blue-50 text-blue-600 group-hover:bg-blue-600 group-hover:text-white'
                  }`}>
                  <Cpu className="h-7 w-7" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-1">Technical</h3>
                <p className="text-sm text-gray-500">Core concepts & theory</p>
                {interviewType === 'technical' && (
                  <div className="absolute top-4 right-4 text-blue-600">
                    <CheckCircle2 className="h-6 w-6" />
                  </div>
                )}
              </div>

              {/* HR Card */}
              <div
                onClick={() => setInterviewType('hr')}
                className={`group relative p-6 rounded-[2rem] border transition-all cursor-pointer overflow-hidden ${interviewType === 'hr'
                  ? 'bg-white border-purple-500 ring-2 ring-purple-100 shadow-xl'
                  : 'bg-white border-gray-100 hover:border-purple-200 hover:shadow-lg'
                  }`}
              >
                <div className="absolute top-0 right-0 w-32 h-32 bg-purple-100 rounded-bl-[4rem] opacity-50 transition-transform group-hover:scale-110" />
                <div className={`relative h-14 w-14 rounded-2xl flex items-center justify-center mb-4 transition-colors ${interviewType === 'hr' ? 'bg-purple-600 text-white' : 'bg-purple-50 text-purple-600 group-hover:bg-purple-600 group-hover:text-white'
                  }`}>
                  <Briefcase className="h-7 w-7" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-1">HR & Behavioral</h3>
                <p className="text-sm text-gray-500">Soft skills & culture fit</p>
                {interviewType === 'hr' && (
                  <div className="absolute top-4 right-4 text-purple-600">
                    <CheckCircle2 className="h-6 w-6" />
                  </div>
                )}
              </div>

              {/* Video Presence Card */}
              <div
                onClick={() => setInterviewType('video-practice')}
                className={`group relative p-6 rounded-[2rem] border transition-all cursor-pointer overflow-hidden ${interviewType === 'video-practice'
                  ? 'bg-white border-green-500 ring-2 ring-green-100 shadow-xl'
                  : 'bg-white border-gray-100 hover:border-green-200 hover:shadow-lg'
                  }`}
              >
                <div className="absolute top-0 right-0 w-32 h-32 bg-green-100 rounded-bl-[4rem] opacity-50 transition-transform group-hover:scale-110" />
                <div className={`relative h-14 w-14 rounded-2xl flex items-center justify-center mb-4 transition-colors ${interviewType === 'video-practice' ? 'bg-green-600 text-white' : 'bg-green-50 text-green-600 group-hover:bg-green-600 group-hover:text-white'
                  }`}>
                  <Video className="h-7 w-7" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-1">Video Presence</h3>
                <p className="text-sm text-gray-500">Body language & eye contact</p>
                {interviewType === 'video-practice' && (
                  <div className="absolute top-4 right-4 text-green-600">
                    <CheckCircle2 className="h-6 w-6" />
                  </div>
                )}
              </div>
            </div>

            {/* Configuration Panel (Technical) */}
            {interviewType === 'technical' && (
              <div className="lg:col-span-3 bg-white rounded-[2.5rem] shadow-xl shadow-gray-100 border border-gray-100 p-8 md:p-10 animate-in slide-in-from-bottom-4 duration-500">
                <div className="max-w-2xl mx-auto space-y-8">
                  <div className="text-center">
                    <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center justify-center">
                      <Target className="h-5 w-5 mr-2 text-indigo-500" />
                      Practice Mode Selection
                    </h3>

                    <div className="relative">
                      <select
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                        className="w-full p-4 pl-4 pr-10 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none appearance-none font-medium text-gray-700 text-center"
                      >
                        <option value="realtime">Real-Time Adaptive (Context-Aware)</option>
                        <option value="python">Python Practice</option>
                        <option value="java">Java Practice</option>
                        <option value="sql">SQL / Database Practice</option>
                        <option value="dotnet">.NET Core Practice</option>
                      </select>
                      <div className="absolute right-4 top-1/2 transform -translate-y-1/2 pointer-events-none text-gray-400">
                        <ArrowRight className="h-4 w-4 rotate-90" />
                      </div>
                    </div>
                    <p className="text-xs text-center text-gray-500 mt-3">
                      {topic === 'realtime'
                        ? 'Starts with general questions and adapts based on your performance.'
                        : `Focused session targeting ${topic} concepts and logic.`}
                    </p>
                  </div>

                  <div className="pt-4 flex justify-center">
                    <button
                      onClick={handleStart}
                      disabled={isLoading}
                      className="flex items-center bg-indigo-600 text-white px-10 py-4 rounded-xl font-bold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-indigo-200 hover:shadow-indigo-300 transform hover:-translate-y-1"
                    >
                      {isLoading ? "Starting Session..." : "Start Technical Interview"}
                      <Rocket className="ml-2 h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Start Button for HR/Behavioral Mode */}
            {interviewType === 'hr' && (
              <div className="lg:col-span-3 flex justify-center mt-8 animate-in slide-in-from-bottom-4 duration-500">
                <button
                  onClick={handleStart}
                  disabled={isLoading}
                  className="flex items-center bg-purple-600 text-white px-12 py-5 rounded-2xl font-bold hover:bg-purple-700 disabled:opacity-50 transition-all shadow-lg shadow-purple-200 hover:shadow-purple-300 transform hover:-translate-y-1 text-lg"
                >
                  {isLoading ? "Starting Session..." : "Start Behavioral Interview"}
                  <Briefcase className="ml-3 h-6 w-6" />
                </button>
              </div>
            )}
            {/* Start Button for Video Presence Mode */}
            {interviewType === 'video-practice' && (
              <div className="lg:col-span-3 flex justify-center mt-4">
                <button
                  onClick={handleStart}
                  className="flex items-center bg-green-600 text-white px-10 py-4 rounded-xl font-bold hover:bg-green-700 transition-all shadow-lg shadow-green-200 hover:shadow-green-300 transform hover:-translate-y-1"
                >
                  Launch Video Practice Studio
                  <Video className="ml-2 h-5 w-5" />
                </button>
              </div>
            )}

          </div>
        </div>
      </div>
    );
  }

  // Completed View - Fetch and display comprehensive results
  if (view === 'completed') {
    return (
      <div className="min-h-screen bg-gray-50 p-6 md:p-12 overflow-y-auto">
        <div className="max-w-5xl mx-auto">
          {/* Header */}
          <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-8 mb-8 text-center animate-in slide-in-from-bottom-4 duration-500">
            <div className="inline-block p-4 bg-green-50 rounded-full mb-4">
              <Award className="h-10 w-10 text-green-600" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Interview Completed!</h1>
            <p className="text-gray-500">Here's a comprehensive breakdown of your performance.</p>
          </div>

          {loadingResults ? (
            <div className="bg-white rounded-[2rem] shadow-xl p-20 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-500 font-medium">Analyzing interview metrics...</p>
            </div>
          ) : results ? (
            <div className="space-y-8 animate-in slide-in-from-bottom-8 duration-700">

              {/* Overall Score Card */}
              <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-8 grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
                <div className="md:col-span-1 text-center border-r border-gray-100">
                  <p className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Overall Score</p>
                  <div className="flex justify-center items-baseline">
                    <span className="text-6xl font-black text-indigo-600">{results.overall_score}</span>
                    <span className="text-gray-400 ml-2 font-medium">/100</span>
                  </div>
                  <div className={`inline-block mt-3 px-4 py-1 rounded-full text-sm font-bold ${results.performance_rating === 'Excellent' ? 'bg-green-100 text-green-700' :
                    results.performance_rating === 'Good' ? 'bg-blue-100 text-blue-700' :
                      'bg-yellow-100 text-yellow-700'
                    }`}>
                    {results.performance_rating}
                  </div>
                </div>

                <div className="md:col-span-2 grid grid-cols-2 gap-6">
                  <div className="bg-gray-50 rounded-2xl p-5">
                    <div className="flex items-center mb-2">
                      <MessageSquare className="h-5 w-5 text-blue-500 mr-2" />
                      <span className="text-sm font-semibold text-gray-600">Questions</span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{results.questions_answered}</p>
                  </div>
                  <div className="bg-gray-50 rounded-2xl p-5">
                    <div className="flex items-center mb-2">
                      <Target className="h-5 w-5 text-purple-500 mr-2" />
                      <span className="text-sm font-semibold text-gray-600">Focus Area</span>
                    </div>
                    <p className="text-lg font-bold text-gray-900 truncate capitalize">{results.topic || interviewType}</p>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Strengths */}
                {results.strengths && results.strengths.length > 0 && (
                  <div className="bg-white rounded-[2rem] shadow-lg p-8 border border-gray-100">
                    <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                      <CheckCircle2 className="h-6 w-6 text-green-500 mr-2" />
                      Key Strengths
                    </h2>
                    <ul className="space-y-4">
                      {results.strengths.map((strength, idx) => (
                        <li key={idx} className="flex items-start bg-green-50 rounded-xl p-4">
                          <div className="mt-1 mr-3 h-2 w-2 rounded-full bg-green-500"></div>
                          <span className="text-gray-700 font-medium">{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Recommendations */}
                {results.recommendations && results.recommendations.length > 0 && (
                  <div className="bg-white rounded-[2rem] shadow-lg p-8 border border-gray-100">
                    <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                      <Target className="h-6 w-6 text-orange-500 mr-2" />
                      Focus Areas
                    </h2>
                    <ul className="space-y-4">
                      {results.recommendations.map((rec, idx) => (
                        <li key={idx} className="flex items-start bg-orange-50 rounded-xl p-4">
                          <div className="mt-1 mr-3 h-2 w-2 rounded-full bg-orange-500"></div>
                          <span className="text-gray-700 font-medium">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Model Answers - Learning Opportunities */}
              {results.model_answers && results.model_answers.length > 0 && (
                <div className="bg-white rounded-[2rem] shadow-lg p-8 border border-gray-100">
                  <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                    <BookOpen className="h-6 w-6 text-blue-500 mr-2" />
                    Learning Opportunities
                  </h2>
                  <p className="text-gray-500 mb-6 ml-1">Review your answers against model responses to improve.</p>

                  <div className="space-y-6">
                    {results.model_answers.map((item, idx) => (
                      <div key={idx} className="bg-gray-50 rounded-2xl p-6 border border-gray-100">
                        <div className="flex justify-between items-start mb-4">
                          <p className="font-bold text-gray-800 text-lg w-3/4">"{item.question}"</p>
                          <span className="bg-red-100 text-red-700 text-xs font-bold px-3 py-1 rounded-full">
                            Score: {item.your_score}
                          </span>
                        </div>

                        <div className="mb-4 pl-4 border-l-2 border-red-300">
                          <p className="text-xs font-bold text-gray-400 uppercase mb-1">Your Answer</p>
                          <p className="text-gray-600 italic">"{item.your_answer || 'No answer provided'}"</p>
                        </div>

                        <div className="bg-white rounded-xl p-4 border border-green-100 relative overflow-hidden">
                          <div className="absolute top-0 left-0 w-1 h-full bg-green-400"></div>
                          <p className="text-xs font-bold text-green-600 uppercase mb-2 flex items-center">
                            <CheckCircle2 className="h-3 w-3 mr-1" /> Ideal Response
                          </p>
                          <p className="text-gray-800 leading-relaxed font-medium">{item.model_answer}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex justify-center gap-4 pb-8">
                <button
                  onClick={() => setView('setup')}
                  className="bg-gray-100 text-gray-700 px-8 py-4 rounded-xl hover:bg-gray-200 font-bold shadow-lg transition-all flex items-center"
                >
                  <ArrowRight className="h-5 w-5 mr-2 rotate-180" />
                  Back to Selection
                </button>
                <button
                  onClick={() => {
                    setView('setup');
                    setMessages([]);
                    setSessionId(null);
                    setResumeText('');
                    setJdText('');
                    setResults(null);
                  }}
                  className="bg-gray-900 text-white px-10 py-4 rounded-xl hover:bg-black font-bold shadow-lg transition-transform hover:-translate-y-1 flex items-center"
                >
                  <Zap className="h-5 w-5 mr-2" />
                  Start New Session
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-[2rem] shadow-xl p-12 text-center">
              <AlertCircle className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-600 mb-6">Unable to load results</p>
              <button
                onClick={() => {
                  setView('setup');
                  setMessages([]);
                  setSessionId(null);
                }}
                className="bg-indigo-600 text-white px-8 py-3 rounded-lg hover:bg-indigo-700 font-semibold"
              >
                Start New Interview
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Analytics View
  if (view === 'analytics') {
    return (
      <InterviewAnalytics
        userId={user?.id || 'demo_user'}
        onBack={() => setView('setup')}
        onStartPractice={(type) => {
          setInterviewType(type);
          setView('setup');
        }}
      />
    );
  }

  return (
    <div className="h-screen bg-gray-50 flex flex-col font-sans">
      {/* Hidden Audio Player for Logic - Updated to toggle isAiSpeaking */}
      <audio
        ref={audioPlayerRef}
        className="hidden"
        onPlay={() => setIsAiSpeaking(true)}
        onPause={() => setIsAiSpeaking(false)}
        onEnded={() => setIsAiSpeaking(false)}
        controls
      />

      {/* Audio Permission Prompt */}
      {audioPermissionNeeded && (
        <div className="bg-amber-50 border-b border-amber-200 p-4 sticky top-0 z-[60]">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Volume2 className="h-5 w-5 text-amber-600" />
              <p className="text-sm font-medium text-amber-800">
                Audio auto-play blocked. Enable audio to hear the interviewer.
              </p>
            </div>
            <button
              onClick={enableAudio}
              className="bg-amber-600 text-white px-4 py-1.5 rounded-lg hover:bg-amber-700 font-semibold text-sm transition-all"
            >
              Enable Audio
            </button>
          </div>
        </div>
      )}

      {/* Sticky Header with Timer */}
      <div className="bg-white border-b border-gray-200 py-4 px-6 shadow-sm z-50 sticky top-0">
        <div className="max-w-5xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg ${interviewType === 'technical' ? 'bg-blue-100 text-blue-600' : 'bg-purple-100 text-purple-600'}`}>
              {interviewType === 'technical' ? <Cpu className="h-5 w-5" /> : <Briefcase className="h-5 w-5" />}
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-800 leading-tight">AI Interview Session</h1>
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500 font-medium bg-gray-100 px-2 py-0.5 rounded-full capitalize">{interviewType}</span>
                <span className="text-xs text-gray-400">•</span>
                <span className="text-xs text-gray-500">Gemini Powered</span>
              </div>
            </div>
          </div>

          {/* Timer & Controls */}
          <div className="flex items-center gap-4">
            {/* Timer Display */}
            <div className={`flex items-center gap-2 px-4 py-2 rounded-lg font-mono font-bold ${timeLeft < 60 ? 'bg-red-50 text-red-600 animate-pulse' : 'bg-gray-100 text-gray-700'
              }`}>
              <Clock className="h-4 w-4" />
              <span>{formatTime(timeLeft)}</span>
            </div>

            <button
              onClick={() => setShowEndConfirmation(true)}
              className="text-gray-500 hover:text-red-500 hover:bg-red-50 px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
            >
              End Session
            </button>
          </div>
        </div>
      </div>

      {/* End Session Confirmation Modal */}
      {
        showEndConfirmation && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6 transform scale-100 animate-in zoom-in-95 duration-200">
              <div className="flex flex-col items-center text-center">
                <div className="h-12 w-12 bg-red-100 rounded-full flex items-center justify-center mb-4">
                  <AlertCircle className="h-6 w-6 text-red-600" />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">End Interview?</h3>
                <p className="text-gray-500 text-sm mb-6">
                  Are you sure you want to end the session? You will see your results immediately.
                </p>
                <div className="flex gap-3 w-full">
                  <button
                    onClick={() => setShowEndConfirmation(false)}
                    className="flex-1 px-4 py-2.5 bg-gray-100 text-gray-700 font-semibold rounded-xl hover:bg-gray-200 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => {
                      setShowEndConfirmation(false);
                      setView('completed');
                    }}
                    className="flex-1 px-4 py-2.5 bg-red-600 text-white font-semibold rounded-xl hover:bg-red-700 transition-colors shadow-lg shadow-red-200"
                  >
                    End Session
                  </button>
                </div>
              </div>
            </div>
          </div>
        )
      }

      {/* Timeout Modal */}
      {showTimeoutModal && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in duration-300">
          <div className="bg-gradient-to-br from-white to-gray-50 rounded-3xl shadow-2xl max-w-md w-full p-8 transform scale-100 animate-in zoom-in-95 duration-300 border border-gray-100">
            <div className="flex flex-col items-center text-center">
              {/* Icon */}
              <div className="h-20 w-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mb-6 shadow-lg shadow-blue-200 animate-pulse">
                <Clock className="h-10 w-10 text-white" />
              </div>

              {/* Title */}
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Time's Up!</h3>

              {/* Message */}
              <p className="text-gray-600 mb-6">
                Thank you for your dedication to practicing the interview.
              </p>

              {/* Motivational Quote */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 mb-6 border border-blue-100 relative overflow-hidden">
                <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-blue-500 to-indigo-600"></div>
                <div className="flex items-start gap-3">
                  <Zap className="h-5 w-5 text-indigo-600 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-700 font-medium italic leading-relaxed">
                    "{timeoutQuote}"
                  </p>
                </div>
              </div>

              {/* Action Button */}
              <button
                onClick={() => {
                  setShowTimeoutModal(false);
                  setView('completed');
                }}
                className="w-full px-6 py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-0.5"
              >
                View Results
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Visual Interview Panel (Centered & Compact) */}
      <div className="bg-gray-50 pt-6 px-4 pb-2 shrink-0">
        <div className="max-w-4xl mx-auto h-[30vh] flex gap-4">

          {/* Left: AI Interviewer */}
          <div className="flex-1 bg-[#DEF1FC] rounded-2xl border border-blue-100 flex items-center justify-center relative overflow-hidden shadow-lg">
            <div className="text-center w-full h-full flex items-center justify-center">
              <div className={`relative inline-block ${isAiSpeaking ? 'scale-105' : 'scale-100'} transition-transform duration-300`}>
                {/* Pulsing Glow when Speaking */}
                {isAiSpeaking && (
                  <div className="absolute inset-0 bg-blue-400 rounded-full blur-xl opacity-40 animate-pulse"></div>
                )}

                <div className="h-40 w-40 flex items-center justify-center relative z-10">
                  <img
                    src={aiAvatar}
                    alt="AI Interviewer"
                    className="w-full h-full object-cover rounded-full"
                    onError={(e) => {
                      // Fallback to icon if image fails to load
                      e.target.style.display = 'none';
                      e.target.nextElementSibling.style.display = 'flex';
                    }}
                  />
                  <div className="hidden w-full h-full bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full items-center justify-center">
                    <Users className="h-20 w-20 text-white" />
                  </div>
                </div>
              </div>

              <div className="absolute bottom-4 left-0 right-0 flex flex-col items-center">
                {isAiSpeaking && (
                  <div className="flex items-center gap-1 bg-white/40 backdrop-blur-sm px-3 py-1 rounded-full border border-white/20">
                    <div className="w-1 h-3 bg-blue-600 rounded-full animate-pulse"></div>
                    <div className="w-1 h-4 bg-blue-600 rounded-full animate-pulse delay-75"></div>
                    <div className="w-1 h-3 bg-blue-600 rounded-full animate-pulse delay-150"></div>
                    <span className="text-[10px] text-blue-800 ml-1 font-bold">Speaking</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right: Student Camera Preview (Visual Only) */}
          <div className="flex-1 bg-black rounded-2xl border border-gray-800 relative overflow-hidden shadow-lg flex items-center justify-center">
            {cameraError ? (
              <div className="flex flex-col items-center text-gray-500">
                <MicOff className="h-6 w-6 mb-2 opacity-50" />
                <span className="text-xs">No Camera</span>
              </div>
            ) : (
              <video
                ref={videoRef}
                autoPlay
                muted
                playsInline
                className="h-full w-full object-cover"
              />
            )}

            {/* Overlay Badge */}
            <div className="absolute bottom-3 right-3 bg-black/50 backdrop-blur-md px-2 py-0.5 rounded-full flex items-center border border-white/10">
              <div className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1.5 animate-pulse"></div>
              <span className="text-[10px] text-white font-medium">You</span>
            </div>
          </div>

        </div>
      </div>

      {/* Messages (Remaining Height) */}
      <div className="flex-1 overflow-y-auto p-6 scroll-smooth bg-gray-50">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex max-w-[85%] items-end gap-2 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>

                {/* Avatar */}
                <div className={`h-8 w-8 rounded-full flex items-center justify-center flex-shrink-0 ${msg.role === 'user' ? 'bg-gray-900 text-white' : 'bg-indigo-600 text-white'
                  }`}>
                  {msg.role === 'user' ? <Users className="h-4 w-4" /> : <MicrochipIcon className="h-4 w-4" />}
                </div>

                {/* Message Bubble */}
                <div
                  className={`px-6 py-4 rounded-2xl shadow-sm text-sm leading-relaxed ${msg.role === 'user'
                    ? 'bg-gray-900 text-white rounded-br-none'
                    : 'bg-white text-gray-800 border border-gray-100 rounded-bl-none'
                    }`}
                >
                  <p className="whitespace-pre-wrap">{msg.text}</p>

                  {/* Audio Controls */}
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
                      className="mt-3 flex items-center gap-2 text-xs font-bold text-indigo-500 hover:text-indigo-700 bg-indigo-50 px-3 py-1.5 rounded-full w-fit transition-colors"
                    >
                      <Play className="h-3 w-3 fill-current" /> Replay Audio
                    </button>
                  )}

                  {/* Feedback Section */}
                  {msg.feedback && msg.feedback.score !== undefined && (
                    <div className="mt-4 pt-3 border-t border-gray-100">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs text-gray-400 font-medium uppercase tracking-wider">Analysis</span>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded ${msg.feedback.score >= 80 ? 'bg-green-100 text-green-700' :
                          msg.feedback.score >= 60 ? 'bg-yellow-100 text-yellow-700' :
                            'bg-red-100 text-red-700'
                          }`}>
                          Score: {msg.feedback.score}/100
                        </span>
                      </div>
                      <p className="text-gray-600 italic border-l-2 border-gray-200 pl-3">
                        "{msg.feedback.feedback_text}"
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="flex items-end gap-2">
                <div className="h-8 w-8 rounded-full bg-indigo-600 text-white flex items-center justify-center flex-shrink-0">
                  <MicrochipIcon className="h-4 w-4" />
                </div>
                <div className="bg-white px-5 py-3 rounded-2xl rounded-bl-none shadow-sm border border-gray-100">
                  <div className="flex gap-1.5">
                    <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={(el) => el && el.scrollIntoView({ behavior: 'smooth' })}></div>
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white p-4 border-t border-gray-200">
        <div className="max-w-3xl mx-auto flex gap-3 items-center">

          {/* Microphone Button */}
          <button
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isLoading}
            className={`p-4 rounded-full transition-all duration-300 shadow-sm ${isRecording
              ? 'bg-red-500 text-white animate-pulse ring-4 ring-red-100'
              : 'bg-gray-100 text-gray-500 hover:bg-indigo-50 hover:text-indigo-600'
              }`}
            title={isRecording ? "Stop Recording" : "Start Recording"}
          >
            {isRecording ? <Square className="h-5 w-5 fill-current" /> : <Mic className="h-5 w-5" />}
          </button>

          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendAnswer()}
            placeholder={isRecording ? "Listening..." : "Type your answer here..."}
            disabled={isLoading || isRecording}
            className="flex-1 px-6 py-4 bg-gray-50 border border-gray-200 rounded-full focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition-all placeholder:text-gray-400"
          />

          <button
            onClick={() => handleSendAnswer()}
            disabled={isLoading || (!userInput.trim() && !isRecording)}
            className="p-4 bg-gray-900 text-white rounded-full hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md transform active:scale-95"
          >
            <ArrowRight className="h-5 w-5" />
          </button>
        </div>
        <p className="text-center text-xs text-gray-400 mt-3">
          AI can make mistakes. Please verify important information.
        </p>
      </div>
    </div >
  );
};

// Helper Icon for AI Avatar
const MicrochipIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <rect width="18" height="18" x="3" y="3" rx="2" />
    <path d="M12 9v6" />
    <path d="M9 12h6" />
    <path d="M7 3v-1" />
    <path d="M11 3v-1" />
    <path d="M13 3v-1" />
    <path d="M17 3v-1" />
  </svg>
);

export default Interview;