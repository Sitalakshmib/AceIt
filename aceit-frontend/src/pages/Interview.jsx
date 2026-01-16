import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { API_BASE_URL } from '../services/api';

const SetupMode = ({ onStart }) => {
  // Simple setup for now, passing resume/jd stub
  return (
    <div className="flex flex-col items-center justify-center h-full bg-gray-900 text-white p-10 text-center">
      <h1 className="text-5xl font-bold mb-6">AI Voice Interview Room</h1>
      <p className="text-xl text-gray-400 mb-10 max-w-2xl">
        Experience a real-time interview. The AI will speak to you.
        Please ensure your camera and microphone are enabled.
      </p>
      <button
        onClick={() => onStart()}
        className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 px-12 rounded-full text-2xl shadow-lg transition transform hover:scale-105"
      >
        Enter Interview Room 🎥
      </button>
    </div>
  );
};

const Interview = () => {
  const { user } = useAuth();
  const [view, setView] = useState('setup');
  const [session, setSession] = useState(null);
  const [currentText, setCurrentText] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const videoRef = useRef(null);
  const audioRef = useRef(new Audio());
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  // Camera Setup
  useEffect(() => {
    if (view === 'session') {
      navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
          if (videoRef.current) videoRef.current.srcObject = stream;
        })
        .catch(console.error);
    }
  }, [view]);

  const playAudio = (url) => {
    if (!url) return;
    setIsSpeaking(true);
    const audio = audioRef.current;
    // ensure full url if relative
    audio.src = url.startsWith("http") ? url : `${API_BASE_URL}${url}`;
    audio.play();
    audio.onended = () => {
      setIsSpeaking(false);
      // Auto-start recording after AI speaks? Maybe manual is safer for now.
    };
  };

  const handleStart = async () => {
    console.log("[Interview] Starting interview...");

    try {
      const url = `${API_BASE_URL}/interview/start`;
      console.log("[Interview] Fetching:", url);

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user?.id || "demo_user",
          resume_text: "Experienced Python Developer",
          jd_text: "Seeking Python Backend Engineer"
        })
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`Server Error (${res.status}): ${errText}`);
      }

      const data = await res.json();
      console.log("[Interview] Session Data:", data);

      setSession(data);
      setCurrentText(data.text);
      setView('session');
      playAudio(data.audio_url);

    } catch (err) {
      console.error("[Interview] Error:", err);
      alert("Failed to start interview: " + err.message);
    }
  };

  const startRecording = () => {
    setIsListening(true);
    chunksRef.current = [];
    const stream = videoRef.current.srcObject;
    const mediaRecorder = new MediaRecorder(stream); // Record audio/video

    mediaRecorder.ondataavailable = e => chunksRef.current.push(e.data);
    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
      await submitAnswer(blob);
    };

    mediaRecorder.start();
    mediaRecorderRef.current = mediaRecorder;
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) mediaRecorderRef.current.stop();
    setIsListening(false);
  };

  const submitAnswer = async (audioBlob) => {
    setCurrentText("Thinking... 🧠");
    try {
      const formData = new FormData();
      formData.append('session_id', session.session_id);
      formData.append('audio_file', audioBlob, 'answer.webm');

      const res = await fetch(`${API_BASE_URL}/interview/answer`, {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      setCurrentText(data.text);

      if (data.is_completed) {
        alert("Interview Completed!");
        setView('setup');
      } else {
        playAudio(data.audio_url);
      }
    } catch (err) {
      console.error(err);
      setCurrentText("Error processing answer.");
    }
  };

  if (view === 'setup') return <SetupMode onStart={handleStart} />;

  return (
    <div className="h-screen bg-black text-white overflow-hidden relative">
      {/* Main Video Feed (User) */}
      <video ref={videoRef} autoPlay muted playsInline className="w-full h-full object-cover opacity-80" />

      {/* AI Overlay / Avatar Placeholder */}
      <div className="absolute top-10 left-10 w-32 h-32 rounded-full border-4 border-blue-500 overflow-hidden shadow-2xl bg-gray-800 flex items-center justify-center">
        <span className={`text-4xl ${isSpeaking ? 'animate-pulse' : ''}`}>🤖</span>
      </div>

      {/* Transcript / Question Overlay */}
      <div className="absolute bottom-32 left-0 right-0 p-6 text-center">
        <div className="bg-black bg-opacity-60 inline-block px-8 py-4 rounded-2xl backdrop-blur-md">
          <h2 className="text-2xl font-semibold shadow-black drop-shadow-md">
            {isSpeaking ? `🗣 ${currentText}` : `${currentText}`}
          </h2>
        </div>
      </div>

      {/* Controls */}
      <div className="absolute bottom-10 left-0 right-0 flex justify-center gap-6">
        {!isListening ? (
          <button
            onClick={startRecording}
            disabled={isSpeaking}
            className={`w-16 h-16 rounded-full flex items-center justify-center transition-all ${isSpeaking ? 'bg-gray-600' : 'bg-red-600 hover:bg-red-500 hover:scale-110 shadow-lg'}`}
          >
            🎙
          </button>
        ) : (
          <button
            onClick={stopRecording}
            className="w-16 h-16 rounded-full bg-gray-200 text-red-600 flex items-center justify-center animate-pulse hover:scale-110"
          >
            ⏹
          </button>
        )}
      </div>

      {/* Status Indicators */}
      {isSpeaking && <div className="absolute top-10 right-10 bg-green-500 px-4 py-1 rounded-full text-sm font-bold animate-bounce">AI Speaking...</div>}
      {isListening && <div className="absolute top-10 right-10 bg-red-500 px-4 py-1 rounded-full text-sm font-bold animate-pulse">Recording...</div>}

    </div>
  );
};

export default Interview;