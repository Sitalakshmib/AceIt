import React, { useState } from 'react';
import { resumeAPI } from '../services/api';

const Resume = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [jobRole, setJobRole] = useState('software_developer');
  const [error, setError] = useState('');

  const jobRoles = [
    { id: 'software_developer', name: 'Software Developer' },
    { id: 'frontend_developer', name: 'Frontend Developer' },
    { id: 'backend_developer', name: 'Backend Developer' },
    { id: 'full_stack_developer', name: 'Full Stack Developer' },
    { id: 'data_scientist', name: 'Data Scientist' },
    { id: 'machine_learning_engineer', name: 'Machine Learning Engineer' },
    { id: 'devops_engineer', name: 'DevOps Engineer' },
    { id: 'product_manager', name: 'Product Manager' }
  ];

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type === 'application/pdf') {
        setResumeFile(file);
        setAnalysisResult(null);
        setError('');
      } else {
        setError('Please upload a PDF file.');
      }
    }
  };

  const analyzeResume = async () => {
    if (!resumeFile) {
      setError('Please upload a resume file first.');
      return;
    }

    setIsAnalyzing(true);
    setError('');
    
    try {
      // Create FormData to send file and other data
      const formData = new FormData();
      formData.append('file', resumeFile);
      formData.append('job_role', jobRole);
      formData.append('user_id', 'user123'); // In a real app, this would come from auth context
      
      const response = await resumeAPI.analyze(formData);
      
      if (response.data.error) {
        setError(response.data.error);
        setAnalysisResult(null);
      } else {
        setAnalysisResult(response.data);
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError('Failed to analyze resume. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const downloadReport = () => {
    // Create a simple text report
    if (!analysisResult) return;
    
    let report = `=== ACEIT Resume Analysis Report ===\n\n`;
    report += `Job Role: ${jobRoles.find(r => r.id === analysisResult.job_role)?.name || analysisResult.job_role}\n`;
    report += `Overall Score: ${analysisResult.overall_score}%\n\n`;
    
    report += `=== ATS Analysis ===\n`;
    report += `ATS Friendliness: ${analysisResult.ats_analysis.ats_score}%\n`;
    report += `Keyword Match: ${analysisResult.ats_analysis.keyword_match_score}%\n`;
    report += `Formatting Score: ${analysisResult.ats_analysis.formatting_score}%\n\n`;
    
    report += `=== Skills Analysis ===\n`;
    report += `Skills Match: ${analysisResult.skills_analysis.match_score}%\n`;
    report += `Matched Skills: ${analysisResult.skills_analysis.matched_skills.join(', ')}\n`;
    report += `Missing Skills: ${analysisResult.skills_analysis.missing_skills.join(', ')}\n\n`;
    
    report += `=== Suggestions ===\n`;
    analysisResult.suggestions.forEach((suggestion, index) => {
      report += `${index + 1}. ${suggestion}\n`;
    });
    
    // Create and download file
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume-analysis-report.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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
                    <option key={role.id} value={role.id}>{role.name}</option>
                  ))}
                </select>
              </div>

              {/* File Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload Resume (PDF only)
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <input
                    type="file"
                    accept=".pdf"
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
                      Supports PDF files only
                    </p>
                  </label>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="text-red-600 text-sm p-2 bg-red-50 rounded">
                  {error}
                </div>
              )}

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
                    <div className="text-3xl font-bold text-blue-600">{analysisResult.overall_score}%</div>
                    <div className="text-blue-700 font-medium">Overall Score</div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-3xl font-bold text-green-600">{analysisResult.ats_analysis.ats_score}%</div>
                    <div className="text-green-700 font-medium">ATS Friendly</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-3xl font-bold text-purple-600">{analysisResult.skills_analysis.match_score}%</div>
                    <div className="text-purple-700 font-medium">Skills Match</div>
                  </div>
                </div>

                <div className="mb-4">
                  <p className="text-gray-700">{analysisResult.overall_feedback}</p>
                </div>

                {/* Progress Bars */}
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>ATS Compatibility</span>
                      <span>{analysisResult.ats_analysis.ats_score}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${
                          analysisResult.ats_analysis.ats_score >= 80 ? 'bg-green-600' : 
                          analysisResult.ats_analysis.ats_score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                        }`} 
                        style={{ width: `${analysisResult.ats_analysis.ats_score}%` }}
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Skills Match</span>
                      <span>{analysisResult.skills_analysis.match_score}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${
                          analysisResult.skills_analysis.match_score >= 80 ? 'bg-green-600' : 
                          analysisResult.skills_analysis.match_score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                        }`} 
                        style={{ width: `${analysisResult.skills_analysis.match_score}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* ATS Analysis */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2">🔍</span>
                  ATS Analysis
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div className="p-3 bg-blue-50 rounded">
                    <div className="font-medium">Keyword Match Score</div>
                    <div className="text-2xl font-bold text-blue-600">{analysisResult.ats_analysis.keyword_match_score}%</div>
                  </div>
                  <div className="p-3 bg-green-50 rounded">
                    <div className="font-medium">Formatting Score</div>
                    <div className="text-2xl font-bold text-green-600">{analysisResult.ats_analysis.formatting_score}%</div>
                  </div>
                </div>
                
                {analysisResult.ats_analysis.missing_keywords.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Recommended Keywords to Add:</h4>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.ats_analysis.missing_keywords.map((keyword, index) => (
                        <span key={index} className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {analysisResult.ats_analysis.formatting_issues.length > 0 && (
                  <div className="mt-4">
                    <h4 className="font-medium text-gray-700 mb-2">Formatting Issues:</h4>
                    <ul className="list-disc pl-5 space-y-1">
                      {analysisResult.ats_analysis.formatting_issues.map((issue, index) => (
                        <li key={index} className="text-gray-600">{issue}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Skills Analysis */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2">🛠️</span>
                  Skills Analysis
                </h3>
                <div className="mb-4">
                  <div className="font-medium mb-2">
                    Matched Skills ({analysisResult.skills_analysis.matched_skills_count}/{analysisResult.skills_analysis.total_required_skills})
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {analysisResult.skills_analysis.matched_skills.map((skill, index) => (
                      <span key={index} className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
                
                {analysisResult.skills_analysis.missing_skills.length > 0 && (
                  <div>
                    <div className="font-medium mb-2">Missing Skills:</div>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.skills_analysis.missing_skills.map((skill, index) => (
                        <span key={index} className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Suggestions */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2">💡</span>
                  Actionable Suggestions
                </h3>
                <ul className="space-y-2">
                  {analysisResult.suggestions.map((suggestion, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-blue-500 mr-2 mt-1">→</span>
                      <span className="text-gray-700">{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Contact Info */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2">📞</span>
                  Contact Information Found
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <div className="text-sm text-gray-500">Email</div>
                    <div className="font-medium">
                      {analysisResult.contact_info?.email || 'Not found'}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Phone</div>
                    <div className="font-medium">
                      {analysisResult.contact_info?.phone || 'Not found'}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">LinkedIn</div>
                    <div className="font-medium">
                      {analysisResult.contact_info?.linkedin ? '✓ Found' : 'Not found'}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">GitHub</div>
                    <div className="font-medium">
                      {analysisResult.contact_info?.github ? '✓ Found' : 'Not found'}
                    </div>
                  </div>
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
              <div className="mt-6 text-sm text-gray-400">
                <p>✓ ATS-friendly analysis</p>
                <p>✓ Skills matching</p>
                <p>✓ Readability assessment</p>
                <p>✓ Actionable suggestions</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Resume;