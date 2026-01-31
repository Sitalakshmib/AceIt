import React, { useState } from 'react';
import { resumeAPI } from '../services/api';
// Import jsPDF for PDF generation
import jsPDF from 'jspdf';
import 'jspdf-autotable';
// Import custom components
import {
  ScoreCircle,
  ScoreBadge,
  SectionHeader,
  SkillTag,
  MetricCard,
  ProgressBar,
  InsightCard,
  MiniProgress,
  EmptyState,
  StrengthWeaknessCard,
  AIInsightPanel,
  AISectionCard
} from '../components/Resume/ResumeComponents';

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

      console.log('[Resume] Sending analysis request...');
      console.log('[Resume] File:', resumeFile.name);
      console.log('[Resume] Job Role:', jobRole);

      const response = await resumeAPI.analyze(formData);

      console.log('[Resume] Response received:', response.data);

      if (response.data.error) {
        setError(response.data.error);
        setAnalysisResult(null);
      } else {
        setAnalysisResult(response.data);
      }
    } catch (err) {
      console.error('[Resume] Analysis error:', err);
      console.error('[Resume] Error details:', err.response?.data || err.message);
      setError('Failed to analyze resume. Error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Helper function to render text with markdown-style bold (**text**) as actual bold
  const renderTextWithBold = (text) => {
    if (!text) return null;

    // Split by **text** pattern
    const parts = text.split(/(\*\*.*?\*\*)/g);

    return parts.map((part, index) => {
      // Check if this part is bold (wrapped in **)
      if (part.startsWith('**') && part.endsWith('**')) {
        // Remove the ** and render as bold
        const boldText = part.slice(2, -2);
        return <strong key={index} className="font-bold text-gray-900">{boldText}</strong>;
      }
      // Regular text
      return <span key={index}>{part}</span>;
    });
  };

  const downloadReport = () => {
    if (!analysisResult) return;

    const doc = new jsPDF();
    let yPos = 20;
    const pageWidth = doc.internal.pageSize.width;
    const pageHeight = doc.internal.pageSize.height;
    const margin = 20;
    const contentWidth = pageWidth - 2 * margin;

    // Helper function to add a new page if needed
    const checkPageBreak = (requiredSpace = 20) => {
      if (yPos + requiredSpace > pageHeight - 30) {
        addFooter();
        doc.addPage();
        yPos = 20;
        return true;
      }
      return false;
    };

    // Helper to add footer on each page
    const addFooter = () => {
      const pageNum = doc.internal.getCurrentPageInfo().pageNumber;
      doc.setFontSize(8);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(120, 120, 120);
      doc.setDrawColor(220, 220, 220);
      doc.line(margin, pageHeight - 20, pageWidth - margin, pageHeight - 20);
      doc.text('AceIt Resume Analyzer - Professional Resume Analysis', pageWidth / 2, pageHeight - 12, { align: 'center' });
      doc.text(`Page ${pageNum}`, pageWidth - margin, pageHeight - 12, { align: 'right' });
      doc.text(new Date().toLocaleDateString(), margin, pageHeight - 12);
    };

    // Helper to draw section header
    const drawSectionHeader = (title, icon = '') => {
      checkPageBreak(15);
      doc.setFillColor(245, 247, 250);
      doc.roundedRect(margin, yPos, contentWidth, 12, 2, 2, 'F');

      doc.setFontSize(14);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(30, 58, 138);
      doc.text(`${icon} ${title}`, margin + 5, yPos + 8);
      yPos += 18;
    };

    // === PROFESSIONAL HEADER ===
    doc.setFillColor(30, 58, 138);
    doc.rect(0, 0, pageWidth, 50, 'F');

    doc.setFillColor(59, 130, 246);
    doc.rect(0, 50, pageWidth, 5, 'F');

    doc.setTextColor(255, 255, 255);
    doc.setFontSize(28);
    doc.setFont('helvetica', 'bold');
    doc.text('RESUME ANALYSIS REPORT', pageWidth / 2, 25, { align: 'center' });

    doc.setFontSize(11);
    doc.setFont('helvetica', 'normal');
    const currentDate = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    doc.text(`Professional Analysis Generated on ${currentDate}`, pageWidth / 2, 38, { align: 'center' });

    yPos = 65;
    doc.setTextColor(0, 0, 0);

    // === EXECUTIVE SUMMARY ===
    drawSectionHeader('EXECUTIVE SUMMARY', '>');

    const jobRoleName = jobRoles.find(r => r.id === analysisResult.job_role)?.name || analysisResult.job_role;
    doc.setFontSize(10);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(60, 60, 60);
    doc.text('Target Position:', margin, yPos);
    doc.setFont('helvetica', 'normal');
    doc.text(jobRoleName, margin + 40, yPos);
    yPos += 10;

    // Professional Score Cards
    const cardWidth = (contentWidth - 10) / 3;
    const drawProfessionalScoreCard = (x, y, label, score, maxScore) => {
      const percentage = maxScore ? (score / maxScore) * 100 : score;
      const color = percentage >= 80 ? [16, 185, 129] : percentage >= 60 ? [245, 158, 11] : [239, 68, 68];

      // Card background
      doc.setFillColor(250, 250, 250);
      doc.roundedRect(x, y, cardWidth, 28, 3, 3, 'F');

      // Colored top border
      doc.setFillColor(color[0], color[1], color[2]);
      doc.roundedRect(x, y, cardWidth, 4, 3, 3, 'F');

      // Border
      doc.setDrawColor(220, 220, 220);
      doc.setLineWidth(0.5);
      doc.roundedRect(x, y, cardWidth, 28, 3, 3, 'S');

      // Label
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(100, 100, 100);
      doc.text(label, x + cardWidth / 2, y + 12, { align: 'center' });

      // Score
      doc.setFontSize(16);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(color[0], color[1], color[2]);
      const scoreText = maxScore ? `${score}/${maxScore}` : `${Math.round(score)}%`;
      doc.text(scoreText, x + cardWidth / 2, y + 23, { align: 'center' });
    };

    drawProfessionalScoreCard(margin, yPos, 'Overall Score', analysisResult.overall_score);
    drawProfessionalScoreCard(margin + cardWidth + 5, yPos, 'ATS Compatibility', analysisResult.ats_analysis.ats_score, 100);
    drawProfessionalScoreCard(margin + 2 * cardWidth + 10, yPos, 'Skills Match', analysisResult.skills_analysis.match_score);
    yPos += 35;

    // Overall Assessment
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(60, 60, 60);
    const feedbackLines = doc.splitTextToSize(analysisResult.overall_feedback, contentWidth);
    doc.text(feedbackLines, margin, yPos, { align: 'justify', maxWidth: contentWidth });
    yPos += feedbackLines.length * 5 + 12;

    // === CONTACT INFORMATION ===
    drawSectionHeader('CONTACT INFORMATION', '@');

    const contactData = [
      ['Email:', analysisResult.contact_info.email || 'Not found'],
      ['Phone:', analysisResult.contact_info.phone || 'Not found'],
      ['LinkedIn:', analysisResult.contact_info.linkedin || 'Not found'],
      ['GitHub:', analysisResult.contact_info.github || 'Not found']
    ];

    doc.setFontSize(10);
    contactData.forEach(([label, value]) => {
      checkPageBreak(7);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(70, 70, 70);
      doc.text(label, margin + 5, yPos);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(90, 90, 90);
      const displayValue = value === 'Not found' ? value : (value.length > 60 ? value.substring(0, 57) + '...' : value);
      doc.text(displayValue, margin + 35, yPos);
      yPos += 7;
    });
    yPos += 5;

    // === ATS COMPATIBILITY ANALYSIS ===
    drawSectionHeader('ATS COMPATIBILITY ANALYSIS', '#');

    doc.setFontSize(10);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(60, 60, 60);
    doc.text(`Overall ATS Score: ${analysisResult.ats_analysis.ats_score}/100`, margin, yPos);
    yPos += 10;

    // ATS component scores with progress bars
    const atsComponents = [
      { label: 'Contact Information', score: analysisResult.ats_analysis.contact_info_score, max: 25 },
      { label: 'Resume Sections', score: analysisResult.ats_analysis.section_score, max: 30 },
      { label: 'Formatting Quality', score: analysisResult.ats_analysis.formatting_score, max: 20 },
      { label: 'Content Quality', score: analysisResult.ats_analysis.content_score, max: 25 }
    ];

    atsComponents.forEach(({ label, score, max }) => {
      checkPageBreak(12);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(70, 70, 70);
      doc.text(label, margin + 5, yPos);

      doc.setFont('helvetica', 'bold');
      doc.text(`${score}/${max}`, margin + 60, yPos);

      // Progress bar
      const barWidth = 100;
      const fillWidth = (score / max) * barWidth;
      const barX = margin + 80;

      doc.setFillColor(240, 240, 240);
      doc.roundedRect(barX, yPos - 4, barWidth, 5, 1, 1, 'F');

      const percentage = (score / max) * 100;
      const barColor = percentage >= 80 ? [16, 185, 129] : percentage >= 60 ? [245, 158, 11] : [239, 68, 68];
      doc.setFillColor(barColor[0], barColor[1], barColor[2]);
      doc.roundedRect(barX, yPos - 4, fillWidth, 5, 1, 1, 'F');

      yPos += 10;
    });
    yPos += 3;

    // Missing elements
    if (analysisResult.ats_analysis.missing_elements.length > 0) {
      checkPageBreak(15);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(239, 68, 68);
      doc.text('Missing Elements:', margin + 5, yPos);
      yPos += 6;
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(90, 90, 90);
      analysisResult.ats_analysis.missing_elements.forEach(element => {
        checkPageBreak(6);
        doc.text(`  - ${element}`, margin + 10, yPos);
        yPos += 5;
      });
      yPos += 5;
    }

    // === SKILLS ANALYSIS ===
    drawSectionHeader('SKILLS ANALYSIS', '*');

    doc.setFontSize(10);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(60, 60, 60);
    doc.text(`Skills Match: ${analysisResult.skills_analysis.matched_skills_count}/${analysisResult.skills_analysis.total_required_skills} (${analysisResult.skills_analysis.match_score}%)`, margin, yPos);
    yPos += 10;

    if (analysisResult.skills_analysis.matched_skills.length > 0) {
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(16, 185, 129);
      doc.text('Skills Found:', margin + 5, yPos);
      yPos += 6;
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(70, 70, 70);

      const skillsText = analysisResult.skills_analysis.matched_skills.join(', ');
      const skillLines = doc.splitTextToSize(skillsText, contentWidth - 10);
      skillLines.forEach(line => {
        checkPageBreak(5);
        doc.text(line, margin + 10, yPos);
        yPos += 5;
      });
      yPos += 5;
    }

    if (analysisResult.skills_analysis.missing_skills.length > 0) {
      checkPageBreak(10);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(245, 158, 11);
      doc.text('Recommended Skills to Add:', margin + 5, yPos);
      yPos += 6;
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(70, 70, 70);

      const missingText = analysisResult.skills_analysis.missing_skills.slice(0, 15).join(', ');
      const missingLines = doc.splitTextToSize(missingText, contentWidth - 10);
      missingLines.forEach(line => {
        checkPageBreak(5);
        doc.text(line, margin + 10, yPos);
        yPos += 5;
      });
      yPos += 5;
    }

    // === ACTIONABLE RECOMMENDATIONS ===
    drawSectionHeader('ACTIONABLE RECOMMENDATIONS', '+');

    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(70, 70, 70);
    analysisResult.suggestions.forEach((suggestion, index) => {
      checkPageBreak(12);
      doc.setFont('helvetica', 'bold');
      doc.text(`${index + 1}.`, margin + 5, yPos);
      doc.setFont('helvetica', 'normal');
      const suggestionLines = doc.splitTextToSize(suggestion, contentWidth - 15);
      doc.text(suggestionLines, margin + 12, yPos, { align: 'justify', maxWidth: contentWidth - 15 });
      yPos += suggestionLines.length * 5 + 3;
    });
    yPos += 5;

    // === AI INSIGHTS ===
    if (analysisResult.ai_analysis) {
      drawSectionHeader('AI-POWERED INSIGHTS', '~');

      if (analysisResult.ai_analysis.overall_impression) {
        checkPageBreak(15);
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(147, 51, 234);
        doc.text('Overall Impression:', margin + 5, yPos);
        yPos += 6;
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(70, 70, 70);
        doc.setFontSize(10);
        const impressionLines = doc.splitTextToSize(analysisResult.ai_analysis.overall_impression, contentWidth - 10);
        impressionLines.forEach(line => {
          checkPageBreak(5);
          doc.text(line, margin + 10, yPos, { align: 'justify', maxWidth: contentWidth - 10 });
          yPos += 5;
        });
        yPos += 5;
      }

      if (analysisResult.ai_analysis.strengths && analysisResult.ai_analysis.strengths.length > 0) {
        checkPageBreak(15);
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(16, 185, 129);
        doc.text('Key Strengths:', margin + 5, yPos);
        yPos += 6;
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(70, 70, 70);

        analysisResult.ai_analysis.strengths.forEach(strength => {
          checkPageBreak(8);
          const strengthLines = doc.splitTextToSize(`- ${strength}`, contentWidth - 10);
          doc.text(strengthLines, margin + 10, yPos, { align: 'justify', maxWidth: contentWidth - 10 });
          yPos += strengthLines.length * 5;
        });
        yPos += 5;
      }

      if (analysisResult.ai_analysis.areas_for_improvement && analysisResult.ai_analysis.areas_for_improvement.length > 0) {
        checkPageBreak(15);
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(245, 158, 11);
        doc.text('Areas for Improvement:', margin + 5, yPos);
        yPos += 6;
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(70, 70, 70);

        analysisResult.ai_analysis.areas_for_improvement.forEach(area => {
          checkPageBreak(8);
          const areaLines = doc.splitTextToSize(`- ${area}`, contentWidth - 10);
          doc.text(areaLines, margin + 10, yPos, { align: 'justify', maxWidth: contentWidth - 10 });
          yPos += areaLines.length * 5;
        });
        yPos += 5;
      }

      if (analysisResult.ai_analysis.actionable_tips && analysisResult.ai_analysis.actionable_tips.length > 0) {
        checkPageBreak(15);
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(99, 102, 241);
        doc.text('AI Actionable Tips:', margin + 5, yPos);
        yPos += 6;
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(70, 70, 70);

        analysisResult.ai_analysis.actionable_tips.forEach((tip, index) => {
          checkPageBreak(10);
          // Remove markdown bold syntax for PDF
          const cleanTip = tip.replace(/\*\*(.*?)\*\*/g, '$1');
          const tipLines = doc.splitTextToSize(`${index + 1}. ${cleanTip}`, contentWidth - 10);
          doc.text(tipLines, margin + 10, yPos, { align: 'justify', maxWidth: contentWidth - 10 });
          yPos += tipLines.length * 5 + 2;
        });
      }
    }

    // Add footer to last page
    addFooter();

    // Save the PDF
    doc.save(`Resume-Analysis-${currentDate.replace(/\s/g, '-')}.pdf`);
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
                    <div className="text-4xl mb-2"></div>
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
            <h3 className="font-semibold text-yellow-800 mb-2">Resume Tips</h3>
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
              {/* Overall Score - Enhanced */}
              <div className="bg-gradient-to-br from-white to-gray-50 rounded-xl shadow-lg p-8 border border-gray-100">
                <SectionHeader
                  icon=""
                  title="Resume Analysis Summary"
                  subtitle={`Analysis for ${jobRoles.find(r => r.id === analysisResult.job_role)?.name || analysisResult.job_role}`}
                >
                  <button
                    onClick={downloadReport}
                    className="bg-gradient-to-r from-green-600 to-green-700 text-white px-5 py-2.5 rounded-lg hover:from-green-700 hover:to-green-800 transition-all shadow-md hover:shadow-lg flex items-center gap-2"
                  >
                    <span></span>
                    <span className="font-semibold">Download PDF Report</span>
                  </button>
                </SectionHeader>

                {/* Score Circles */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                  <div className="flex flex-col items-center p-4 bg-white rounded-lg shadow-sm">
                    <ScoreCircle score={analysisResult.overall_score} label="Overall" />
                    <ScoreBadge score={analysisResult.overall_score} />
                  </div>
                  <div className="flex flex-col items-center p-4 bg-white rounded-lg shadow-sm">
                    <ScoreCircle score={analysisResult.ats_analysis.ats_score} label="ATS" />
                    <ScoreBadge score={analysisResult.ats_analysis.ats_score} />
                  </div>
                  <div className="flex flex-col items-center p-4 bg-white rounded-lg shadow-sm">
                    <ScoreCircle score={analysisResult.skills_analysis.match_score} label="Skills" />
                    <ScoreBadge score={analysisResult.skills_analysis.match_score} />
                  </div>
                </div>

                {/* Overall Feedback */}
                <InsightCard type="info" icon="" title="Overall Assessment">
                  <p className="leading-relaxed">{analysisResult.overall_feedback}</p>
                </InsightCard>

                {/* Enhanced Progress Bars */}
                <div className="mt-6 space-y-2">
                  <ProgressBar
                    label="ATS Compatibility"
                    current={analysisResult.ats_analysis.ats_score}
                  />
                  <ProgressBar
                    label="Skills Match"
                    current={analysisResult.skills_analysis.match_score}
                  />
                </div>
              </div>

              {/* Contact Information */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
                  <span className="mr-2"></span>
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

              {/* ATS Analysis - Enhanced */}
              <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-100">
                <SectionHeader
                  icon=""
                  title="ATS Compatibility Analysis"
                  subtitle={`Overall ATS Score: ${analysisResult.ats_analysis.ats_score}/100`}
                />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <MetricCard
                    icon=""
                    label="Contact Information"
                    value={`${analysisResult.ats_analysis.contact_info_score}/25`}
                    color="blue"
                  />
                  <MetricCard
                    icon=""
                    label="Resume Sections"
                    value={`${analysisResult.ats_analysis.section_score}/30`}
                    color="green"
                  />
                  <MetricCard
                    icon=""
                    label="Formatting Quality"
                    value={`${analysisResult.ats_analysis.formatting_score}/20`}
                    color="purple"
                  />
                  <MetricCard
                    icon=""
                    label="Content Quality"
                    value={`${analysisResult.ats_analysis.content_score}/25`}
                    color="orange"
                  />
                </div>

                {/* Component Breakdown with Mini Progress Bars */}
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <h4 className="font-semibold text-gray-700 mb-3">Component Breakdown</h4>
                  <MiniProgress label="Contact Info" value={analysisResult.ats_analysis.contact_info_score} max={25} color="blue" />
                  <MiniProgress label="Sections" value={analysisResult.ats_analysis.section_score} max={30} color="green" />
                  <MiniProgress label="Formatting" value={analysisResult.ats_analysis.formatting_score} max={20} color="purple" />
                  <MiniProgress label="Content" value={analysisResult.ats_analysis.content_score} max={25} color="orange" />
                </div>

                {analysisResult.ats_analysis.missing_elements.length > 0 && (
                  <InsightCard type="warning" icon="" title="Missing Elements">
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.ats_analysis.missing_elements.map((element, index) => (
                        <span key={index} className="bg-orange-100 text-orange-800 px-3 py-1.5 rounded-lg text-sm font-medium border border-orange-200">
                          {element}
                        </span>
                      ))}
                    </div>
                  </InsightCard>
                )}
              </div>

              {/* Skills Analysis - Enhanced */}
              <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-100">
                <SectionHeader
                  icon=""
                  title="Skills Match Analysis"
                  subtitle={`${analysisResult.skills_analysis.matched_skills_count} of ${analysisResult.skills_analysis.total_required_skills} required skills found`}
                />

                {/* Skills Match Progress */}
                <div className="mb-6">
                  <ProgressBar
                    label={`Skills Match Rate: ${analysisResult.skills_analysis.match_score}%`}
                    current={analysisResult.skills_analysis.matched_skills_count}
                    max={analysisResult.skills_analysis.total_required_skills}
                    showPercentage={false}
                  />
                </div>

                {/* Matched Skills */}
                {analysisResult.skills_analysis.matched_skills.length > 0 && (
                  <InsightCard type="success" icon="" title={`Matched Skills (${analysisResult.skills_analysis.matched_skills_count})`}>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.skills_analysis.matched_skills.map((skill, index) => (
                        <SkillTag key={index} skill={skill} matched={true} />
                      ))}
                    </div>
                  </InsightCard>
                )}

                {/* Missing Skills */}
                {analysisResult.skills_analysis.missing_skills.length > 0 && (
                  <InsightCard type="warning" icon="" title="Recommended Skills to Add">
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.skills_analysis.missing_skills.map((skill, index) => (
                        <SkillTag key={index} skill={skill} matched={false} />
                      ))}
                    </div>
                  </InsightCard>
                )}
              </div>

              {/* Suggestions - Enhanced */}
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg shadow-lg p-6 border border-blue-200">
                <SectionHeader
                  icon=""
                  title="Actionable Recommendations"
                  subtitle="Prioritized steps to improve your resume"
                />
                <div className="space-y-3">
                  {analysisResult.suggestions.map((suggestion, index) => (
                    <div key={index} className="flex items-start bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow border border-blue-100">
                      <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-sm mr-3">
                        {index + 1}
                      </div>
                      <p className="text-gray-700 leading-relaxed flex-1">{suggestion}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* AI-Powered Feedback (Gemini) - ENHANCED */}
              {analysisResult.ai_analysis && (
                <>
                  {/* Strengths & Weaknesses - Prominent Display */}
                  {(analysisResult.ai_analysis.strengths?.length > 0 || analysisResult.ai_analysis.areas_for_improvement?.length > 0) && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                      {/* Strengths Card */}
                      {analysisResult.ai_analysis.strengths && analysisResult.ai_analysis.strengths.length > 0 && (
                        <StrengthWeaknessCard
                          type="strength"
                          items={analysisResult.ai_analysis.strengths}
                          title="Key Strengths"
                        />
                      )}

                      {/* Areas for Improvement Card */}
                      {analysisResult.ai_analysis.areas_for_improvement && analysisResult.ai_analysis.areas_for_improvement.length > 0 && (
                        <StrengthWeaknessCard
                          type="weakness"
                          items={analysisResult.ai_analysis.areas_for_improvement}
                          title="Areas for Improvement"
                        />
                      )}
                    </div>
                  )}

                  {/* AI Insights Panel */}
                  <AIInsightPanel title="AI-Powered Insights">
                    {/* Overall Impression */}
                    {analysisResult.ai_analysis.overall_impression && (
                      <AISectionCard icon="" title="Overall Impression" color="blue">
                        <p>{analysisResult.ai_analysis.overall_impression}</p>
                      </AISectionCard>
                    )}

                    {/* Interview Readiness */}
                    {analysisResult.ai_analysis.interview_readiness && (
                      <AISectionCard icon="" title="Interview Readiness" color="green">
                        <p>{analysisResult.ai_analysis.interview_readiness}</p>
                      </AISectionCard>
                    )}

                    {/* Actionable Tips - Enhanced */}
                    {analysisResult.ai_analysis.actionable_tips && analysisResult.ai_analysis.actionable_tips.length > 0 && (
                      <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl p-6 border-2 border-purple-200 shadow-sm">
                        <div className="flex items-center mb-5">
                          <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-xl flex items-center justify-center text-white text-2xl shadow-md mr-4">
                          </div>
                          <div>
                            <h4 className="text-xl font-bold text-purple-900">AI Actionable Tips</h4>
                            <p className="text-sm text-purple-600">{analysisResult.ai_analysis.actionable_tips.length} recommendations to improve your resume</p>
                          </div>
                        </div>

                        <div className="grid grid-cols-1 gap-3">
                          {analysisResult.ai_analysis.actionable_tips.map((tip, index) => (
                            <div
                              key={index}
                              className="bg-white rounded-lg p-4 border border-purple-100 hover:shadow-md hover:border-purple-300 transition-all duration-200"
                            >
                              <div className="flex items-start">
                                <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-purple-600 to-indigo-600 text-white rounded-lg flex items-center justify-center font-bold text-sm mr-4 shadow-sm">
                                  {index + 1}
                                </div>
                                <div className="flex-1">
                                  <p className="text-gray-800 leading-relaxed">{renderTextWithBold(tip)}</p>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Keyword Suggestions */}
                    {analysisResult.ai_analysis.keyword_suggestions && analysisResult.ai_analysis.keyword_suggestions.length > 0 && (
                      <AISectionCard icon="" title="Suggested Keywords for ATS" color="gray">
                        <div className="flex flex-wrap gap-2">
                          {analysisResult.ai_analysis.keyword_suggestions.map((keyword, index) => (
                            <span key={index} className="bg-gradient-to-r from-purple-100 to-blue-100 text-purple-800 px-4 py-2 rounded-full text-sm font-medium border border-purple-200 shadow-sm">
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </AISectionCard>
                    )}

                    {/* Formatting Advice */}
                    {analysisResult.ai_analysis.formatting_advice && (
                      <AISectionCard icon="" title="Formatting Advice" color="gray">
                        <p>{analysisResult.ai_analysis.formatting_advice}</p>
                      </AISectionCard>
                    )}

                    {/* Raw feedback fallback */}
                    {analysisResult.ai_analysis.raw_feedback && !analysisResult.ai_analysis.overall_impression && (
                      <AISectionCard icon="" title="AI Feedback" color="gray">
                        <p className="whitespace-pre-wrap">{analysisResult.ai_analysis.raw_feedback}</p>
                      </AISectionCard>
                    )}
                  </AIInsightPanel>
                </>
              )}

              {/* AI Error Message */}
              {analysisResult.ai_error && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-yellow-700 text-sm">
                    <span className="font-medium">Note:</span> AI analysis was not available: {analysisResult.ai_error}
                  </p>
                </div>
              )}
            </div>
          ) : (
            /* Empty State - Enhanced */
            <EmptyState
              icon=""
              title="Upload Your Resume to Get Started"
              description="Get AI-powered analysis of your resume with detailed feedback and improvement suggestions."
              features={[
                "ATS-friendly analysis",
                "Skills matching",
                "Professional feedback",
                "Actionable suggestions"
              ]}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default Resume;