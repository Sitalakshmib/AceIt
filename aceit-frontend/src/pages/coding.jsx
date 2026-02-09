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

  // Fetch coding problems and solved status on component mount
  useEffect(() => {
    fetchProblems();
    fetchSolvedProblems();
  }, []);

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
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="text-xl">Loading coding problems...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="text-xl text-red-600">Error: {error}</div>
          <button
            onClick={fetchProblems}
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (problems.length === 0) {
    return (
      <div className="p-6 h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="text-xl">No coding problems available</div>
          <button
            onClick={fetchProblems}
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
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
    <div className="p-6 min-h-screen flex flex-col bg-gray-50">
      <h1 className="text-2xl font-bold mb-4 text-gray-800">Coding Practice</h1>



      <div className="flex flex-1 gap-4 items-start">
        {/* Problem List Sidebar */}
        <div className="w-1/4 flex flex-col h-[calc(100vh-3rem)] sticky top-6">
          <div className="bg-white rounded-l-lg shadow-md p-4 flex flex-col h-full">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-800">Problems</h2>
              <div className="flex items-center gap-3">
                <div className="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full">
                  ✓ {solvedProblems.length} Solved
                </div>
                <div className="text-xs text-gray-500">{filteredProblems.length} available</div>
              </div>
            </div>

            {/* Tags / Topics Filter */}
            <div className="flex flex-wrap gap-2 mb-4 overflow-x-auto pb-2 scrollbar-hide" style={{ maxHeight: '100px' }}>
              {allTags.map(tag => (
                <button
                  key={tag}
                  onClick={() => setSelectedTag(tag)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-all whitespace-nowrap ${selectedTag === tag
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                >
                  {tag}
                </button>
              ))}
            </div>

            <div className="space-y-2 flex-1 overflow-y-auto pr-1 overscroll-y-contain scrollbar-thin scrollbar-thumb-gray-200 scrollbar-track-transparent">
              {filteredProblems.map((prob) => (
                <div
                  key={prob.id}
                  onClick={() => changeProblem(prob.id)}
                  className={`p-3 rounded-lg cursor-pointer transition-all border-2 relative ${selectedProblemId === prob.id
                    ? 'bg-blue-50 border-blue-500'
                    : 'bg-white hover:bg-gray-50 border-gray-100 shadow-sm'
                    }`}
                >
                  {/* Solved indicator */}
                  {solvedProblems.includes(prob.id) && (
                    <div className="absolute top-2 right-2">
                      <span className="text-green-600 text-lg" title="Solved">✓</span>
                    </div>
                  )}
                  <div className="flex justify-between items-start mb-1 pr-6">
                    <h3 className="font-medium text-gray-800 text-sm line-clamp-1">{prob.title}</h3>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${prob.difficulty === 'Easy' ? 'bg-green-100 text-green-700' :
                      prob.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-red-100 text-red-700'
                      }`}>
                      {prob.difficulty}
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {prob.tags && prob.tags.slice(0, 2).map((tag, idx) => (
                      <span key={idx} className="text-[10px] text-gray-400 bg-gray-50 px-1.5 py-0.5 rounded border border-gray-100">
                        {tag}
                      </span>
                    ))}
                    {prob.tags && prob.tags.length > 2 && (
                      <span className="text-[10px] text-gray-400">+{prob.tags.length - 2}</span>
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
          <div className="flex flex-col gap-6 ml-6">
            {/* Problem Statement */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-4 h-auto border border-gray-100">
              {detailsLoading ? (
                <div className="h-full flex flex-col items-center justify-center space-y-4">
                  <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                  <p className="text-gray-500 font-medium">Fetching problem details...</p>
                </div>
              ) : (
                <>
                  <div className="flex justify-between items-start mb-4">
                    <h2 className="text-2xl font-bold text-gray-800">{problem.title}</h2>
                    <div className="flex gap-2">
                      <span className={`text-xs px-2 py-1 rounded-full font-bold uppercase ${problem.difficulty === 'Easy' ? 'bg-green-100 text-green-700' :
                        problem.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-red-100 text-red-700'
                        }`}>
                        {problem.difficulty}
                      </span>
                      <span className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded-full font-medium">
                        {problem.source || 'Premium'}
                      </span>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2 mb-6">
                    {problem.tags && problem.tags.map((tag, idx) => (
                      <span key={idx} className="text-xs text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-100 font-medium">
                        {tag}
                      </span>
                    ))}
                  </div>

                  <div
                    className="text-gray-700 mb-8 prose prose-blue max-w-none leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: problem.description || "No description available." }}
                  />

                  {problem.examples && problem.examples.length > 0 && (
                    <div className="mt-8 border-t pt-6">
                      <h4 className="text-lg font-semibold mb-4 text-gray-800">Examples</h4>
                      <div className="space-y-4">
                        {problem.examples.map((example, idx) => (
                          <div key={idx} className="bg-gray-50 p-4 rounded-xl border border-gray-100">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                              <div>
                                <span className="text-xs font-bold text-gray-400 uppercase tracking-wider block mb-1">Input</span>
                                <pre className="text-sm font-mono text-gray-800 bg-white p-2 rounded border border-gray-200 overflow-x-auto">
                                  {typeof example.input === 'object' ? JSON.stringify(example.input) : example.input}
                                </pre>
                              </div>
                              <div>
                                <span className="text-xs font-bold text-gray-400 uppercase tracking-wider block mb-1">Output</span>
                                <pre className="text-sm font-mono text-gray-800 bg-white p-2 rounded border border-gray-200 overflow-x-auto">
                                  {typeof example.output === 'object' ? JSON.stringify(example.output) : example.output}
                                </pre>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>

            {/* Code Editor Header with Language Selector */}
            <div className="bg-gray-900 rounded-lg shadow-md mb-4 flex flex-col h-[600px] shrink-0">
              <div className="flex justify-between items-center p-3 bg-gray-800 rounded-t-lg">
                <div className="flex items-center space-x-4">
                  <span className="text-white font-mono text-sm">
                    solution.{languages.find(lang => lang.id === selectedLanguage)?.extension}
                  </span>

                  {/* Language Selector */}
                  <div className="flex space-x-1 bg-gray-700 rounded-lg p-1">
                    {languages.map(lang => (
                      <button
                        key={lang.id}
                        onClick={() => changeLanguage(lang.id)}
                        className={`px-3 py-1 rounded-md text-sm font-medium transition-all ${selectedLanguage === lang.id
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-300 hover:text-white hover:bg-gray-600'
                          }`}
                      >
                        <span className="mr-1">{lang.icon}</span>
                        {lang.name}
                      </button>
                    ))}
                  </div>
                </div>

                <button
                  onClick={resetCode}
                  className="bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700"
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
            <div className="bg-white rounded-lg shadow-md">
              <div className="flex justify-between items-center p-3 border-b">
                <div>
                  <h3 className="font-semibold text-gray-800">Output</h3>
                  <span className="text-sm text-gray-500">
                    Language: {languages.find(lang => lang.id === selectedLanguage)?.name}
                  </span>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={runCode}
                    disabled={isRunning || isSubmitting}
                    className="bg-gray-700 text-white px-4 py-2 rounded-md hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                  >
                    {isRunning ? '▶ Running...' : '▶ Run Code'}
                  </button>
                  <button
                    onClick={submitCode}
                    disabled={isRunning || isSubmitting}
                    className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 font-semibold"
                  >
                    {isSubmitting ? '📤 Submitting...' : '📤 Submit'}
                  </button>
                </div>
              </div>

              {/* Test Results Bar */}
              {testResults && (
                <div className="p-3 bg-gray-50 border-b">
                  <div className="flex justify-between items-center mb-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium">Test Results:</span>
                      {testResults.action === 'run' && testResults.hiddenCount > 0 && (
                        <span className="text-xs text-gray-500">({testResults.visibleCount} visible, {testResults.hiddenCount} hidden)</span>
                      )}
                      {testResults.isSolved && (
                        <span className="text-green-600 font-bold text-sm">✓ Solved!</span>
                      )}
                    </div>
                    <span className={`font-bold ${testResults.passed === testResults.total ? 'text-green-600' : 'text-red-600'
                      }`}>
                      {testResults.passed}/{testResults.total} passed ({testResults.percentage}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all ${testResults.percentage >= 80 ? 'bg-green-600' :
                        testResults.percentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                      style={{ width: `${testResults.percentage}%` }}
                    ></div>
                  </div>
                </div>
              )}

              <pre className="p-4 bg-gray-50 text-sm min-h-[120px] max-h-60 overflow-y-auto whitespace-pre-wrap font-mono">
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
          width: '60px',
          height: '60px',
          border: 'none',
          borderRadius: '50%',
          background: isTutorOpen
            ? 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)'
            : 'linear-gradient(135deg, #8a2be2 0%, #667eea 100%)',
          color: '#fff',
          fontSize: '28px',
          cursor: 'pointer',
          boxShadow: '0 4px 20px rgba(138, 43, 226, 0.5)',
          transition: 'all 0.3s',
          zIndex: 999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
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