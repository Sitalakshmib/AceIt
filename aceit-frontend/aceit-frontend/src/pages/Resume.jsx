import React, { useState } from 'react';

const Resume = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [jobRole, setJobRole] = useState('Software Developer');

  const jobRoles = [
    'Software Developer',
    'Frontend Developer', 
    'Backend Developer',
    'Full Stack Developer',
    'Data Scientist',
    'Machine Learning Engineer',
    'DevOps Engineer',
    'Product Manager'
  ];

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type === 'application/pdf' || file.type.includes('word') || file.type === 'text/plain') {
        setResumeFile(file);
        setAnalysisResult(null);
      } else {
        alert('Please upload a PDF, Word document, or text file.');
      }
    }
  };

  const analyzeResume = () => {
    if (!resumeFile) {
      alert('Please upload a resume file first.');
      return;
    }

    setIsAnalyzing(true);
    
    // Simulate AI analysis
    setTimeout(() => {
      const mockAnalysis = {
        score: Math.floor(Math.random() * 30) + 70, // 70-100
        strengths: [
          'Strong technical skills in programming languages',
          'Good project experience',
          'Clear education background',
          'Relevant coursework mentioned'
        ],
        weaknesses: [
          'Limited work experience',
          'Could add more quantifiable achievements',
          'Missing GitHub profile link',
          'Skills section could be more detailed'
        ],
        missingSkills: [
          'Docker containerization',
          'Cloud platform experience (AWS/Azure)',
          'CI/CD pipeline knowledge',
          'Testing frameworks experience'
        ],
        suggestions: [
          'Add more specific metrics and numbers to quantify achievements',
          'Include links to your GitHub and portfolio',
          'Highlight leadership experience in projects',
          'Add relevant certifications if any'
        ],
        atsScore: Math.floor(Math.random() * 20) + 75, // 75-95
        keywordMatch: Math.floor(Math.random() * 15) + 80 // 80-95
      };
      
      setAnalysisResult(mockAnalysis);
      setIsAnalyzing(false);
    }, 3000);
  };

  const downloadReport = () => {
    alert('PDF report download would start here!');
    // In real app, this would generate and download PDF
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">AceIt Resume Analyzer</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Side - Upload & Controls */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Upload Resume</h2>
            
            <div className="space-y-4">
              {/* Job Role Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Target Job Role
                </label>
                <select
                  value={jobRole}
                  onChange={(e) => setJobRole(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  {jobRoles.map(role => (
                    <option key={role} value={role}>{role}</option>
                  ))}
                </select>
              </div>

              {/* File Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload Resume
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <input
                    type="file"
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handleFileUpload}
                    className="hidden"
                    id="resume-upload"
                  />
                  <label htmlFor="resume-upload" className="cursor-pointer">
                    <div className="text-4xl mb-2">📄</div>
                    <p className="text-gray-600 mb-2">
                      {resumeFile ? resumeFile.name : 'Click to upload resume'}
                    </p>
                    <p className="text-sm text-gray-500">
                      Supports PDF, Word, Text files
                    </p>
                  </label>
                </div>
              </div>

              {/* Analyze Button */}
              <button
                onClick={analyzeResume}
                disabled={!resumeFile || isAnalyzing}
                className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
              >
                {isAnalyzing ? (
                  <span className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Analyzing...
                  </span>
                ) : (
                  'Analyze Resume'
                )}
              </button>
            </div>
          </div>

          {/* Quick Tips */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mt-6">
            <h3 className="font-semibold text-yellow-800 mb-2">💡 Resume Tips</h3>
            <ul className="text-yellow-700 text-sm space-y-1">
              <li>• Use action verbs and quantifiable results</li>
              <li>• Include relevant keywords from job description</li>
              <li>• Keep it to 1-2 pages maximum</li>
              <li>• Proofread for spelling and grammar</li>
              <li>• Use clear, professional formatting</li>
            </ul>
          </div>
        </div>

        {/* Right Side - Analysis Results */}
        <div className="lg:col-span-2">
          {analysisResult ? (
            <div className="space-y-6">
              {/* Overall Score */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-gray-800">Analysis Results</h2>
                  <button
                    onClick={downloadReport}
                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                  >
                    📥 Download Report
                  </button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-3xl font-bold text-blue-600">{analysisResult.score}%</div>
                    <div className="text-blue-700 font-medium">Overall Score</div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-3xl font-bold text-green-600">{analysisResult.atsScore}%</div>
                    <div className="text-green-700 font-medium">ATS Friendly</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-3xl font-bold text-purple-600">{analysisResult.keywordMatch}%</div>
                    <div className="text-purple-700 font-medium">Keyword Match</div>
                  </div>
                </div>

                {/* Progress Bars */}
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Technical Skills</span>
                      <span>85%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-green-600 h-2 rounded-full" style={{ width: '85%' }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Experience Relevance</span>
                      <span>78%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '78%' }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Format & Structure</span>
                      <span>92%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-600 h-2 rounded-full" style={{ width: '92%' }}></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Strengths & Weaknesses */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Strengths */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-semibold mb-4 text-green-700 flex items-center">
                    <span className="mr-2">✅</span>
                    Strengths
                  </h3>
                  <ul className="space-y-2">
                    {analysisResult.strengths.map((strength, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        <span className="text-gray-700">{strength}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Weaknesses */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-semibold mb-4 text-red-700 flex items-center">
                    <span className="mr-2">⚠️</span>
                    Areas for Improvement
                  </h3>
                  <ul className="space-y-2">
                    {analysisResult.weaknesses.map((weakness, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-red-500 mr-2">•</span>
                        <span className="text-gray-700">{weakness}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Missing Skills & Suggestions */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Missing Skills */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-semibold mb-4 text-orange-600 flex items-center">
                    <span className="mr-2">🔍</span>
                    Recommended Skills to Add
                  </h3>
                  <ul className="space-y-2">
                    {analysisResult.missingSkills.map((skill, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-orange-500 mr-2">+</span>
                        <span className="text-gray-700">{skill}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Suggestions */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-semibold mb-4 text-blue-600 flex items-center">
                    <span className="mr-2">💡</span>
                    Actionable Suggestions
                  </h3>
                  <ul className="space-y-2">
                    {analysisResult.suggestions.map((suggestion, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-blue-500 mr-2">→</span>
                        <span className="text-gray-700">{suggestion}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            /* Placeholder before analysis */
            <div className="bg-white rounded-lg shadow-md p-12 text-center">
              <div className="text-6xl mb-4">📊</div>
              <h3 className="text-xl font-semibold text-gray-700 mb-2">
                Upload Your Resume to Get Started
              </h3>
              <p className="text-gray-500">
                Get AI-powered analysis of your resume with detailed feedback and improvement suggestions.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Resume;