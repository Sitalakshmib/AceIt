import React, { useState, useEffect } from 'react';
import { codingAPI } from '../services/api';
import AITutor from '../components/AITutor';
import Editor from '@monaco-editor/react';

const Coding = () => {
  const [code, setCode] = useState(`// Write your solution here
function solveProblem(input) {
  // Your code here
  return input;
}`);
  const [output, setOutput] = useState('');
  const [problems, setProblems] = useState([]);
  const [selectedProblemId, setSelectedProblemId] = useState(null);
  const [selectedTag, setSelectedTag] = useState('All');
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('python');
  const [loading, setLoading] = useState(false);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [error, setError] = useState('');
  const [testResults, setTestResults] = useState(null);
  const [solvedProblems, setSolvedProblems] = useState([]);
  const [hasStarted, setHasStarted] = useState(false);

  const [isTutorOpen, setIsTutorOpen] = useState(false);

  const languages = [
    { id: 'python', name: 'Python', extension: 'py', icon: '🐍' },
    { id: 'r', name: 'R', extension: 'r', icon: '📊' },
    { id: 'java', name: 'Java', extension: 'java', icon: '☕' },
    { id: 'cpp', name: 'C++', extension: 'cpp', icon: '⚡' },
    { id: 'c', name: 'C', extension: 'c', icon: '🔧' },
  ];

  // Map language IDs to Monaco Editor language modes
  const getMonacoLanguage = (langId) => {
    const mapping = {
      'python': 'python',
      'r': 'r',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c'
    };
    return mapping[langId] || 'plaintext';
  };

  // Fetch coding problems and solved status only when user has started
  useEffect(() => {
    if (hasStarted) {
      fetchProblems();
      fetchSolvedProblems();
    }
  }, [hasStarted]);

  const fetchProblems = async () => {
    try {
      console.log('Fetching coding problems from backend...');
      setLoading(true);
      setError('');
      const response = await codingAPI.getProblems();
      console.log('Received problems:', response.data);
      setProblems(response.data);
      if (response.data.length > 0) {
        // Set default problem and code
        const firstProblem = response.data[0];
        setSelectedProblemId(firstProblem.id);
        setCode(firstProblem.starterCode?.python || '# Write your solution here');
      }
    } catch (err) {
      console.error('Failed to fetch problems:', err);
      setError('Failed to fetch problems: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const fetchSolvedProblems = async () => {
    try {
      const response = await codingAPI.getSolvedProblems();
      setSolvedProblems(response.data.solved_problems || []);
    } catch (err) {
      console.error('Failed to fetch solved problems:', err);
    }
  };

  const runCode = async () => {
    if (problems.length === 0) return;

    try {
      setIsRunning(true);
      setOutput('Running code...\n\n');
      setTestResults(null);

      const currentProblem = problems.find(p => p.id === selectedProblemId);
      if (!currentProblem) return;

      const response = await codingAPI.submitCode(currentProblem.id, code, selectedLanguage, 'run');

      // Handle the response from backend
      const { feedback, passed_tests, total_tests, percentage, problem_title, visible_count, hidden_count } = response.data;

      setTestResults({
        passed: passed_tests,
        total: total_tests,
        percentage: percentage,
        problemTitle: problem_title,
        visibleCount: visible_count,
        hiddenCount: hidden_count,
        action: 'run'
      });

      setOutput(feedback || 'Code executed successfully');

    } catch (err) {
      console.error('Failed to run code:', err);
      setOutput('Error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsRunning(false);
    }
  };

  const submitCode = async () => {
    if (problems.length === 0) return;

    try {
      setIsSubmitting(true);
      setOutput('Submitting solution for evaluation...\n\n');
      setTestResults(null);

      const currentProblem = problems.find(p => p.id === selectedProblemId);
      if (!currentProblem) return;

      const response = await codingAPI.submitCode(currentProblem.id, code, selectedLanguage, 'submit');

      // Handle the response from backend
      const { feedback, passed_tests, total_tests, percentage, problem_title, is_solved, total_all_tests } = response.data;

      setTestResults({
        passed: passed_tests,
        total: total_tests,
        totalAllTests: total_all_tests,
        percentage: percentage,
        problemTitle: problem_title,
        action: 'submit',
        isSolved: is_solved
      });

      setOutput(feedback || 'Code executed successfully');

      // Update solved problems list if problem was solved
      if (is_solved && !solvedProblems.includes(currentProblem.id)) {
        setSolvedProblems([...solvedProblems, currentProblem.id]);
      }

    } catch (err) {
      console.error('Failed to submit code:', err);
      setOutput('Error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsSubmitting(false);
    }
  };

  const resetCode = () => {
    const problem = problems.find(p => p.id === selectedProblemId);
    if (problem) {
      setCode(problem.starterCode?.[selectedLanguage] || '// Write your solution here');
    }
    setOutput('');
    setTestResults(null);
  };

  const changeProblem = async (id) => {
    setSelectedProblemId(id);
    const problem = problems.find(p => p.id === id);
    if (!problem) return;

    // Fetch details if description is missing
    if (!problem.description || problem.description === "" || !problem.test_cases) {
      try {
        setDetailsLoading(true);
        const response = await codingAPI.getProblemDetails(id);
        const details = response.data;

        // Update the problem in our list with full details
        setProblems(prev => prev.map(p => p.id === id ? { ...p, ...details } : p));

        // Set code from fetched details
        setCode(details.starterCode?.[selectedLanguage] || '// Write your solution here');
      } catch (err) {
        console.error('Failed to fetch problem details:', err);
      } finally {
        setDetailsLoading(false);
      }
    } else {
      setCode(problem.starterCode?.[selectedLanguage] || '// Write your solution here');
    }

    setOutput('');
    setTestResults(null);
  };

  const changeLanguage = (langId) => {
    setSelectedLanguage(langId);
    const problem = problems.find(p => p.id === selectedProblemId);
    if (problem) {
      setCode(problem.starterCode?.[langId] || '// Write your solution here');
    }
    setOutput('');
    setTestResults(null);
  };

  if (loading) {
    return (
      <div className="p-6 h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-12 text-center border border-gray-100 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-bl-[4rem] opacity-50"></div>
          <div className="relative z-10">
            <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
            <div className="text-xl font-bold text-gray-800">Loading coding problems...</div>
            <p className="text-gray-500 mt-2">Setting up your practice environment</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-12 text-center border border-gray-100 relative overflow-hidden max-w-md">
          <div className="absolute top-0 right-0 w-32 h-32 bg-red-50 rounded-bl-[4rem] opacity-50"></div>
          <div className="relative z-10">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-3xl">⚠️</span>
            </div>
            <div className="text-xl font-bold text-gray-800 mb-2">Oops! Something went wrong</div>
            <div className="text-red-600 mb-6">{error}</div>
            <button
              onClick={fetchProblems}
              className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-blue-700 shadow-lg shadow-blue-200 hover:shadow-blue-300 transition-all transform hover:-translate-y-0.5"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (problems.length === 0) {
    return (
      <div className="p-6 h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-12 text-center border border-gray-100 relative overflow-hidden max-w-md">
          <div className="absolute top-0 right-0 w-32 h-32 bg-gray-100 rounded-bl-[4rem] opacity-50"></div>
          <div className="relative z-10">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-3xl">📝</span>
            </div>
            <div className="text-xl font-bold text-gray-800 mb-2">No Problems Available</div>
            <p className="text-gray-500 mb-6">We couldn't find any coding problems at the moment</p>
            <button
              onClick={fetchProblems}
              className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-blue-700 shadow-lg shadow-blue-200 hover:shadow-blue-300 transition-all transform hover:-translate-y-0.5"
            >
              Refresh
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Welcome Screen - Show before starting practice
  if (!hasStarted) {
    return (
      <div className="p-8 min-h-screen bg-gray-50">
        {/* Header */}
        <div className="mb-10 text-center max-w-7xl mx-auto">
          <div className="inline-block p-4 bg-blue-50 rounded-2xl mb-4">
            <span className="text-4xl font-bold text-blue-600">{ }</span>
          </div>
          <h1 className="text-4xl font-black text-gray-900 mb-2 tracking-tight">Coding Practice</h1>
          <p className="text-lg text-gray-500 max-w-2xl mx-auto">
            Sharpen your programming skills with curated problems. Write, test, and submit solutions in multiple languages.
          </p>
        </div>

        {/* Welcome Content */}
        <div className="max-w-5xl mx-auto">
          <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-12 border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-bl-full opacity-50"></div>

            <div className="relative z-10">
              <h2 className="text-3xl font-black text-gray-900 mb-4 text-center">Ready to Code?</h2>
              <p className="text-gray-600 text-center mb-12 text-lg">
                Choose how you'd like to practice today
              </p>

              {/* Main Action - Start Coding Practice */}
              <div className="mb-8">
                <button
                  onClick={() => setHasStarted(true)}
                  className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-6 rounded-2xl font-bold text-xl hover:from-blue-700 hover:to-indigo-700 shadow-xl shadow-blue-200 hover:shadow-blue-300 transition-all transform hover:-translate-y-1 flex items-center justify-center gap-3"
                >
                  <span className="text-2xl">▶</span>
                  Start Coding Practice
                </button>
              </div>

              {/* Category Selection Options */}
              <div className="border-t border-gray-200 pt-8">
                <h3 className="text-lg font-bold text-gray-700 mb-6 text-center">Or Browse by Category</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Arrays Category */}
                  <button
                    onClick={() => {
                      setHasStarted(true);
                      setSelectedTag('Arrays');
                    }}
                    className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 hover:border-green-400 p-6 rounded-2xl transition-all transform hover:-translate-y-1 hover:shadow-lg group"
                  >
                    <div className="text-3xl mb-3 font-bold text-green-600">[ ]</div>
                    <div className="font-bold text-gray-800 mb-1">Arrays</div>
                    <div className="text-sm text-gray-600">Master array manipulation</div>
                  </button>

                  {/* Strings Category */}
                  <button
                    onClick={() => {
                      setHasStarted(true);
                      setSelectedTag('Strings');
                    }}
                    className="bg-gradient-to-br from-purple-50 to-violet-50 border-2 border-purple-200 hover:border-purple-400 p-6 rounded-2xl transition-all transform hover:-translate-y-1 hover:shadow-lg group"
                  >
                    <div className="text-3xl mb-3 font-bold text-purple-600">" "</div>
                    <div className="font-bold text-gray-800 mb-1">Strings</div>
                    <div className="text-sm text-gray-600">Text processing challenges</div>
                  </button>

                  {/* Algorithms Category */}
                  <button
                    onClick={() => {
                      setHasStarted(true);
                      setSelectedTag('Algorithms');
                    }}
                    className="bg-gradient-to-br from-orange-50 to-amber-50 border-2 border-orange-200 hover:border-orange-400 p-6 rounded-2xl transition-all transform hover:-translate-y-1 hover:shadow-lg group"
                  >
                    <div className="text-3xl mb-3 font-bold text-orange-600">∑</div>
                    <div className="font-bold text-gray-800 mb-1">Algorithms</div>
                    <div className="text-sm text-gray-600">Problem-solving techniques</div>
                  </button>

                  {/* Data Structures Category */}
                  <button
                    onClick={() => {
                      setHasStarted(true);
                      setSelectedTag('Data Structures');
                    }}
                    className="bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-200 hover:border-blue-400 p-6 rounded-2xl transition-all transform hover:-translate-y-1 hover:shadow-lg group"
                  >
                    <div className="text-3xl mb-3 font-bold text-blue-600">⊕</div>
                    <div className="font-bold text-gray-800 mb-1">Data Structures</div>
                    <div className="text-sm text-gray-600">Trees, graphs, and more</div>
                  </button>

                  {/* Dynamic Programming Category */}
                  <button
                    onClick={() => {
                      setHasStarted(true);
                      setSelectedTag('Dynamic Programming');
                    }}
                    className="bg-gradient-to-br from-pink-50 to-rose-50 border-2 border-pink-200 hover:border-pink-400 p-6 rounded-2xl transition-all transform hover:-translate-y-1 hover:shadow-lg group"
                  >
                    <div className="text-3xl mb-3 font-bold text-pink-600">ƒ(n)</div>
                    <div className="font-bold text-gray-800 mb-1">Dynamic Programming</div>
                    <div className="text-sm text-gray-600">Optimization problems</div>
                  </button>

                  {/* All Problems */}
                  <button
                    onClick={() => {
                      setHasStarted(true);
                      setSelectedTag('All');
                    }}
                    className="bg-gradient-to-br from-gray-50 to-slate-50 border-2 border-gray-200 hover:border-gray-400 p-6 rounded-2xl transition-all transform hover:-translate-y-1 hover:shadow-lg group"
                  >
                    <div className="text-3xl mb-3 font-bold text-gray-600">∀</div>
                    <div className="font-bold text-gray-800 mb-1">All Problems</div>
                    <div className="text-sm text-gray-600">Browse everything</div>
                  </button>
                </div>
              </div>

              {/* Additional Info */}
              <div className="mt-10 pt-8 border-t border-gray-200">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
                  <div>
                    <div className="text-2xl mb-2 font-bold text-blue-600">&lt;/&gt;</div>
                    <div className="font-bold text-gray-800 text-sm">Multiple Languages</div>
                    <div className="text-xs text-gray-500">Python, Java, C++, C, R</div>
                  </div>
                  <div>
                    <div className="text-2xl mb-2 font-bold text-purple-600">AI</div>
                    <div className="font-bold text-gray-800 text-sm">AI Tutor</div>
                    <div className="text-xs text-gray-500">Get hints when stuck</div>
                  </div>
                  <div>
                    <div className="text-2xl mb-2 font-bold text-green-600">✓</div>
                    <div className="font-bold text-gray-800 text-sm">Auto-Grading</div>
                    <div className="text-xs text-gray-500">Instant feedback</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Get all unique tags from problems
  const allTags = ['All', ...new Set(problems.flatMap(p => p.tags || []))];

  // Filter problems by selected tag
  const filteredProblems = selectedTag === 'All'
    ? problems
    : problems.filter(p => p.tags && p.tags.includes(selectedTag));

  const problem = problems.find(p => p.id === selectedProblemId) || problems[0];

  return (
    <div className="p-8 min-h-screen bg-gray-50">
      {/* Header */}
      <div className="mb-10 text-center max-w-7xl mx-auto">
        <div className="inline-block p-4 bg-blue-50 rounded-2xl mb-4">
          <span className="text-4xl font-bold text-blue-600">{ }</span>
        </div>
        <h1 className="text-4xl font-black text-gray-900 mb-2 tracking-tight">Coding Practice</h1>
        <p className="text-lg text-gray-500 max-w-2xl mx-auto">
          Sharpen your programming skills with curated problems. Write, test, and submit solutions in multiple languages.
        </p>
      </div>

      <div className="flex flex-1 gap-6 items-start max-w-7xl mx-auto">
        {/* Problem List Sidebar */}
        <div className="w-1/4 flex flex-col h-[calc(100vh-12rem)] sticky top-6">
          <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-6 flex flex-col h-full border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-24 h-24 bg-blue-50 rounded-bl-[3rem] opacity-40"></div>
            <div className="flex justify-between items-center mb-6 relative z-10">
              <h2 className="text-xl font-bold text-gray-800">Problems</h2>
              <div className="flex items-center gap-3">
                <div className="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full">
                  ✓ {solvedProblems.length} Solved
                </div>
                <div className="text-xs text-gray-500">{filteredProblems.length} available</div>
              </div>
            </div>

            {/* Tags / Topics Filter */}
            <div className="flex flex-wrap gap-2 mb-6 overflow-x-auto pb-2 scrollbar-hide relative z-10" style={{ maxHeight: '100px' }}>
              {allTags.map(tag => (
                <button
                  key={tag}
                  onClick={() => setSelectedTag(tag)}
                  className={`px-3 py-1.5 rounded-full text-xs font-bold transition-all whitespace-nowrap ${selectedTag === tag
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                >
                  {tag}
                </button>
              ))}
            </div>

            <div className="space-y-3 flex-1 overflow-y-auto pr-1 overscroll-y-contain scrollbar-thin scrollbar-thumb-gray-200 scrollbar-track-transparent relative z-10">
              {filteredProblems.map((prob) => (
                <div
                  key={prob.id}
                  onClick={() => changeProblem(prob.id)}
                  className={`p-4 rounded-xl cursor-pointer transition-all border-2 relative ${selectedProblemId === prob.id
                    ? 'bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-500 shadow-md'
                    : 'bg-white hover:bg-gray-50 border-gray-100 shadow-sm hover:shadow-md'
                    }`}
                >
                  {/* Solved indicator */}
                  {solvedProblems.includes(prob.id) && (
                    <div className="absolute top-3 right-3">
                      <span className="text-green-600 text-xl" title="Solved">✓</span>
                    </div>
                  )}
                  <div className="flex justify-between items-start mb-2 pr-8">
                    <h3 className="font-bold text-gray-800 text-sm line-clamp-1">{prob.title}</h3>
                    <span className={`text-[10px] px-2.5 py-1 rounded-full font-bold uppercase ${prob.difficulty === 'Easy' ? 'bg-green-100 text-green-700' :
                      prob.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-red-100 text-red-700'
                      }`}>
                      {prob.difficulty}
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {prob.tags && prob.tags.slice(0, 2).map((tag, idx) => (
                      <span key={idx} className="text-[10px] text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full border border-blue-100 font-medium">
                        {tag}
                      </span>
                    ))}
                    {prob.tags && prob.tags.length > 2 && (
                      <span className="text-[10px] text-gray-500 font-medium">+{prob.tags.length - 2}</span>
                    )}
                  </div>
                </div>
              ))}
              {filteredProblems.length === 0 && (
                <div className="text-center py-10 text-gray-500 italic">
                  No problems found for this topic.
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Main Coding Area */}
        <div className="flex-1 flex flex-col min-w-0">
          <div className="flex flex-col gap-6">
            {/* Problem Statement */}
            <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-8 border border-gray-100 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-bl-full opacity-50"></div>
              {detailsLoading ? (
                <div className="h-full flex flex-col items-center justify-center space-y-4 py-20">
                  <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                  <p className="text-gray-500 font-semibold">Fetching problem details...</p>
                </div>
              ) : (
                <div className="relative z-10">
                  <div className="flex justify-between items-start mb-6">
                    <h2 className="text-3xl font-black text-gray-900">{problem.title}</h2>
                    <div className="flex gap-2">
                      <span className={`text-xs px-3 py-1.5 rounded-full font-bold uppercase ${problem.difficulty === 'Easy' ? 'bg-green-100 text-green-700' :
                        problem.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-red-100 text-red-700'
                        }`}>
                        {problem.difficulty}
                      </span>
                      <span className="text-xs px-3 py-1.5 bg-gray-100 text-gray-600 rounded-full font-bold">
                        {problem.source || 'Premium'}
                      </span>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2 mb-8">
                    {problem.tags && problem.tags.map((tag, idx) => (
                      <span key={idx} className="text-xs text-blue-600 bg-blue-50 px-3 py-1.5 rounded-full border border-blue-100 font-bold">
                        {tag}
                      </span>
                    ))}
                  </div>

                  <div
                    className="text-gray-700 mb-8 prose prose-blue max-w-none leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: problem.description || "No description available." }}
                  />

                  {problem.examples && problem.examples.length > 0 && (
                    <div className="mt-8 border-t pt-8">
                      <h4 className="text-xl font-bold mb-6 text-gray-800">Examples</h4>
                      <div className="space-y-4">
                        {problem.examples.map((example, idx) => (
                          <div key={idx} className="bg-gradient-to-br from-gray-50 to-blue-50 p-5 rounded-2xl border border-gray-100">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                              <div>
                                <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-2">Input</span>
                                <pre className="text-sm font-mono text-gray-800 bg-white p-3 rounded-xl border border-gray-200 overflow-x-auto">
                                  {typeof example.input === 'object' ? JSON.stringify(example.input) : example.input}
                                </pre>
                              </div>
                              <div>
                                <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-2">Output</span>
                                <pre className="text-sm font-mono text-gray-800 bg-white p-3 rounded-xl border border-gray-200 overflow-x-auto">
                                  {typeof example.output === 'object' ? JSON.stringify(example.output) : example.output}
                                </pre>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Code Editor Header with Language Selector */}
            <div className="bg-gray-900 rounded-[2rem] shadow-xl mb-4 flex flex-col h-[600px] shrink-0 overflow-hidden">
              <div className="flex justify-between items-center p-4 bg-gray-800">
                <div className="flex items-center space-x-4">
                  <span className="text-white font-mono text-sm">
                    solution.{languages.find(lang => lang.id === selectedLanguage)?.extension}
                  </span>

                  {/* Language Selector */}
                  <div className="flex space-x-1 bg-gray-700 rounded-xl p-1.5">
                    {languages.map(lang => (
                      <button
                        key={lang.id}
                        onClick={() => changeLanguage(lang.id)}
                        className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${selectedLanguage === lang.id
                          ? 'bg-blue-600 text-white shadow-md'
                          : 'text-gray-300 hover:text-white hover:bg-gray-600'
                          }`}
                      >
                        <span className="mr-1.5">{lang.icon}</span>
                        {lang.name}
                      </button>
                    ))}
                  </div>
                </div>

                <button
                  onClick={resetCode}
                  className="bg-gray-600 text-white px-4 py-2 rounded-xl text-sm font-bold hover:bg-gray-700 transition-all shadow-md"
                >
                  Reset Code
                </button>
              </div>

              <Editor
                height="100%"
                language={getMonacoLanguage(selectedLanguage)}
                value={code}
                onChange={(value) => setCode(value || '')}
                theme="vs-dark"
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  lineNumbers: 'on',
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                  tabSize: 2,
                  wordWrap: 'on',
                  padding: { top: 10, bottom: 10 },
                }}
              />
            </div>

            {/* Output & Controls */}
            <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 border border-gray-100 overflow-hidden">
              <div className="flex justify-between items-center p-5 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
                <div>
                  <h3 className="font-bold text-gray-900 text-lg">Output</h3>
                  <span className="text-sm text-gray-500 font-medium">
                    Language: {languages.find(lang => lang.id === selectedLanguage)?.name}
                  </span>
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={runCode}
                    disabled={isRunning || isSubmitting}
                    className="bg-gradient-to-r from-gray-700 to-gray-800 text-white px-6 py-2.5 rounded-xl hover:from-gray-800 hover:to-gray-900 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 font-bold shadow-md hover:shadow-lg transition-all transform hover:-translate-y-0.5"
                  >
                    {isRunning ? '▶ Running...' : '▶ Run Code'}
                  </button>
                  <button
                    onClick={submitCode}
                    disabled={isRunning || isSubmitting}
                    className="bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-2.5 rounded-xl hover:from-green-700 hover:to-green-800 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 font-bold shadow-lg shadow-green-200 hover:shadow-green-300 transition-all transform hover:-translate-y-0.5"
                  >
                    {isSubmitting ? '📤 Submitting...' : '📤 Submit'}
                  </button>
                </div>
              </div>

              {/* Test Results Bar */}
              {testResults && (
                <div className="p-5 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-100">
                  <div className="flex justify-between items-center mb-3">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-gray-800">Test Results:</span>
                      {testResults.action === 'run' && testResults.hiddenCount > 0 && (
                        <span className="text-xs text-gray-500 bg-white px-2 py-1 rounded-full">({testResults.visibleCount} visible, {testResults.hiddenCount} hidden)</span>
                      )}
                      {testResults.isSolved && (
                        <span className="text-green-600 font-bold text-sm bg-green-100 px-3 py-1 rounded-full">✓ Solved!</span>
                      )}
                    </div>
                    <span className={`font-bold text-lg ${testResults.passed === testResults.total ? 'text-green-600' : 'text-red-600'
                      }`}>
                      {testResults.passed}/{testResults.total} passed ({testResults.percentage}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${testResults.percentage >= 80 ? 'bg-gradient-to-r from-green-500 to-green-600' :
                        testResults.percentage >= 60 ? 'bg-gradient-to-r from-yellow-500 to-yellow-600' : 'bg-gradient-to-r from-red-500 to-red-600'
                        }`}
                      style={{ width: `${testResults.percentage}%` }}
                    ></div>
                  </div>
                </div>
              )}

              <pre className="p-6 bg-gray-50 text-sm min-h-[120px] max-h-60 overflow-y-auto whitespace-pre-wrap font-mono text-gray-700">
                {output || "Click 'Run Code' to test your solution..."}
              </pre>
            </div>
          </div>
        </div>
      </div>

      {/* AI Tutor Toggle Button */}
      <button
        className={`ai-tutor-toggle ${isTutorOpen ? 'active' : ''}`}
        onClick={() => setIsTutorOpen(!isTutorOpen)}
        title="AI Tutor"
        style={{
          position: 'fixed',
          right: isTutorOpen ? '400px' : '20px',
          bottom: '20px',
          width: '64px',
          height: '64px',
          border: 'none',
          borderRadius: '50%',
          background: isTutorOpen
            ? 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)'
            : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: '#fff',
          fontSize: '32px',
          cursor: 'pointer',
          boxShadow: isTutorOpen
            ? '0 8px 24px rgba(231, 76, 60, 0.4)'
            : '0 8px 24px rgba(102, 126, 234, 0.4)',
          transition: 'all 0.3s ease',
          zIndex: 999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transform: isTutorOpen ? 'scale(1.05)' : 'scale(1)',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.1)';
          e.currentTarget.style.boxShadow = isTutorOpen
            ? '0 12px 32px rgba(231, 76, 60, 0.5)'
            : '0 12px 32px rgba(102, 126, 234, 0.5)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = isTutorOpen ? 'scale(1.05)' : 'scale(1)';
          e.currentTarget.style.boxShadow = isTutorOpen
            ? '0 8px 24px rgba(231, 76, 60, 0.4)'
            : '0 8px 24px rgba(102, 126, 234, 0.4)';
        }}
      >
        {isTutorOpen ? '✕' : '🤖'}
      </button>

      {/* AI Tutor Panel */}
      <AITutor
        isOpen={isTutorOpen}
        onClose={() => setIsTutorOpen(false)}
        currentProblem={problems.find(p => p.id === selectedProblemId)}
        userCode={code}
        testResults={testResults}
      />
    </div >
  );
};

export default Coding;