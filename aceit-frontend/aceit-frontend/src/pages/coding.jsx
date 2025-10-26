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
  const [selectedLanguage, setSelectedLanguage] = useState('javascript');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const languages = [
    { id: 'javascript', name: 'JavaScript', extension: 'js', icon: 'JS' },
    { id: 'python', name: 'Python', extension: 'py', icon: 'PY' },
    { id: 'java', name: 'Java', extension: 'java', icon: 'J' },
    { id: 'cpp', name: 'C++', extension: 'cpp', icon: 'C++' },
  ];

  // Fetch coding problems on component mount
  useEffect(() => {
    fetchProblems();
  }, []);

  const fetchProblems = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await codingAPI.getProblems();
      setProblems(response.data);
      if (response.data.length > 0) {
        // Set default code based on first problem
        setCode(response.data[0].starterCode?.javascript || '// Write your solution here');
      }
    } catch (err) {
      setError('Failed to fetch problems: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const runCode = async () => {
    if (problems.length === 0) return;
    
    try {
      setIsRunning(true);
      setOutput('Running code...');
      
      const currentProblem = problems[selectedProblem];
      const response = await codingAPI.submitCode(currentProblem.id, code);
      
      setOutput(response.data.output || 'Code executed successfully');
    } catch (err) {
      setOutput('Error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsRunning(false);
    }
  };

  const handleProblemChange = (index) => {
    setSelectedProblem(index);
    if (problems[index]) {
      setCode(problems[index].starterCode?.javascript || '// Write your solution here');
    }
  };

  if (loading) {
    return (
      <div className="p-6 max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="text-xl">Loading coding problems...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 max-w-6xl mx-auto">
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

  const currentProblem = problems[selectedProblem] || {};

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Problem List */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Coding Problems</h2>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {problems.map((problem, index) => (
                <div
                  key={problem.id}
                  onClick={() => handleProblemChange(index)}
                  className={`p-4 rounded-lg border cursor-pointer transition-all ${
                    selectedProblem === index
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <h3 className="font-medium">{problem.title}</h3>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      problem.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                      problem.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {problem.difficulty}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                    {problem.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Code Editor and Output */}
        <div className="lg:col-span-2 space-y-6">
          {/* Problem Description */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-xl font-semibold">{currentProblem.title}</h2>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                currentProblem.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                currentProblem.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {currentProblem.difficulty}
              </span>
            </div>
            <p className="text-gray-700 mb-6">{currentProblem.description}</p>
            
            {currentProblem.examples && currentProblem.examples.length > 0 && (
              <div className="mb-6">
                <h3 className="font-medium mb-2">Examples:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {currentProblem.examples.map((example, index) => (
                    <div key={index} className="bg-gray-50 p-3 rounded">
                      <div className="text-sm">
                        <div className="font-medium">Input:</div>
                        <div className="font-mono bg-white p-2 rounded mb-2">{example.input}</div>
                        <div className="font-medium">Output:</div>
                        <div className="font-mono bg-white p-2 rounded">{example.output}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Code Editor */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="flex justify-between items-center p-4 border-b">
              <div className="flex gap-2">
                {languages.map((lang) => (
                  <button
                    key={lang.id}
                    onClick={() => setSelectedLanguage(lang.id)}
                    className={`px-3 py-1 rounded text-sm ${
                      selectedLanguage === lang.id
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 hover:bg-gray-200'
                    }`}
                  >
                    {lang.icon} {lang.name}
                  </button>
                ))}
              </div>
              <button
                onClick={runCode}
                disabled={isRunning}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isRunning ? 'Running...' : 'Run Code'}
              </button>
            </div>
            <div className="p-4">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full h-64 font-mono text-sm p-4 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Write your code here..."
              />
            </div>
          </div>

          {/* Output */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="font-medium mb-2">Output:</h3>
            <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm min-h-32">
              {output || 'Run your code to see the output'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Coding;