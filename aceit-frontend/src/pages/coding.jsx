import React, { useState, useEffect } from 'react';
import { codingAPI } from '../services/api';

const Coding = () => {
  const [code, setCode] = useState(`// Write your solution here
function solveProblem(input) {
  // Your code here
  return input;
}`);
  const [output, setOutput] = useState('');
  const [problems, setProblems] = useState([]);
  const [selectedProblem, setSelectedProblem] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('python');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [testResults, setTestResults] = useState(null);

  const languages = [
    { id: 'python', name: 'Python', extension: 'py', icon: '🐍' },
    { id: 'javascript', name: 'JavaScript', extension: 'js', icon: '🟨' },
    { id: 'java', name: 'Java', extension: 'java', icon: '☕' },
    { id: 'cpp', name: 'C++', extension: 'cpp', icon: '⚡' },
  ];

  // Fetch coding problems on component mount
  useEffect(() => {
    fetchProblems();
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
        // Set default code based on first problem (Python)
        setCode(response.data[0].starterCode?.python || '# Write your solution here');
      }
    } catch (err) {
      console.error('Failed to fetch problems:', err);
      setError('Failed to fetch problems: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const runCode = async () => {
    if (problems.length === 0) return;

    try {
      setIsRunning(true);
      setOutput('Running code...\n\n');
      setTestResults(null);

      const currentProblem = problems[selectedProblem];
      const response = await codingAPI.submitCode(currentProblem.id, code, selectedLanguage);

      // Handle the response from backend
      const { feedback, passed_tests, total_tests, percentage, problem_title } = response.data;

      setTestResults({
        passed: passed_tests,
        total: total_tests,
        percentage: percentage,
        problemTitle: problem_title
      });

      setOutput(feedback || 'Code executed successfully');

      // Show success message if tests passed
      if (passed_tests === total_tests && total_tests > 0) {
        setTimeout(() => {
          setOutput(prev => prev + '\n\n🎉 All tests passed! Progress saved.');
        }, 500);
      }

    } catch (err) {
      console.error('Failed to run code:', err);
      setOutput('Error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsRunning(false);
    }
  };

  const resetCode = () => {
    if (problems.length > 0) {
      const problem = problems[selectedProblem];
      setCode(problem.starterCode?.[selectedLanguage] || '// Write your solution here');
    }
    setOutput('');
    setTestResults(null);
  };

  const changeProblem = (index) => {
    setSelectedProblem(index);
    if (problems.length > 0) {
      const problem = problems[index];
      setCode(problem.starterCode?.[selectedLanguage] || '// Write your solution here');
    }
    setOutput('');
    setTestResults(null);
  };

  const changeLanguage = (langId) => {
    setSelectedLanguage(langId);
    if (problems.length > 0) {
      const problem = problems[selectedProblem];
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

  const problem = problems[selectedProblem];

  return (
    <div className="p-6 h-screen flex flex-col bg-gray-50">
      <h1 className="text-2xl font-bold mb-4 text-gray-800">Coding Practice</h1>

      <div className="flex flex-1 gap-6 min-h-0">
        {/* Problem List Sidebar */}
        <div className="w-1/3 bg-white rounded-lg shadow-md p-4 flex flex-col">
          <h2 className="text-lg font-semibold mb-4 text-gray-800">Problems</h2>
          <div className="space-y-2 flex-1 overflow-y-auto">
            {problems.map((prob, index) => (
              <div
                key={prob.id}
                onClick={() => changeProblem(index)}
                className={`p-3 rounded-lg cursor-pointer transition-all ${selectedProblem === index
                  ? 'bg-blue-100 border-blue-500 border-2'
                  : 'bg-gray-50 hover:bg-gray-100 border border-transparent'
                  }`}
              >
                <div className="flex justify-between items-start">
                  <h3 className="font-medium text-gray-800">{prob.title}</h3>
                  <span className={`text-xs px-2 py-1 rounded-full ${prob.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                    prob.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                    {prob.difficulty}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mt-1 line-clamp-2">{prob.title}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Main Coding Area */}
        <div className="flex-1 flex flex-col min-h-0">
          {/* Problem Statement */}
          <div className="bg-white rounded-lg shadow-md p-4 mb-4 flex-1 overflow-y-auto">
            <h2 className="text-xl font-semibold mb-2 text-gray-800">{problem.title}</h2>
            <div
              className="text-gray-700 mb-4 prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: problem.description }}
            />

            {problem.examples && problem.examples.length > 0 && (
              <div className="mb-4">
                <h4 className="font-semibold mb-2 text-gray-800">Examples:</h4>
                {problem.examples.map((example, idx) => (
                  <div key={idx} className="bg-gray-50 p-3 rounded mb-2">
                    <div className="text-sm">
                      <span className="font-medium">Input:</span> {example.input}
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Output:</span> {example.output}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Code Editor Header with Language Selector */}
          <div className="bg-gray-900 rounded-lg shadow-md mb-4 flex-1 flex flex-col">
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

            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="flex-1 w-full font-mono text-sm p-4 text-white bg-gray-900 focus:outline-none resize-none"
              spellCheck="false"
              style={{ minHeight: '200px' }}
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
              <button
                onClick={runCode}
                disabled={isRunning}
                className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isRunning ? 'Running...' : 'Run Code'}
              </button>
            </div>

            {/* Test Results Bar */}
            {testResults && (
              <div className="p-3 bg-gray-50 border-b">
                <div className="flex justify-between items-center mb-1">
                  <span className="font-medium">Test Results:</span>
                  <span className={`font-bold ${testResults.passed === testResults.total ? 'text-green-600' : 'text-red-600'
                    }`}>
                    {testResults.passed}/{testResults.total} passed ({testResults.percentage}%)
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${testResults.percentage >= 80 ? 'bg-green-600' :
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
  );
};

export default Coding;