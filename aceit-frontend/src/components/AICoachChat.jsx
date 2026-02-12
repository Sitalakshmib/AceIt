import React, { useState, useEffect, useRef } from 'react';
import { analyticsAPI, API_BASE_URL } from '../services/api';
import { Mic, Send, X, Square, Play, Pause, RotateCcw } from 'lucide-react';

const AICoachChat = ({ summary, compact = false }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [currentlyPlayingIdx, setCurrentlyPlayingIdx] = useState(null);
    const [isPaused, setIsPaused] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const audioPlayerRef = useRef(null);
    const chatEndRef = useRef(null);

    // Reset playing state when audio ends
    useEffect(() => {
        const player = audioPlayerRef.current;
        if (player) {
            const handleEnded = () => {
                setCurrentlyPlayingIdx(null);
                setIsPaused(false);
            };
            const handlePause = () => setIsPaused(true);
            const handlePlay = () => setIsPaused(false);

            player.addEventListener('ended', handleEnded);
            player.addEventListener('pause', handlePause);
            player.addEventListener('play', handlePlay);

            return () => {
                player.removeEventListener('ended', handleEnded);
                player.removeEventListener('pause', handlePause);
                player.removeEventListener('play', handlePlay);
            };
        }
    }, [audioPlayerRef.current]);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    // Initialize session when opening
    useEffect(() => {
        if (isOpen && !sessionId) {
            startSession();
        }
    }, [isOpen]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Auto-play AI audio when new message arrives (ONLY for the very first message)
    useEffect(() => {
        if (messages.length === 1) { // Only the initial intro
            const lastMsg = messages[messages.length - 1];
            if (lastMsg.role === 'assistant' && lastMsg.audio_url) {
                const url = (lastMsg.audio_url.startsWith('http') || lastMsg.audio_url.startsWith('data:'))
                    ? lastMsg.audio_url
                    : `${API_BASE_URL}${lastMsg.audio_url}`;

                if (audioPlayerRef.current) {
                    audioPlayerRef.current.src = url;
                    audioPlayerRef.current.play().catch(e => console.error("Auto-play blocked:", e));
                    setCurrentlyPlayingIdx(0); // Mark first message as playing
                    setIsPaused(false);
                }
            }
        }
    }, [messages]);

    const startSession = async () => {
        setIsProcessing(true);
        try {
            const res = await analyticsAPI.startCoach();
            setSessionId(res.data.session_id);
            setMessages([{
                role: 'assistant',
                content: res.data.text,
                audio_url: res.data.audio_url // Intro message has pre-generated audio
            }]);
        } catch (err) {
            console.error('Failed to start coach session:', err);
        } finally {
            setIsProcessing(false);
        }
    };

    const handleSend = async (textOverride = null, audioBlob = null) => {
        const textToSend = textOverride || input;
        if (!textToSend.trim() && !audioBlob) return;

        // Optimistic UI update
        if (textToSend) {
            setMessages(prev => [...prev, { role: 'user', content: textToSend }]);
            setInput('');
        } else if (audioBlob) {
            setMessages(prev => [...prev, { role: 'user', content: '[Audio Message]' }]);
        }

        setIsProcessing(true);

        try {
            const response = await analyticsAPI.sendCoachMessage(sessionId, textToSend, audioBlob);

            if (response.data.error) {
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    content: "I'm having a bit of trouble connecting to my brain right now! (Model busy). Please try again in 30 seconds."
                }]);
            } else {
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    content: response.data.text,
                    audio_url: response.data.audio_url // Typically null for replies (latency optimization)
                }]);
            }
        } catch (err) {
            console.error('Chat failed:', err);
            setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I hit a snag. Please try again.' }]);
        } finally {
            setIsProcessing(false);
        }
    };

    const handleReplay = async (msg, idx) => {
        if (!audioPlayerRef.current) return;

        // Force start from beginning
        const startAudio = (url) => {
            audioPlayerRef.current.src = url;
            audioPlayerRef.current.currentTime = 0;
            audioPlayerRef.current.play();
            setCurrentlyPlayingIdx(idx);
            setIsPaused(false);
        };

        // Case 1: Audio already pre-loaded or generated
        if (msg.audio_url) {
            const url = msg.audio_url.startsWith('http') || msg.audio_url.startsWith('data:')
                ? msg.audio_url
                : `${API_BASE_URL}${msg.audio_url}`;
            startAudio(url);
            return;
        }

        // Case 2: On-demand audio generation (for replies)
        setIsProcessing(true);
        try {
            const res = await analyticsAPI.generateCoachAudio(msg.content);
            if (res.data.audio_url) {
                const updatedMessages = [...messages];
                updatedMessages[idx].audio_url = res.data.audio_url;
                setMessages(updatedMessages);
                startAudio(res.data.audio_url);
            }
        } catch (err) {
            console.error('Failed to generate audio on-demand:', err);
        } finally {
            setIsProcessing(false);
        }
    };

    const handlePauseResume = () => {
        if (!audioPlayerRef.current) return;
        if (audioPlayerRef.current.paused) {
            audioPlayerRef.current.play();
            setIsPaused(false);
        } else {
            audioPlayerRef.current.pause();
            setIsPaused(true);
        }
    };

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (e) => {
                if (e.data.size > 0) audioChunksRef.current.push(e.data);
            };

            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                handleSend(null, audioBlob);
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
        } catch (err) {
            console.error('Recording failed:', err);
            alert('Could not access microphone.');
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    };

    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-6 right-6 z-50 hover:scale-110 transition-transform duration-300 group"
                title="Chat with AI Coach"
            >
                <div className="relative">
                    <img
                        src="/ai-coach-transparent.png"
                        alt="AI Coach"
                        className={`${compact ? 'h-32' : 'h-60'} w-auto drop-shadow-2xl hover:scale-110 transition-transform duration-300 filter`}
                    />

                    {/* Floating Badge - Always visible */}
                    <div className="absolute top-1/2 right-full -translate-y-1/2 mr-4 bg-white text-gray-800 text-xs font-bold px-4 py-2 rounded-xl shadow-lg border border-blue-100 flex flex-col items-center gap-0.5 w-max">
                        <span className="text-[10px] text-blue-500 uppercase tracking-wider">Hi! I'm your AI Coach</span>
                        <span className="whitespace-nowrap">Ask doubts & Learn with me!</span>

                        {/* Triangle pointer */}
                        <div className="absolute top-1/2 -right-2 -translate-y-1/2 w-0 h-0 border-t-[6px] border-t-transparent border-l-[8px] border-l-white border-b-[6px] border-b-transparent"></div>
                    </div>
                </div>
            </button>
        );
    }

    return (
        <div className="fixed bottom-8 right-8 w-96 h-[500px] bg-white rounded-3xl shadow-2xl z-50 flex flex-col border border-gray-100 overflow-hidden animate-in slide-in-from-bottom-10 fade-in">
            {/* Hidden Audio Player */}
            <audio ref={audioPlayerRef} className="hidden" controls />

            <div className="p-4 bg-gradient-to-r from-blue-600 to-indigo-700 text-white flex justify-between items-center">
                <div className="flex items-center gap-3">
                    <div className="relative">
                        <img src="/ai-coach-transparent.png" alt="AI Coach" className="h-10 w-10 rounded-full border-2 border-white/30 object-cover" />
                        <div className="absolute bottom-0 right-0 h-2.5 w-2.5 bg-green-400 border-2 border-blue-600 rounded-full"></div>
                    </div>
                    <div>
                        <h4 className="font-bold text-sm">AceIt AI Coach</h4>
                        <p className="text-[10px] text-blue-100 uppercase tracking-widest">Personalized Guidance</p>
                    </div>
                </div>
                <button onClick={() => setIsOpen(false)} className="p-2 hover:bg-white/10 rounded-full">
                    <X className="h-5 w-5" />
                </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} `}>
                        <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${msg.role === 'user'
                            ? 'bg-blue-600 text-white rounded-tr-none'
                            : 'bg-white text-gray-800 shadow-sm rounded-tl-none border border-gray-100'
                            } `}>
                            <p>{msg.content}</p>
                            {msg.role === 'assistant' && (
                                <div className="mt-2 flex items-center gap-2 pt-2 border-t border-gray-50">
                                    <button
                                        onClick={() => currentlyPlayingIdx === idx ? handlePauseResume() : handleReplay(msg, idx)}
                                        className={`p-2 rounded-full transition-all flex items-center justify-center ${currentlyPlayingIdx === idx ? 'bg-orange-100 text-orange-600 ring-2 ring-orange-200' : 'bg-blue-50 text-blue-600 hover:bg-blue-100'} `}
                                        disabled={isProcessing && currentlyPlayingIdx !== idx}
                                        title={currentlyPlayingIdx === idx ? (isPaused ? "Resume" : "Pause") : "Play"}
                                    >
                                        {currentlyPlayingIdx === idx && !isPaused ?
                                            <Pause className="h-4 w-4 fill-current" /> :
                                            <Play className="h-4 w-4 fill-current ml-0.5" />
                                        }
                                    </button>

                                    <button
                                        onClick={() => handleReplay(msg, idx)}
                                        className="p-2 rounded-full text-gray-400 hover:bg-gray-100 hover:text-blue-500 transition-all"
                                        title="Replay from Start"
                                        disabled={isProcessing && currentlyPlayingIdx !== idx}
                                    >
                                        <RotateCcw className="h-4 w-4" />
                                    </button>

                                    {currentlyPlayingIdx === idx && (
                                        <span className="text-[10px] font-bold uppercase tracking-wider text-orange-500 ml-2 animate-pulse">
                                            {isPaused ? 'Paused' : 'Playing'}
                                        </span>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {isProcessing && (
                    <div className="flex justify-start">
                        <div className="bg-white p-3 rounded-2xl shadow-sm border border-gray-100 rounded-tl-none">
                            <div className="flex gap-1">
                                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={chatEndRef} />
            </div>

            <div className="p-4 bg-white border-t border-gray-100 flex gap-2 items-center">
                <button
                    onClick={isRecording ? stopRecording : startRecording}
                    className={`p-3 rounded-xl transition-all ${isRecording ? 'bg-red-500 text-white animate-pulse ring-4 ring-red-200' : 'bg-gray-100 text-gray-400 hover:bg-gray-200'} `}
                    title={isRecording ? "Click to Stop" : "Click to Record"}
                >
                    {isRecording ? <Square className="h-5 w-5 fill-current" /> : <Mic className="h-5 w-5" />}
                </button>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder={isRecording ? "Listening..." : "Ask your coach..."}
                    className="flex-1 text-sm bg-gray-50 border-none rounded-xl px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
                    disabled={isProcessing}
                />
                <button
                    onClick={() => handleSend()}
                    disabled={isProcessing || !input.trim()}
                    className="p-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:opacity-50 shadow-lg shadow-blue-200"
                >
                    <Send className="h-5 w-5" />
                </button>
            </div>
        </div>
    );
};

export default AICoachChat;
