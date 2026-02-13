import React, { useState, useRef, useEffect } from 'react';
import './AITutor.css';
import {
    Bot, X, Trash2, Lightbulb, Bug, FileText,
    BookOpen, MessageCircle, Send, AlertTriangle, CheckCircle
} from 'lucide-react';

const AITutor = ({
    isOpen,
    onClose,
    currentProblem,
    userCode,
    testResults
}) => {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: `👋 Hi! I'm your AI Tutor. I can help you with:

💡 **Hints** - Get progressive hints without spoilers
🐛 **Debug** - Understand why your code failed
📝 **Review** - Get feedback on your solution
📖 **Explain** - Learn the optimal approach
💬 **Ask** - Any algorithm questions

What would you like help with?`,
            type: 'welcome'
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [hintLevel, setHintLevel] = useState(1);
    const messagesEndRef = useRef(null);

    const API_BASE = 'http://localhost:8000/tutor';

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const addMessage = (role, content, type = 'text') => {
        setMessages(prev => [...prev, { role, content, type }]);
    };

    const getHint = async () => {
        if (!currentProblem) {
            addMessage('assistant', '⚠️ Please select a problem first.', 'error');
            return;
        }

        setIsLoading(true);
        addMessage('user', `💡 Give me a Level ${hintLevel} hint`, 'action');

        try {
            const response = await fetch(`${API_BASE}/hint`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    problem_title: currentProblem.title,
                    problem_description: currentProblem.description,
                    user_code: userCode,
                    hint_level: hintLevel,
                    tags: currentProblem.tags || []
                })
            });

            const data = await response.json();
            if (data.success) {
                addMessage('assistant', `💡 **Level ${hintLevel} Hint:**\n\n${data.response}`, 'hint');
                // Increment hint level for next time
                if (hintLevel < 3) setHintLevel(hintLevel + 1);
            } else {
                addMessage('assistant', '❌ Sorry, I couldn\'t generate a hint. Please try again.', 'error');
            }
        } catch (error) {
            addMessage('assistant', `❌ Error: ${error.message}. Check backend connection.`, 'error');
        } finally {
            setIsLoading(false);
        }
    };

    const debugCode = async () => {
        if (!currentProblem || !testResults) {
            addMessage('assistant', '⚠️ Run your code first to see failed tests, then I can help debug!', 'error');
            return;
        }

        setIsLoading(true);
        addMessage('user', '🐛 Help me debug my code', 'action');

        try {
            const response = await fetch(`${API_BASE}/debug`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    problem_title: currentProblem.title,
                    problem_description: currentProblem.description,
                    user_code: userCode,
                    test_input: testResults.failedInput || 'N/A',
                    expected_output: testResults.expected || 'N/A',
                    actual_output: testResults.actual || 'N/A',
                    error_message: testResults.error || null
                })
            });

            const data = await response.json();
            if (data.success) {
                addMessage('assistant', `🐛 **Debug Analysis:**\n\n${data.response}`, 'debug');
            } else {
                addMessage('assistant', '❌ Sorry, I couldn\'t analyze the code. Please try again.', 'error');
            }
        } catch (error) {
            addMessage('assistant', `❌ Error: ${error.message}`, 'error');
        } finally {
            setIsLoading(false);
        }
    };

    const reviewCode = async () => {
        if (!currentProblem || !userCode) {
            addMessage('assistant', '⚠️ Please write some code first, then I can review it!', 'error');
            return;
        }

        setIsLoading(true);
        addMessage('user', '📝 Review my code', 'action');

        try {
            const response = await fetch(`${API_BASE}/review`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    problem_title: currentProblem.title,
                    problem_description: currentProblem.description,
                    user_code: userCode,
                    passed_all_tests: testResults?.percentage === 100,
                    tags: currentProblem.tags || []
                })
            });

            const data = await response.json();
            if (data.success) {
                addMessage('assistant', `📝 **Code Review:**\n\n${data.response}`, 'review');
            } else {
                addMessage('assistant', '❌ Sorry, I couldn\'t review the code. Please try again.', 'error');
            }
        } catch (error) {
            addMessage('assistant', `❌ Error: ${error.message}`, 'error');
        } finally {
            setIsLoading(false);
        }
    };

    const explainSolution = async () => {
        if (!currentProblem) {
            addMessage('assistant', '⚠️ Please select a problem first.', 'error');
            return;
        }

        setIsLoading(true);
        addMessage('user', '📖 Explain the optimal solution', 'action');

        try {
            const response = await fetch(`${API_BASE}/explain`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    problem_title: currentProblem.title,
                    problem_description: currentProblem.description,
                    optimal_solution: currentProblem.solution || null,
                    tags: currentProblem.tags || []
                })
            });

            const data = await response.json();
            if (data.success) {
                addMessage('assistant', `📖 **Solution Explanation:**\n\n${data.response}`, 'explain');
            } else {
                addMessage('assistant', '❌ Sorry, I couldn\'t explain the solution. Please try again.', 'error');
            }
        } catch (error) {
            addMessage('assistant', `❌ Error: ${error.message}`, 'error');
        } finally {
            setIsLoading(false);
        }
    };

    const sendChat = async () => {
        if (!inputValue.trim()) return;

        const userMessage = inputValue.trim();
        setInputValue('');
        addMessage('user', userMessage, 'chat');
        setIsLoading(true);

        try {
            const response = await fetch(`${API_BASE}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: userMessage,
                    problem_context: currentProblem ? {
                        title: currentProblem.title,
                        tags: currentProblem.tags || []
                    } : null,
                    conversation_history: messages
                        .filter(m => m.type === 'chat')
                        .slice(-6)
                        .map(m => ({ role: m.role, content: m.content }))
                })
            });

            const data = await response.json();
            if (data.success) {
                addMessage('assistant', data.response, 'chat');
            } else {
                addMessage('assistant', '❌ Sorry, I couldn\'t respond. Please try again.', 'error');
            }
        } catch (error) {
            addMessage('assistant', `❌ Error: ${error.message}`, 'error');
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendChat();
        }
    };

    const clearChat = () => {
        setMessages([messages[0]]); // Keep welcome message
        setHintLevel(1);
    };

    if (!isOpen) return null;

    return (
        <div className="ai-tutor-panel">
            <div className="ai-tutor-header">
                <div className="header-title">
                    <span className="tutor-icon flex items-center justify-center"><Bot className="w-6 h-6" /></span>
                    <span>AI Coding Tutor</span>
                </div>
                <div className="header-actions">
                    <button onClick={clearChat} className="clear-btn flex items-center justify-center" title="Clear Chat">
                        <Trash2 className="w-5 h-5" />
                    </button>
                    <button onClick={onClose} className="close-btn flex items-center justify-center" title="Close">
                        <X className="w-5 h-5" />
                    </button>
                </div>
            </div>

            <div className="ai-tutor-actions">
                <button
                    onClick={getHint}
                    disabled={isLoading}
                    className="action-btn hint-btn flex items-center justify-center gap-1"
                >
                    <Lightbulb className="w-4 h-4" /> Hint {hintLevel > 1 ? `(L${hintLevel})` : ''}
                </button>
                <button
                    onClick={debugCode}
                    disabled={isLoading}
                    className="action-btn debug-btn flex items-center justify-center gap-1"
                >
                    <Bug className="w-4 h-4" /> Debug
                </button>
                <button
                    onClick={reviewCode}
                    disabled={isLoading}
                    className="action-btn review-btn flex items-center justify-center gap-1"
                >
                    <FileText className="w-4 h-4" /> Review
                </button>
                <button
                    onClick={explainSolution}
                    disabled={isLoading}
                    className="action-btn explain-btn flex items-center justify-center gap-1"
                >
                    <BookOpen className="w-4 h-4" /> Explain
                </button>
            </div>

            <div className="ai-tutor-messages">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`message ${msg.role} ${msg.type}`}
                    >
                        <div className="message-content">
                            {msg.type === 'welcome' ? (
                                <div className="welcome-message space-y-2">
                                    <p className="font-medium mb-2">👋 Hi! I'm your AI Coding Tutor. I can help you with:</p>
                                    <ul className="space-y-1">
                                        <li className="flex items-center gap-2"><Lightbulb className="w-4 h-4 text-yellow-500" /> <span className="font-bold">Hints</span> - Get progressive hints without spoilers</li>
                                        <li className="flex items-center gap-2"><Bug className="w-4 h-4 text-red-500" /> <span className="font-bold">Debug</span> - Understand why your code failed</li>
                                        <li className="flex items-center gap-2"><FileText className="w-4 h-4 text-blue-500" /> <span className="font-bold">Review</span> - Get feedback on your solution</li>
                                        <li className="flex items-center gap-2"><BookOpen className="w-4 h-4 text-purple-500" /> <span className="font-bold">Explain</span> - Learn the optimal approach</li>
                                        <li className="flex items-center gap-2"><Send className="w-4 h-4 text-green-500" /> <span className="font-bold">Ask</span> - Any algorithm questions</li>
                                    </ul>
                                    <p className="mt-2">What would you like help with?</p>
                                </div>
                            ) : (
                                msg.content.split('\n').map((line, i) => (
                                    <React.Fragment key={i}>
                                        {line.startsWith('**') && line.endsWith('**')
                                            ? <strong>{line.slice(2, -2)}</strong>
                                            : line.startsWith('- ')
                                                ? <li>{line.slice(2)}</li>
                                                : line}
                                        {i < msg.content.split('\n').length - 1 && <br />}
                                    </React.Fragment>
                                ))
                            )}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="message assistant loading">
                        <div className="loading-dots">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="ai-tutor-input">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask about algorithms, data structures..."
                    disabled={isLoading}
                />
                <button
                    onClick={sendChat}
                    disabled={isLoading || !inputValue.trim()}
                    className="send-btn flex items-center justify-center"
                >
                    <Send className="w-5 h-5" />
                </button>
            </div>
        </div>
    );
};

export default AITutor;
