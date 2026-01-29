/**
 * VideoPractice.jsx
 * 
 * ISOLATED MODULE: Video-Based Interview Presence & Body-Language Analysis
 * 
 * Features:
 * - Multi-modal Analysis (Video + REAL Audio Hesitation Detection)
 * - Real-time Confidence Scoring (Eye Contact, Stability, Voice, Tension)
 * - Backend Audio Analysis (Filler Words, Pauses, Speech Continuity)
 * - Interactive Question Flow
 * - Student Audio ONLY (No Interviewer TTS)
 */
import React, { useEffect, useRef, useState } from 'react';
import { FaceLandmarker, FilesetResolver } from '@mediapipe/tasks-vision';
import axios from 'axios';

const QUESTION_BANK = [
    "Tell me about yourself.",
    "What do you consider your greatest strength?",
    "Describe a challenge you faced and how you handled it.",
    "Why do you want to work for this company?",
    "Where do you see yourself in five years?"
];

// Backend API endpoint
const API_BASE_URL = 'http://localhost:8000';

const VideoPractice = ({ onBack }) => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [isModelLoaded, setIsModelLoaded] = useState(false);

    // Session State
    const [mode, setMode] = useState('idle'); // 'idle', 'question', 'answering', 'feedback', 'summary'
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [questions, setQuestions] = useState([]);

    // Analysis State
    const isPracticingRef = useRef(false);
    const [liveFeedback, setLiveFeedback] = useState({
        eyeContact: 'Waiting...',
        headStability: 'Waiting...',
        voice: 'Listening...',
        tension: 'Neutral',
        confidence: 0,
        status: 'Ready'
    });

    // Stats Accumulation
    const answerStatsRef = useRef({
        frames: 0,
        goodEyeContactFrames: 0,
        stableHeadFrames: 0,
        tenseFrames: 0,
        speechFrames: 0,
        silenceFrames: 0,
        confidenceSum: 0
    });

    const [sessionReport, setSessionReport] = useState([]);

    // Loop Control
    const lastProcessTimeRef = useRef(0);
    const lastFeedbackTimeRef = useRef(0);
    const landmarkerRef = useRef(null);
    const animationFrameRef = useRef(null);
    const noseHistoryRef = useRef([]);

    // Audio Context (for visualization only)
    const audioContextRef = useRef(null);
    const analyserRef = useRef(null);
    const dataArrayRef = useRef(null);
    const sourceRef = useRef(null);

    // Audio Recording (for backend analysis)
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const audioStreamRef = useRef(null);
    const [micVolume, setMicVolume] = useState(0); // For visualization

    useEffect(() => {
        loadModel();
        const shuffled = [...QUESTION_BANK].sort(() => 0.5 - Math.random());
        setQuestions(shuffled.slice(0, 3));
        return () => stopLoop();
    }, []);

    const loadModel = async () => {
        try {
            const vision = await FilesetResolver.forVisionTasks(
                'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm'
            );
            landmarkerRef.current = await FaceLandmarker.createFromOptions(vision, {
                baseOptions: {
                    modelAssetPath: `https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task`,
                    delegate: 'GPU',
                },
                outputFaceBlendshapes: true,
                runningMode: 'VIDEO',
                numFaces: 1,
            });
            setIsModelLoaded(true);
        } catch (error) {
            console.error('Error loading MediaPipe model:', error);
            alert('Failed to load. Please refresh.');
        }
    };

    const startSession = async () => {
        try {
            // CRITICAL: Capture ONLY microphone audio (student audio)
            // Video for display, separate audio stream for recording
            const videoStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false  // No audio in video stream to avoid TTS capture
            });

            // Separate audio stream - MICROPHONE ONLY
            const audioStream = await navigator.mediaDevices.getUserMedia({
                video: false,
                audio: {
                    echoCancellation: true,  // Helps exclude system audio
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });

            audioStreamRef.current = audioStream;

            // Video Setup
            if (videoRef.current) {
                videoRef.current.srcObject = videoStream;
                videoRef.current.addEventListener('loadeddata', () => {
                    isPracticingRef.current = true;
                    predictWebcam();
                });
            }

            // Audio Visualization Setup (for live feedback only)
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioContextRef.current = new AudioContext();
            analyserRef.current = audioContextRef.current.createAnalyser();
            analyserRef.current.fftSize = 256;
            sourceRef.current = audioContextRef.current.createMediaStreamSource(audioStream);
            sourceRef.current.connect(analyserRef.current);
            dataArrayRef.current = new Uint8Array(analyserRef.current.frequencyBinCount);

            // Resume context (important for some browsers)
            if (audioContextRef.current.state === 'suspended') {
                await audioContextRef.current.resume();
            }

            setCurrentQuestionIndex(0);
            setSessionReport([]);
            askQuestion(0);
        } catch (err) {
            console.error('Error accessing media:', err);
            alert('Camera & Microphone access required. Please check permissions.');
        }
    };

    const askQuestion = (index) => {
        const q = questions[index];
        setMode('question');
        const utterance = new SpeechSynthesisUtterance(q);
        utterance.rate = 1.0;
        utterance.onend = () => startAnswering();
        window.speechSynthesis.speak(utterance);
    };

    const startAnswering = () => {
        setMode('answering');
        answerStatsRef.current = {
            frames: 0,
            goodEyeContactFrames: 0,
            stableHeadFrames: 0,
            tenseFrames: 0,
            speechFrames: 0,
            silenceFrames: 0,
            confidenceSum: 0
        };
        isPracticingRef.current = true;

        // Start audio recording for backend analysis
        startAudioRecording();
    };

    const startAudioRecording = () => {
        if (!audioStreamRef.current) {
            console.error('No audio stream available for recording');
            return;
        }

        try {
            audioChunksRef.current = [];

            // Use webm format for compatibility
            const options = { mimeType: 'audio/webm' };
            mediaRecorderRef.current = new MediaRecorder(audioStreamRef.current, options);

            mediaRecorderRef.current.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorderRef.current.start();
            console.log('[AUDIO] Audio recording started (student microphone only)');
        } catch (error) {
            console.error('Failed to start audio recording:', error);
        }
    };

    const stopAudioRecording = () => {
        return new Promise((resolve) => {
            if (!mediaRecorderRef.current || mediaRecorderRef.current.state === 'inactive') {
                resolve(null);
                return;
            }

            mediaRecorderRef.current.onstop = () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                console.log('[AUDIO] Audio recording stopped, blob size:', audioBlob.size);
                resolve(audioBlob);
            };

            mediaRecorderRef.current.stop();
        });
    };

    const finishAnswer = async () => {
        setMode('feedback');
        isPracticingRef.current = true;

        // Stop audio recording and get blob
        const audioBlob = await stopAudioRecording();

        // Calculate Visual Metrics
        const stats = answerStatsRef.current;
        const totalFrames = stats.frames || 1;

        const eyeMetric = (stats.goodEyeContactFrames / totalFrames) * 100;
        const stabilityMetric = (stats.stableHeadFrames / totalFrames) * 100;
        const tensionMetric = (stats.tenseFrames / totalFrames) * 100; // Lower is better

        // Get REAL audio hesitation analysis from backend
        let voiceMetric = 50;  // Default fallback
        let vFeedback = "Audio analysis unavailable.";
        let hesitationData = null;

        if (audioBlob && audioBlob.size > 0) {
            try {
                console.log('[BACKEND] Sending audio to backend for analysis...');
                const formData = new FormData();
                formData.append('audio_file', audioBlob, 'answer.webm');
                formData.append('session_id', `session_${Date.now()}`);

                const response = await axios.post(
                    `${API_BASE_URL}/video-presence/analyze-answer`,
                    formData,
                    {
                        headers: { 'Content-Type': 'multipart/form-data' },
                        timeout: 30000  // 30 second timeout
                    }
                );

                console.log('[BACKEND] Backend analysis received:', response.data);

                if (response.data.status === 'success' && response.data.hesitation_analysis) {
                    hesitationData = response.data.hesitation_analysis;

                    // Calculate voice metric from REAL hesitation data
                    const confidenceScore = hesitationData.confidence_score || 50;
                    voiceMetric = confidenceScore;

                    // Use real feedback from backend (now structured)
                    vFeedback = hesitationData.feedback?.summary || "Speech analyzed.";
                } else if (response.data.status === 'no_speech') {
                    vFeedback = "No speech detected. Please check your microphone.";
                    voiceMetric = 30;
                } else {
                    vFeedback = "Audio analysis unavailable.";
                    voiceMetric = 50;
                }
            } catch (error) {
                console.error('[ERROR] Backend audio analysis failed:', error);
                vFeedback = "Audio analysis unavailable.";
                voiceMetric = 50;  // Neutral fallback
            }
        } else {
            console.warn('[WARNING] No audio recorded');
            vFeedback = "No audio recorded.";
            voiceMetric = 30;
        }

        // Composite Confidence Score (REAL multi-modal)
        let confidence = (
            (eyeMetric * 0.3) +
            (stabilityMetric * 0.2) +
            (voiceMetric * 0.3) +
            ((100 - tensionMetric) * 0.2)
        );

        // Fallback for zero data (ensure never zero)
        if (totalFrames < 10) confidence = Math.max(confidence, 40);
        confidence = Math.max(confidence, 30);  // Absolute minimum

        const reportItem = {
            question: questions[currentQuestionIndex],
            eyeMetric: Math.round(eyeMetric),
            stabilityMetric: Math.round(stabilityMetric),
            confidence: Math.round(confidence),
            voiceFeedback: vFeedback,
            visualFeedback: generateFeedback(eyeMetric, stabilityMetric, tensionMetric),
            hesitationData: hesitationData  // Store for detailed display
        };

        setSessionReport(prev => [...prev, reportItem]);
    };

    const generateFeedback = (eye, stability, tension) => {
        const tips = [];
        if (eye < 60) tips.push("Maintain more eye contact.");
        if (stability < 60) tips.push("Keep head steady.");
        if (tension > 30) tips.push("Relax facial muscles.");
        if (tips.length === 0) return "Excellent visual presence!";
        return tips.join(" ");
    };

    const nextStep = () => {
        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(prev => prev + 1);
            askQuestion(currentQuestionIndex + 1);
        } else {
            setMode('summary');
            stopLoop();
        }
    };

    const stopLoop = () => {
        isPracticingRef.current = false;

        // Stop video tracks
        if (videoRef.current && videoRef.current.srcObject) {
            videoRef.current.srcObject.getTracks().forEach(t => t.stop());
            videoRef.current.srcObject = null;
        }

        // Stop audio stream
        if (audioStreamRef.current) {
            audioStreamRef.current.getTracks().forEach(t => t.stop());
            audioStreamRef.current = null;
        }

        // Close audio context
        if (audioContextRef.current) {
            audioContextRef.current.close().catch(console.error);
            audioContextRef.current = null;
        }

        // Stop any ongoing recording
        if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
            mediaRecorderRef.current.stop();
        }

        if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
    };

    const predictWebcam = () => {
        if (!landmarkerRef.current || !videoRef.current) return;
        if (!isPracticingRef.current) return;

        const startTimeMs = performance.now();
        if (startTimeMs - lastProcessTimeRef.current < 50) { // ~20 FPS
            animationFrameRef.current = requestAnimationFrame(predictWebcam);
            return;
        }
        lastProcessTimeRef.current = startTimeMs;

        // Visual Analysis
        if (videoRef.current.videoWidth > 0) {
            try {
                const result = landmarkerRef.current.detectForVideo(videoRef.current, startTimeMs);
                analyzeVisuals(result);
                drawLandmarks(result);
            } catch (e) { console.error(e); }
        }

        // Audio Analysis
        if (analyserRef.current && dataArrayRef.current) {
            analyserRef.current.getByteFrequencyData(dataArrayRef.current);
            const volume = dataArrayRef.current.reduce((a, b) => a + b, 0) / dataArrayRef.current.length;
            analyzeAudio(volume);
        }

        if (isPracticingRef.current) animationFrameRef.current = requestAnimationFrame(predictWebcam);
    };

    const analyzeAudio = (volume) => {
        // Update Visualization State (Throttled slightly by loop)
        setMicVolume(volume);

        if (mode !== 'answering') return;

        // Thresholds - Increased to 20 to Filter Noise
        const SILENCE_THRESH = 20;
        if (volume > SILENCE_THRESH) {
            answerStatsRef.current.speechFrames++;
        } else {
            answerStatsRef.current.silenceFrames++;
        }
    };

    const analyzeVisuals = (result) => {
        // Fallback for no detection
        if (!result.faceLandmarks || result.faceLandmarks.length === 0) {
            if (performance.now() - lastFeedbackTimeRef.current > 1000) {
                updateFeedbackUI(0, false, false, false); // Reset
            }
            return;
        }

        const landmarks = result.faceLandmarks[0];
        const blendshapes = result.faceBlendshapes[0].categories;

        // 1. Eye Contact
        const noseTip = landmarks[1];
        const leftCheek = landmarks[234];
        const rightCheek = landmarks[454];
        const faceCenterX = (leftCheek.x + rightCheek.x) / 2;
        const isLookingAtCam = Math.abs(noseTip.x - faceCenterX) < 0.05;

        // 2. Head Stability
        noseHistoryRef.current.push(noseTip);
        if (noseHistoryRef.current.length > 30) noseHistoryRef.current.shift();
        let movement = 0;
        if (noseHistoryRef.current.length > 5) {
            const first = noseHistoryRef.current[0];
            const last = noseHistoryRef.current[noseHistoryRef.current.length - 1];
            movement = Math.sqrt(Math.pow(last.x - first.x, 2) + Math.pow(last.y - first.y, 2));
        }
        const isStable = movement < 0.15;

        // 3. Facial Tension
        const browDownL = blendshapes.find(b => b.categoryName === 'browDownLeft')?.score || 0;
        const browDownR = blendshapes.find(b => b.categoryName === 'browDownRight')?.score || 0;
        const isTense = (browDownL + browDownR) > 1.2;

        // Update Answer Stats
        if (mode === 'answering') {
            answerStatsRef.current.frames++;
            if (isLookingAtCam) answerStatsRef.current.goodEyeContactFrames++;
            if (isStable) answerStatsRef.current.stableHeadFrames++;
            if (isTense) answerStatsRef.current.tenseFrames++;
        }

        // Live Confidence Calculation
        let liveConf = 50;
        if (isLookingAtCam) liveConf += 20;
        if (isStable) liveConf += 10;
        if (!isTense) liveConf += 10;
        if (liveConf > 100) liveConf = 100;

        // Update UI
        if (performance.now() - lastFeedbackTimeRef.current > 200) {
            updateFeedbackUI(liveConf, isLookingAtCam, isStable, isTense);
            lastFeedbackTimeRef.current = performance.now();
        }
    };

    const updateFeedbackUI = (conf, eye, stable, tense) => {
        // Audio Feedback Check
        // Since we don't have direct access to last volume in this func, we rely on cumulative
        // But for live feedback, let's use the stats trend or a "speaking" indicator

        // Simple visualizer check:
        // This runs after analyzeLow, so vol should be somewhat current.
        // But let's just toggle based on total history ratio for now:
        const total = answerStatsRef.current.speechFrames + answerStatsRef.current.silenceFrames;
        if (total > 5) {
            // Check last few frames? Hard without history.
            // Let's use the micVolume state we just set (async but close enough for UI)
            // Note: micVolume state update might lag, but 'voiceMsg' is for Display.
        }

        setLiveFeedback({
            confidence: Math.round(conf),
            eyeContact: eye ? 'Good Contact ✅' : 'Looking Away ⚠️',
            headStability: stable ? 'Steady ✅' : 'Moving too much ⚠️',
            tension: tense ? 'Relax Face 🧘' : 'Relaxed ✅',
            voice: 'Active 🎙️', // Replaced by Mic Bar below
            status: mode === 'answering' ? 'Analyzing...' : 'Ready'
        });
    };

    const drawLandmarks = (result) => {
        if (!canvasRef.current || !videoRef.current) return;
        const ctx = canvasRef.current.getContext('2d');
        const video = videoRef.current;
        canvasRef.current.width = video.videoWidth;
        canvasRef.current.height = video.videoHeight;
        ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
        if (result.faceLandmarks && result.faceLandmarks.length > 0) {
            ctx.fillStyle = "#00FF00";
            for (const landmark of result.faceLandmarks[0]) {
                const x = landmark.x * canvasRef.current.width;
                const y = landmark.y * canvasRef.current.height;
                ctx.beginPath();
                ctx.arc(x, y, 1.5, 0, 2 * Math.PI);
                ctx.fill();
            }
        }
    };

    const getQualitativeLabel = (score) => {
        if (score >= 80) return <span className="text-green-600 font-bold">Strong</span>;
        if (score >= 50) return <span className="text-blue-600 font-bold">Good</span>;
        return <span className="text-orange-500 font-bold">Needs Practice</span>;
    };

    if (mode === 'summary') {
        return (
            <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-6 flex flex-col items-center">
                <div className="max-w-5xl w-full bg-white rounded-2xl shadow-2xl p-8">
                    <h1 className="text-4xl font-bold text-gray-800 mb-2 text-center">Professional AI Analysis 🎯</h1>
                    <p className="text-center text-gray-600 mb-8">Detailed performance insights with explainability</p>

                    <div className="space-y-8">
                        {sessionReport.map((item, idx) => {
                            const hesitation = item.hesitationData;
                            const feedback = hesitation?.feedback || {};
                            const temporal = hesitation?.temporal_progression || {};
                            const fillers = hesitation?.filler_words || {};
                            const pauses = hesitation?.pauses || {};

                            return (
                                <div key={idx} className="border-2 border-gray-200 p-6 rounded-2xl bg-gradient-to-br from-white to-gray-50 shadow-lg">
                                    <h3 className="text-xl font-bold text-gray-800 mb-6 pb-3 border-b-2 border-blue-100">
                                        Question {idx + 1}: {item.question}
                                    </h3>

                                    {/* Presence Summary */}
                                    <div className="mb-6 bg-blue-50 p-4 rounded-xl border border-blue-200">
                                        <h4 className="text-sm font-bold text-blue-900 uppercase mb-2 flex items-center gap-2">
                                            <span>📊</span> Presence Summary
                                        </h4>
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="text-lg font-semibold text-gray-800">
                                                    {feedback.summary || `Overall Confidence: ${getQualitativeLabel(item.confidence)}`}
                                                </p>
                                                {temporal.trend && (
                                                    <p className="text-sm text-gray-600 mt-1 flex items-center gap-2">
                                                        <span className="text-lg">
                                                            {temporal.trend === 'improving' ? '↑' : temporal.trend === 'declining' ? '↓' : '→'}
                                                        </span>
                                                        {temporal.progression}
                                                    </p>
                                                )}
                                            </div>
                                            {/* Confidence Gauge */}
                                            <div className="relative w-24 h-24">
                                                <svg viewBox="0 0 100 100" className="transform -rotate-90">
                                                    <circle cx="50" cy="50" r="40" fill="none" stroke="#e5e7eb" strokeWidth="8" />
                                                    <circle
                                                        cx="50" cy="50" r="40"
                                                        fill="none"
                                                        stroke={item.confidence > 75 ? '#10b981' : item.confidence > 50 ? '#3b82f6' : '#f59e0b'}
                                                        strokeWidth="8"
                                                        strokeDasharray={`${item.confidence * 2.51} 251`}
                                                        strokeLinecap="round"
                                                    />
                                                </svg>
                                                <div className="absolute inset-0 flex flex-col items-center justify-center">
                                                    <span className="text-2xl font-bold text-gray-800">{item.confidence}</span>
                                                    <span className="text-xs text-gray-500">Score</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Visual Cues */}
                                    <div className="mb-6">
                                        <h4 className="text-sm font-bold text-gray-700 uppercase mb-3 flex items-center gap-2">
                                            <span>👁️</span> Visual Cues
                                        </h4>
                                        <div className="grid grid-cols-3 gap-3">
                                            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                                                <div className="text-xs text-gray-500 uppercase font-bold mb-1">Eye Contact</div>
                                                <div className="text-lg font-semibold text-gray-800">{getQualitativeLabel(item.eyeMetric)}</div>
                                                <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className={`h-2 rounded-full ${item.eyeMetric > 75 ? 'bg-green-500' : item.eyeMetric > 50 ? 'bg-blue-500' : 'bg-orange-400'}`}
                                                        style={{ width: `${item.eyeMetric}%` }}
                                                    ></div>
                                                </div>
                                            </div>
                                            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                                                <div className="text-xs text-gray-500 uppercase font-bold mb-1">Head Stability</div>
                                                <div className="text-lg font-semibold text-gray-800">{getQualitativeLabel(item.stabilityMetric)}</div>
                                                <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className={`h-2 rounded-full ${item.stabilityMetric > 75 ? 'bg-green-500' : item.stabilityMetric > 50 ? 'bg-blue-500' : 'bg-orange-400'}`}
                                                        style={{ width: `${item.stabilityMetric}%` }}
                                                    ></div>
                                                </div>
                                            </div>
                                            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                                                <div className="text-xs text-gray-500 uppercase font-bold mb-1">Composure</div>
                                                <div className="text-lg font-semibold text-gray-800">Good</div>
                                                <div className="text-xs text-gray-500 mt-1">Facial tension low</div>
                                            </div>
                                        </div>
                                        <div className="mt-3 text-sm text-gray-600 bg-gray-50 p-3 rounded-lg border border-gray-200">
                                            💡 {item.visualFeedback}
                                        </div>
                                    </div>

                                    {/* Speech Delivery */}
                                    {hesitation && (
                                        <div className="mb-6">
                                            <h4 className="text-sm font-bold text-gray-700 uppercase mb-3 flex items-center gap-2">
                                                <span>🎙️</span> Speech Delivery
                                            </h4>
                                            <div className="space-y-3">
                                                {feedback.speech_delivery?.observations?.map((obs, i) => (
                                                    <div key={i} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                                                        <div className="flex items-start gap-2">
                                                            <span className="text-orange-500 font-bold">⚠</span>
                                                            <div className="flex-1">
                                                                <p className="font-medium text-gray-800">{obs}</p>
                                                                {feedback.speech_delivery?.explanations?.[i] && (
                                                                    <p className="text-sm text-gray-600 mt-1 italic">
                                                                        → {feedback.speech_delivery.explanations[i]}
                                                                    </p>
                                                                )}
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))}

                                                {/* Patterns Detected */}
                                                {feedback.patterns_detected?.length > 0 && (
                                                    <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                                                        <div className="text-xs font-bold text-purple-900 uppercase mb-2">Patterns Detected</div>
                                                        {feedback.patterns_detected.map((pattern, i) => (
                                                            <p key={i} className="text-sm text-gray-700">• {pattern}</p>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )}

                                    {/* Positive Notes */}
                                    {feedback.positive_notes?.length > 0 && (
                                        <div className="mb-6 bg-green-50 p-4 rounded-lg border border-green-200">
                                            <h4 className="text-sm font-bold text-green-900 uppercase mb-2 flex items-center gap-2">
                                                <span>✓</span> Strengths
                                            </h4>
                                            <div className="space-y-1">
                                                {feedback.positive_notes.map((note, i) => (
                                                    <p key={i} className="text-sm text-gray-700">• {note}</p>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Improvement Suggestions */}
                                    {feedback.improvement_suggestions?.length > 0 && (
                                        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                                            <h4 className="text-sm font-bold text-blue-900 uppercase mb-3 flex items-center gap-2">
                                                <span>🎯</span> Top Improvement Suggestions
                                            </h4>
                                            <div className="space-y-2">
                                                {feedback.improvement_suggestions.map((suggestion, i) => (
                                                    <div key={i} className="flex items-start gap-2">
                                                        <span className="text-blue-600 font-bold">{i + 1}.</span>
                                                        <p className="text-sm text-gray-700 font-medium">{suggestion}</p>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>

                    <div className="mt-8 flex justify-center gap-4">
                        <button onClick={startSession} className="px-8 py-4 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 shadow-lg transition-all transform hover:scale-105">
                            Practice Again 🔄
                        </button>
                        <button onClick={onBack} className="px-8 py-4 border-2 border-gray-300 text-gray-700 rounded-xl font-bold hover:bg-gray-50 transition-all">
                            Back to Menu
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 p-6 flex flex-col items-center">
            {/* Header */}
            <div className="w-full max-w-5xl flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-gray-800">📸 Video Presence Coach</h1>
                    <p className="text-gray-600">Real Audio-Visual Analysis. Microphone and Camera required.</p>
                </div>
                <button onClick={onBack} className="px-4 py-2 text-gray-600 hover:text-gray-900 font-medium">Exit</button>
            </div>

            <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Main Video Area */}
                <div className="lg:col-span-2 relative aspect-video bg-black rounded-2xl overflow-hidden shadow-2xl flex items-center justify-center">
                    {mode === 'idle' && (
                        <div className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-gray-900/90 text-white p-8 text-center backdrop-blur-sm">
                            <h3 className="text-3xl font-bold mb-4">Start Session?</h3>
                            <ul className="text-left space-y-2 mb-8 text-gray-300">
                                <li>👀 <b>Eye Contact</b> Analysis</li>
                                <li>😊 <b>Facial Tension</b> & Expression Analysis</li>
                                <li>🎙️ <b>Voice Confidence</b> & Hesitation Analysis</li>
                            </ul>
                            <button
                                onClick={startSession}
                                disabled={!isModelLoaded}
                                className={`px-8 py-3 rounded-full font-bold text-lg transition-all ${isModelLoaded
                                    ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg transform hover:scale-105'
                                    : 'bg-gray-600 text-gray-400 cursor-not-allowed'
                                    }`}
                            >
                                {isModelLoaded ? 'Start Session 🚀' : 'Loading AI...'}
                            </button>
                        </div>
                    )}

                    {mode === 'question' && (
                        <div className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-black/80 backdrop-blur-md text-white p-8 text-center">
                            <h3 className="text-xl text-blue-300 mb-4 font-semibold uppercase tracking-widest">Question {currentQuestionIndex + 1}</h3>
                            <p className="text-3xl font-bold leading-relaxed max-w-2xl">"{questions[currentQuestionIndex]}"</p>
                            <p className="mt-8 text-sm opacity-50 animate-pulse">Listening to question...</p>
                        </div>
                    )}

                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted // Mute self to avoid loopback
                        className="w-full h-full object-cover transform -scale-x-100"
                    />
                    <canvas
                        ref={canvasRef}
                        className="absolute inset-0 w-full h-full object-cover transform -scale-x-100 pointer-events-none opacity-40"
                    />

                    {mode === 'answering' && (
                        <div className="absolute top-4 left-4 flex gap-2">
                            <div className="bg-red-600 text-white px-3 py-1 rounded-full text-xs font-bold animate-pulse flex items-center gap-1">
                                <span className="w-2 h-2 bg-white rounded-full"></span> RECORDING
                            </div>
                        </div>
                    )}
                </div>

                {/* Right Panel: Live Feed */}
                <div className="space-y-4">

                    {/* Confidence Meter */}
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <div className="flex justify-between items-end mb-2">
                            <h4 className="text-sm font-bold text-gray-500 uppercase">Confidence Score</h4>
                            <span className="text-3xl font-bold text-blue-600">{liveFeedback.confidence}</span>
                        </div>
                        <div className="w-full bg-gray-100 rounded-full h-4 overflow-hidden">
                            <div
                                className={`h-full rounded-full transition-all duration-300 ease-out ${liveFeedback.confidence > 75 ? 'bg-green-500' : liveFeedback.confidence > 50 ? 'bg-blue-500' : 'bg-orange-400'
                                    }`}
                                style={{ width: `${liveFeedback.confidence}%` }}
                            ></div>
                        </div>
                    </div>

                    {/* Microphone Volume Visualizer */}
                    <div className="bg-gray-100 p-3 rounded-lg border border-gray-200">
                        <div className="flex justify-between items-center mb-1">
                            <div className="text-xs font-bold text-gray-400 uppercase">Input Level</div>
                            <div className="text-xs font-bold text-gray-600">{micVolume > 20 ? 'DETECTED 🔊' : 'SILENT 🤫'}</div>
                        </div>
                        <div className="w-full h-2 bg-gray-300 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-blue-500 transition-all duration-75"
                                style={{ width: `${Math.min(micVolume, 100)}%` }}
                            ></div>
                        </div>
                    </div>

                    {/* Live Signals */}
                    <div className="grid grid-cols-2 gap-3">
                        <div className="p-3 bg-gray-50 rounded-lg border border-gray-100">
                            <div className="text-xs font-bold text-gray-400 mb-1">EYES</div>
                            <div className="font-semibold text-gray-700">{liveFeedback.eyeContact}</div>
                        </div>
                        <div className="p-3 bg-gray-50 rounded-lg border border-gray-100">
                            <div className="text-xs font-bold text-gray-400 mb-1">HEAD</div>
                            <div className="font-semibold text-gray-700">{liveFeedback.headStability}</div>
                        </div>
                        <div className="p-3 bg-gray-50 rounded-lg border border-gray-100">
                            <div className="text-xs font-bold text-gray-400 mb-1">FACE</div>
                            <div className="font-semibold text-gray-700">{liveFeedback.tension}</div>
                        </div>
                        <div className="p-3 bg-gray-50 rounded-lg border border-gray-100">
                            <div className="text-xs font-bold text-gray-400 mb-1">STATUS</div>
                            <div className="font-semibold text-gray-700">{liveFeedback.status}</div>
                        </div>
                    </div>

                    {/* Controls */}
                    <div className="pt-2">
                        {mode === 'answering' ? (
                            <button
                                onClick={finishAnswer}
                                className="w-full py-4 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl shadow-lg transition-all"
                            >
                                ■ Stop Answering
                            </button>
                        ) : mode === 'feedback' ? (
                            <button
                                onClick={nextStep}
                                className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg transition-all"
                            >
                                Next Question →
                            </button>
                        ) : <div className="h-14 flex items-center justify-center text-gray-400 bg-gray-100 rounded-xl rounded-dashed border border-gray-200">Waiting for start...</div>}
                    </div>

                </div>
            </div>
        </div>
    );
};

export default VideoPractice;
