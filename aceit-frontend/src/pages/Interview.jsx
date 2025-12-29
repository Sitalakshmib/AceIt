import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';

// --- COMPONENTS ---

const SetupMode = ({ onStart }) => {
  const [type, setType] = useState('hr');
  const [stack, setStack] = useState('python');

  return (
    <div className="max-w-2xl mx-auto p-10 text-center bg-white rounded-xl shadow-xl mt-10">
      <h1 className="text-4xl font-extrabold text-gray-800 mb-6 tracking-tight">AI Interview Practice 🤖</h1>
      <p className="text-gray-600 mb-8 text-lg">
        Master your interview skills with real-time AI feedback.
        <br /> We analyze your <strong>speech, confidence, and technical accuracy</strong>.
      </p>

      <div className="grid grid-cols-2 gap-6 mb-8 text-left">
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">Interview Type</label>
          <select
            className="w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-purple-500"
            value={type} onChange={(e) => setType(e.target.value)}
          >
            <option value="hr">HR / Behavioral</option>
            <option value="technical">Technical</option>
          </select>
        </div>
        {type === 'technical' && (
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">Tech Stack</label>
            <select
              className="w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-purple-500"
              value={stack} onChange={(e) => setStack(e.target.value)}
            >
              <option value="python">Python</option>
              <option value="react">React</option>
            </select>
          </div>
        )}
      </div>

      <button
        onClick={() => onStart(type, stack)}
        className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold py-4 px-12 rounded-full text-xl shadow-lg transition transform hover:scale-105"
      >
        Start Session 🎤
      </button>
    </div>
  );
};

const Recorder = ({ onRecordingComplete, isProcessing }) => {
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const videoRef = useRef(null);

  // Initial Camera Setup
  useEffect(() => {
    const startStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Camera Error:", err);
      }
    };
    startStream();
    // Cleanup not strictly simpler for MVP to keep stream open
  }, []);

  const startRecording = async () => {
    console.log("🟢 Starting Recording...");
    const stream = videoRef.current.srcObject;
    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorderRef.current = mediaRecorder;
    chunksRef.current = [];

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunksRef.current.push(e.data);
    };

    mediaRecorder.onstop = () => {
      console.log("🔴 specific onstop triggered");
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
      console.log("📦 Blob created:", blob.size, blob.type);
      onRecordingComplete(blob);
    };

    mediaRecorder.start();
    setRecording(true);
  };

  const stopRecording = () => {
    console.log("🛑 stopRecording called");
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      setRecording(false);
    } else {
      console.warn("⚠️ MediaRecorder not active or null");
    }
  };

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-full max-w-md aspect-video bg-black rounded-xl overflow-hidden shadow-lg mb-6 border-4 border-gray-100">
        <video ref={videoRef} autoPlay muted playsInline className="w-full h-full object-cover transform scale-x-[-1]" />
        {recording && (
          <div className="absolute top-4 right-4 bg-red-600 text-white text-xs font-bold px-3 py-1 rounded-full animate-pulse">
            REC ●
          </div>
        )}
      </div>

      <div className="flex gap-4">
        {!recording ? (
          <button
            onClick={startRecording}
            disabled={isProcessing}
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-full shadow-md transition-all flex items-center gap-2"
          >
            <span>🎙️</span> Start Answer
          </button>
        ) : (
          <button
            onClick={stopRecording}
            className="bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-8 rounded-full shadow-md transition-all animate-pulse"
          >
            ⏹ Stop & Submit
          </button>
        )}
      </div>
      {isProcessing && <p className="mt-4 text-purple-600 font-semibold animate-bounce">Analyzing Audio...</p>}
    </div>
  );
};

const ReportView = ({ report }) => {
  if (!report) return null;
  const { session_summary, metrics, detailed_feedback, recommendation } = report;

  return (
    <div className="max-w-4xl mx-auto p-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Interview Performance Report 📊</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-6 rounded-xl shadow text-center">
          <div className="text-sm text-gray-500 uppercase font-bold">Overall Score</div>
          <div className="text-4xl font-extrabold text-purple-600 mt-2">{session_summary.overall_score}</div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow text-center">
          <div className="text-sm text-gray-500 uppercase font-bold">Confidence</div>
          <div className="text-4xl font-bold text-blue-600 mt-2">{metrics.confidence}</div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow text-center">
          <div className="text-sm text-gray-500 uppercase font-bold">Technical</div>
          <div className="text-4xl font-bold text-indigo-600 mt-2">{metrics.technical_depth}</div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow text-center">
          <div className="text-sm text-gray-500 uppercase font-bold">Communication</div>
          <div className="text-4xl font-bold text-pink-600 mt-2">{metrics.communication}</div>
        </div>
      </div>

      {/* Recommendation Banner */}
      <div className={`p-6 rounded-xl mb-8 text-white font-bold text-lg text-center shadow-md ${session_summary.result === 'Pass' ? 'bg-gradient-to-r from-green-500 to-emerald-600' : 'bg-gradient-to-r from-orange-500 to-red-500'}`}>
        {recommendation}
      </div>

      {/* Feedback Lists */}
      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-xl shadow">
          <h3 className="text-xl font-bold text-green-700 mb-4 border-b pb-2">✅ Key Strengths</h3>
          <ul className="space-y-3">
            {detailed_feedback.strengths.map((s, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-green-500 mt-1">✔</span>
                <span className="text-gray-700">{s}</span>
              </li>
            ))}
            {detailed_feedback.strengths.length === 0 && <span className="text-gray-400 italic">No specific strengths detected.</span>}
          </ul>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <h3 className="text-xl font-bold text-orange-700 mb-4 border-b pb-2">💡 Areas for Improvement</h3>
          <ul className="space-y-3">
            {detailed_feedback.improvements.map((s, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-orange-500 mt-1">⚠</span>
                <span className="text-gray-700">{s}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};


// --- MAIN PAGE ---

const Interview = () => {
  const { user } = useAuth();
  const [view, setView] = useState('setup'); // setup, session, report
  const [sessionData, setSessionData] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [report, setReport] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState(null);

  const handleStart = async (type, stack) => {
    try {
      const res = await fetch('http://localhost:8001/interview/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user?.id || "demo_user",
          interview_type: type,
          tech_stack: stack
        })
      });
      const data = await res.json();
      setSessionData(data);
      setCurrentQuestion(data.current_question);
      setTranscript(null);
      setView('session');
    } catch (err) {
      console.error(err);
      alert("Failed to start session. Check backend!");
    }
  };

  const handleAudioSubmit = async (audioBlob) => {
    console.log("🚀 handleAudioSubmit triggered with blob:", audioBlob.size);
    setIsProcessing(true);
    setTranscript(null); // Clear previous
    try {
      // 1. Transcribe (STT)
      const formData = new FormData();
      // Important: Send 'file' field, name it 'blob.wav' (backend handles conversion)
      formData.append('file', audioBlob, 'answer.webm');

      console.log("📡 Sending to /stt/transcribe...");
      const sttRes = await fetch('http://localhost:8001/stt/transcribe', {
        method: 'POST',
        body: formData
      });

      if (!sttRes.ok) throw new Error("STT Failed");

      const { text } = await sttRes.json();
      console.log("📝 Transcript received:", text);

      setTranscript(text); // Store transcript immediately

      if (!text) {
        alert("Could not hear audio. Try again.");
        setIsProcessing(false);
        return;
      }

      // 2. Analyze
      console.log("🧠 Sending to /interview/analyze...");
      const analyzeRes = await fetch('http://localhost:8001/interview/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionData.session_id,
          question_id: currentQuestion.id,
          user_response_text: text,
          // Mock Video Metrics for MVP
          video_metrics: { face_visible_pct: 0.95, looking_away_pct: 0.05 },
          speech_metrics: { audio_duration_seconds: 10 } // Simplified for MVP
        })
      });

      if (!analyzeRes.ok) throw new Error("Analysis Failed");

      const data = await analyzeRes.json();
      console.log("📊 Analysis received:", data);

      setFeedback({
        text: data.feedback,
        score: data.score,
        user_response_text: text
      });

      // Check if report available (session done)
      if (data.report) {
        setReport(data.report);
        // We still show feedback for last question, then transitioning button changes to "View Report"
      }

      if (data.is_completed && !data.report) {
        // Fallback if no report present but completed
        alert("Session Done.");
      }

      // Prepare next
      if (data.current_question) {
        window.nextQ = data.current_question;
      } else {
        window.nextQ = null;
      }

    } catch (err) {
      console.error(err);
      alert("Error processing answer: " + err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleNext = () => {
    setTranscript(null); // Reset transcript
    if (report) {
      setView('report');
    } else {
      setFeedback(null);
      setCurrentQuestion(window.nextQ);
    }
  };

  // --- RENDER SWITCH ---

  if (view === 'setup') return <SetupMode onStart={handleStart} />;

  if (view === 'report') return <ReportView report={report} />;

  return (
    <div className="max-w-6xl mx-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-8 h-[calc(100vh-100px)]">
      {/* Left Panel: Question */}
      <div className="flex flex-col justify-center">
        <div className="bg-white p-10 rounded-2xl shadow-xl border-l-8 border-purple-600">
          <span className="text-purple-600 font-bold tracking-widest uppercase text-sm">Current Question</span>
          <h2 className="text-3xl font-bold text-gray-800 mt-4 leading-snug">
            {currentQuestion?.text}
          </h2>
          {currentQuestion?.ai_context && (
            <div className="mt-4 p-3 bg-blue-50 text-blue-800 text-sm rounded-lg flex items-center gap-2">
              <span>💡</span> {currentQuestion.ai_context}
            </div>
          )}
        </div>

        {/* Transcript Section */}
        {transcript && (
          <div className="mt-6 p-5 bg-indigo-50 border-l-4 border-indigo-500 rounded-r-xl shadow-sm animate-fade-in">
            <h3 className="text-xs font-bold text-indigo-500 uppercase mb-2 tracking-wider">📝 What the AI heard from you</h3>
            <p className="text-gray-800 text-lg font-medium leading-relaxed">"{transcript}"</p>
          </div>
        )}

        {/* Feedback Modal (Overlay or Inline) */}
        {feedback && (
          <div className="mt-8 bg-gray-900 text-white p-6 rounded-xl shadow-2xl animate-fade-in relative overflow-hidden">
            <div className="absolute top-0 left-0 w-2 h-full bg-green-500"></div>
            <h3 className="font-bold text-xl mb-2 flex justify-between">
              <span>AI Feedback</span>
              <span className="bg-green-600 text-xs px-2 py-1 rounded-full">Score: {feedback.score}</span>
            </h3>
            {/* Removed the small italic text since we have the main transcript block now */}
            <p className="font-semibold text-lg mt-2">{feedback.text}</p>

            <button
              onClick={handleNext}
              className="w-full mt-6 bg-white text-gray-900 font-bold py-3 rounded-lg hover:bg-gray-100 transition"
            >
              {report ? "View Final Report 📊" : "Next Question ➔"}
            </button>
          </div>
        )}
      </div>

      {/* Right Panel: Recorder or Feedback */}
      <div className="bg-white rounded-2xl shadow-xl p-6 flex flex-col items-center justify-center relative overflow-hidden">
        {!feedback ? (
          <Recorder onRecordingComplete={handleAudioSubmit} isProcessing={isProcessing} />
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center animate-fade-in p-4">
            <div className="text-6xl mb-4">✅</div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">Answer Analyzed!</h3>
            <div className="bg-purple-50 p-4 rounded-xl w-full mb-6 border border-purple-100">
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold text-purple-700">Confidence Score</span>
                <span className="bg-purple-600 text-white px-3 py-1 rounded-full text-sm font-bold">{feedback.score}/100</span>
              </div>
              <p className="text-gray-700 italic">"{feedback.text}"</p>
            </div>

            <button
              onClick={handleNext}
              className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 px-10 rounded-full shadow-lg transition transform hover:scale-105"
            >
              {report ? "View Final Report 📊" : "Next Question ➔"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Interview;