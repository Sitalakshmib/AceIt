import React, { useState } from 'react';
import { resumeAPI } from '../services/api';
// Import jsPDF for PDF generation
import jsPDF from 'jspdf';
import 'jspdf-autotable';

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
    // Create a PDF report instead of text
    if (!analysisResult) return;
    
    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(20);
    doc.text('ACEIT Resume Analysis Report', 105, 20, null, null, 'center');
    
    // Add job role and overall score
    doc.setFontSize(12);
    const jobRoleName = jobRoles.find(r => r.id === analysisResult.job_role)?.name || analysisResult.job_role;
    doc.text(`Job Role: ${jobRoleName}`, 20, 35);
    doc.text(`Overall Score: ${analysisResult.overall_score}%`, 20, 45);
    
    // Add Contact Information
    doc.setFontSize(16);
    doc.text('Contact Information', 20, 60);
    doc.setFontSize(12);
    doc.text(`Email: ${analysisResult.contact_info.email}`, 20, 70);
    doc.text(`Phone: ${analysisResult.contact_info.phone}`, 20, 80);
    doc.text(`LinkedIn: ${analysisResult.contact_info.linkedin}`, 20, 90);
    doc.text(`GitHub: ${analysisResult.contact_info.github}`, 20, 100);
    
    // Add ATS Analysis
    doc.setFontSize(16);
    doc.text('ATS Analysis', 20, 120);
    doc.setFontSize(12);
    doc.text(`ATS Score: ${analysisResult.ats_analysis.ats_score}/100`, 20, 130);
    doc.text(`Contact Info: ${analysisResult.ats_analysis.contact_info_score}/25`, 20, 140);
    doc.text(`Sections: ${analysisResult.ats_analysis.section_score}/30`, 20, 150);
    doc.text(`Formatting: ${analysisResult.ats_analysis.formatting_score}/20`, 20, 160);
    doc.text(`Content: ${analysisResult.ats_analysis.content_score}/25`, 20, 170);
    
    // Add Skills Analysis
    doc.setFontSize(16);
    doc.text('Skills Analysis', 20, 190);
    doc.setFontSize(12);
    doc.text(`Skills Match: ${analysisResult.skills_analysis.match_score}%`, 20, 200);
    doc.text(`Matched Skills: ${analysisResult.skills_analysis.matched_skills.length}/${analysisResult.skills_analysis.total_required_skills}`, 20, 210);
    
    // Add Suggestions
    doc.setFontSize(16);
    doc.text('Suggestions', 20, 230);
    doc.setFontSize(12);
    
    // Add suggestions as bullet points
    analysisResult.suggestions.slice(0, 8).forEach((suggestion, index) => {
      const yPosition = 240 + (index * 10);
      if (yPosition < 280) { // Avoid going beyond page
        doc.text(`• ${suggestion}`, 20, yPosition);
      }
    });
    
    // Save the PDF
    doc.save('resume-analysis-report.pdf');
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
                    📥 Download PDF Report
                  </button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-3xl font-bold text-blue-600">{analysisResult.overall_score}%</div>
                    <div className="text-blue-700 font-medium">Overall Score</div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-3xl font-bold text-green-600">{analysisResult.ats_analysis.ats_score}/100</div>
                    <div className="text-green-700 font-medium">ATS Score</div>
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
                      <span>{analysisResult.ats_analysis.ats_score}/100</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${
                          analysisResult.ats_analysis.ats_score >= 80 ? 'bg-green-600' : 
                          analysisResult.ats_analysis.ats_score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                        }`} 
                        style={{ width: `${Math.min(100, analysisResult.ats_analysis.ats_score)}%` }}
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

              {/* Contact Information */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2">📞</span>
                  Contact Information
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-3 border rounded">
                    <div className="text-sm text-gray-500">Email</div>
                    <div className="font-medium">{analysisResult.contact_info.email}</div>
                  </div>
                  <div className="p-3 border rounded">
                    <div className="text-sm text-gray-500">Phone</div>
                    <div className="font-medium">{analysisResult.contact_info.phone}</div>
                  </div>
                  <div className="p-3 border rounded">
                    <div className="text-sm text-gray-500">LinkedIn</div>
                    <div className="font-medium">{analysisResult.contact_info.linkedin}</div>
                  </div>
                  <div className="p-3 border rounded">
                    <div className="text-sm text-gray-500">GitHub</div>
                    <div className="font-medium">{analysisResult.contact_info.github}</div>
                  </div>
                </div>
              </div>

              {/* ATS Analysis */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2">🔍</span>
                  ATS Analysis (Score: {analysisResult.ats_analysis.ats_score}/100)
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div className="p-3 bg-blue-50 rounded">
                    <div className="font-medium">Contact Info</div>
                    <div className="text-2xl font-bold text-blue-600">{analysisResult.ats_analysis.contact_info_score}/25</div>
                  </div>
                  <div className="p-3 bg-green-50 rounded">
                    <div className="font-medium">Sections</div>
                    <div className="text-2xl font-bold text-green-600">{analysisResult.ats_analysis.section_score}/30</div>
                  </div>
                  <div className="p-3 bg-purple-50 rounded">
                    <div className="font-medium">Formatting</div>
                    <div className="text-2xl font-bold text-purple-600">{analysisResult.ats_analysis.formatting_score}/20</div>
                  </div>
                  <div className="p-3 bg-yellow-50 rounded">
                    <div className="font-medium">Content</div>
                    <div className="text-2xl font-bold text-yellow-600">{analysisResult.ats_analysis.content_score}/25</div>
                  </div>
                </div>
                
                {analysisResult.ats_analysis.missing_elements.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Missing Elements:</h4>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.ats_analysis.missing_elements.map((element, index) => (
                        <span key={index} className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm">
                          {element}
                        </span>
                      ))}
                    </div>
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