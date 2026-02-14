import React, { useState } from 'react';
import { Loader2, AlertCircle, FileDown, Trash2, Plus, Sparkles, Wand2, ChevronRight, CheckCircle2 } from 'lucide-react';
import { resumeAPI } from '../../services/api';
import ResumePreview from './ResumePreview';

const ResumeCreator = () => {
    const [isGenerating, setIsGenerating] = useState(false);
    const [error, setError] = useState('');
    const [selectedTemplate, setSelectedTemplate] = useState('general');

    const [formData, setFormData] = useState({
        personal_info: {
            name: '',
            email: '',
            phone: '',
            linkedin: '',
            github: ''
        },
        professional_profile: {
            current_status: 'student',
            years_of_experience: 0,
            career_goal: '',
            preferred_domain: ''
        },
        education: [{ degree: '', institution: '', year: '', gpa: '' }],
        skills: [],
        projects: [{ title: '', description: '', technologies: '' }],
        experience: [],
        certifications: [],
        target_role: 'software_developer',
        template_type: 'general',
        references: [] // Added references field
    });

    // Content Review State
    const [generatedContent, setGeneratedContent] = useState(null);
    const [isReviewing, setIsReviewing] = useState(false);
    const [isSaving, setIsSaving] = useState(false);

    // Temp inputs
    const [skillInput, setSkillInput] = useState('');
    const [certInput, setCertInput] = useState('');

    // References Input State
    const [refInput, setRefInput] = useState({
        name: '',
        designation: '',
        organization: '',
        contact: ''
    });

    // Style Options (for visual editor)
    const [styleOptions, setStyleOptions] = useState({});

    const handlePersonalInfoChange = (field, value) => {
        setFormData(prev => ({
            ...prev,
            personal_info: { ...prev.personal_info, [field]: value }
        }));
    };

    const addEducation = () => {
        setFormData(prev => ({
            ...prev,
            education: [...prev.education, { degree: '', institution: '', year: '', gpa: '' }]
        }));
    };

    const updateEducation = (index, field, value) => {
        setFormData(prev => ({
            ...prev,
            education: prev.education.map((edu, i) =>
                i === index ? { ...edu, [field]: value } : edu
            )
        }));
    };

    const removeEducation = (index) => {
        setFormData(prev => ({
            ...prev,
            education: prev.education.filter((_, i) => i !== index)
        }));
    };

    const addSkill = () => {
        if (skillInput.trim()) {
            setFormData(prev => ({
                ...prev,
                skills: [...prev.skills, skillInput.trim()]
            }));
            setSkillInput('');
        }
    };

    const removeSkill = (index) => {
        setFormData(prev => ({
            ...prev,
            skills: prev.skills.filter((_, i) => i !== index)
        }));
    };

    const addProject = () => {
        setFormData(prev => ({
            ...prev,
            projects: [...prev.projects, { title: '', description: '', technologies: '' }]
        }));
    };

    const updateProject = (index, field, value) => {
        setFormData(prev => ({
            ...prev,
            projects: prev.projects.map((proj, i) =>
                i === index ? { ...proj, [field]: value } : proj
            )
        }));
    };

    const removeProject = (index) => {
        setFormData(prev => ({
            ...prev,
            projects: prev.projects.filter((_, i) => i !== index)
        }));
    };

    const addExperience = () => {
        setFormData(prev => ({
            ...prev,
            experience: [...prev.experience, { role: '', company: '', duration: '', responsibilities: '' }]
        }));
    };

    const updateExperience = (index, field, value) => {
        setFormData(prev => ({
            ...prev,
            experience: prev.experience.map((exp, i) =>
                i === index ? { ...exp, [field]: value } : exp
            )
        }));
    };

    const removeExperience = (index) => {
        setFormData(prev => ({
            ...prev,
            experience: prev.experience.filter((_, i) => i !== index)
        }));
    };

    const addCertification = () => {
        if (certInput.trim()) {
            setFormData(prev => ({
                ...prev,
                certifications: [...prev.certifications, certInput.trim()]
            }));
            setCertInput('');
        }
    };

    const removeCertification = (index) => {
        setFormData(prev => ({
            ...prev,
            certifications: prev.certifications.filter((_, i) => i !== index)
        }));
    };

    const addReference = () => {
        if (refInput.name.trim()) {
            setFormData(prev => ({
                ...prev,
                references: [...prev.references, { ...refInput }]
            }));
            setRefInput({ name: '', designation: '', organization: '', contact: '' });
        }
    };

    const removeReference = (index) => {
        setFormData(prev => ({
            ...prev,
            references: prev.references.filter((_, i) => i !== index)
        }));
    };

    const validateForm = () => {
        if (!formData.personal_info.name.trim()) {
            setError('Name is required');
            return false;
        }
        if (!formData.personal_info.email.trim()) {
            setError('Email is required');
            return false;
        }
        if (!formData.personal_info.phone.trim()) {
            setError('Phone is required');
            return false;
        }
        if (!formData.professional_profile.career_goal.trim() || formData.professional_profile.career_goal.length < 10) {
            setError('Career goal is required (minimum 10 characters)');
            return false;
        }
        if (!formData.professional_profile.preferred_domain) {
            setError('Preferred domain is required');
            return false;
        }
        if (formData.education.length === 0 || !formData.education[0].degree.trim()) {
            setError('At least one education entry is required');
            return false;
        }
        if (formData.skills.length === 0) {
            setError('At least one skill is required');
            return false;
        }
        if (formData.projects.length === 0 || !formData.projects[0].title.trim()) {
            setError('At least one project is required');
            return false;
        }
        return true;
    };

    const handleGenerateContent = async () => {
        setError('');
        if (!validateForm()) return;
        setIsGenerating(true);
        try {
            const response = await resumeAPI.generateContent(formData);
            setGeneratedContent(response.data.content); // Store AI content

            // Set default styles based on template
            if (formData.template_type === 'fresher') {
                setStyleOptions({
                    header_alignment: 'center',
                    body_alignment: 'center',
                    font_family: 'Arial',
                    font_size: 'medium', // small, medium, large
                    font_color: '#000000'
                });
            } else if (formData.template_type === 'technical') {
                setStyleOptions({
                    header_alignment: 'left',
                    body_alignment: 'left',
                    font_family: 'Calibri',
                    font_size: 'medium',
                    font_color: '#000000'
                });
            } else { // general
                setStyleOptions({
                    header_alignment: 'center',
                    body_alignment: 'left',
                    font_family: 'Times New Roman',
                    font_size: 'medium',
                    font_color: '#000000'
                });
            }

            setIsReviewing(true); // Switch to review mode
        } catch (err) {
            console.error('[Resume Creator] Error:', err);
            setError('Failed to generate content. Please try again.');
        } finally {
            setIsGenerating(false);
        }
    };

    const handleDownload = async () => {
        setIsSaving(true);
        try {
            // Construct clean user_data strictly for backend
            const userData = {
                personal_info: formData.personal_info,
                education: formData.education,
                skills: formData.skills,
                projects: formData.projects, // Descriptions here are ignored by template in favor of ai_content
                experience: formData.experience, // Same for bullets
                certifications: formData.certifications,
                target_role: formData.target_role,
                references: formData.references,
                professional_profile: formData.professional_profile,
                template_type: formData.template_type
            };

            const response = await resumeAPI.download(userData, generatedContent, formData.template_type, styleOptions);

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${formData.personal_info.name.replace(/ /g, '_')}_Resume.docx`);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);

            // Optional: reset or stay? Stay is better.
        } catch (err) {
            console.error('Download Error:', err);
            setError('Failed to download resume.');
        } finally {
            setIsSaving(false);
        }
    };

    // Review Component (Visual Editor)
    if (isReviewing && generatedContent) {
        return (
            <ResumePreview
                formData={formData}
                generatedContent={generatedContent}
                templateType={formData.template_type}
                onUpdateContent={setGeneratedContent}
                onUpdateStyle={setStyleOptions}
                onDownload={handleDownload}
                onBack={() => setIsReviewing(false)}
                isSaving={isSaving}
                styleOptions={styleOptions}
            />
        );
    }

    // Default Form Render
    return (
        <div className="space-y-6">
            {/* Info Banner - Clarify Tool Purpose */}
            <div className="bg-blue-50 border-l-4 border-blue-500 rounded-xl p-6">
                <div className="flex items-start">
                    <div className="flex-shrink-0">
                        <AlertCircle className="h-6 w-6 text-blue-600" />
                    </div>
                    <div className="ml-3">
                        <h3 className="text-sm font-bold text-blue-900 mb-1">
                            About This Tool
                        </h3>
                        <p className="text-sm text-blue-800">
                            This tool formats your resume using ATS-friendly templates. <strong>You provide the content</strong> — we handle the professional structure and layout. The quality of your resume depends on the details you enter below.
                        </p>
                    </div>
                </div>
            </div>

            {/* Template Selection */}
            <div className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Choose Resume Template</h3>
                <p className="text-sm text-gray-600 mb-2">Select a template that best matches your profile</p>
                <p className="text-xs text-gray-500 mb-6 italic">💡 You provide the content. This tool formats your resume in an ATS-friendly layout.</p>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Fresher Template */}
                    <div
                        onClick={() => {
                            setSelectedTemplate('fresher');
                            setFormData({ ...formData, template_type: 'fresher' });
                        }}
                        className={`p-6 rounded-xl border-2 cursor-pointer transition-all ${selectedTemplate === 'fresher'
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:border-blue-300'
                            }`}
                    >
                        <div className="flex items-center justify-between mb-3">
                            <h4 className="font-bold text-gray-900">Fresher / Student</h4>
                            {selectedTemplate === 'fresher' && (
                                <span className="text-blue-500">✓</span>
                            )}
                        </div>
                        <p className="text-sm text-gray-600 mb-3">
                            Best for students and recent graduates
                        </p>
                        <ul className="text-xs text-gray-500 space-y-1">
                            <li>• Education first</li>
                            <li>• Projects emphasized</li>
                            <li>• Skills highlighted</li>
                        </ul>
                    </div>

                    {/* Technical Template */}
                    <div
                        onClick={() => {
                            setSelectedTemplate('technical');
                            setFormData({ ...formData, template_type: 'technical' });
                        }}
                        className={`p-6 rounded-xl border-2 cursor-pointer transition-all ${selectedTemplate === 'technical'
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:border-blue-300'
                            }`}
                    >
                        <div className="flex items-center justify-between mb-3">
                            <h4 className="font-bold text-gray-900">Technical / Software</h4>
                            {selectedTemplate === 'technical' && (
                                <span className="text-blue-500">✓</span>
                            )}
                        </div>
                        <p className="text-sm text-gray-600 mb-3">
                            Ideal for technical and software roles
                        </p>
                        <ul className="text-xs text-gray-500 space-y-1">
                            <li>• Technical skills first</li>
                            <li>• Projects with depth</li>
                            <li>• Experience highlighted</li>
                        </ul>
                    </div>

                    {/* General Template */}
                    <div
                        onClick={() => {
                            setSelectedTemplate('general');
                            setFormData({ ...formData, template_type: 'general' });
                        }}
                        className={`p-6 rounded-xl border-2 cursor-pointer transition-all ${selectedTemplate === 'general'
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:border-blue-300'
                            }`}
                    >
                        <div className="flex items-center justify-between mb-3">
                            <h4 className="font-bold text-gray-900">General Professional</h4>
                            {selectedTemplate === 'general' && (
                                <span className="text-blue-500">✓</span>
                            )}
                        </div>
                        <p className="text-sm text-gray-600 mb-3">
                            Balanced approach for all professionals
                        </p>
                        <ul className="text-xs text-gray-500 space-y-1">
                            <li>• Experience first</li>
                            <li>• Balanced sections</li>
                            <li>• Achievement-focused</li>
                        </ul>
                    </div>
                </div>
            </div>

            {/* Professional Profile */}
            <div className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Professional Profile</h3>
                <p className="text-sm text-gray-600 mb-6">Help us create a personalized summary for you</p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Current Status *</label>
                        <select
                            value={formData.professional_profile.current_status}
                            onChange={(e) => setFormData({
                                ...formData,
                                professional_profile: {
                                    ...formData.professional_profile,
                                    current_status: e.target.value,
                                    years_of_experience: e.target.value === 'student' || e.target.value === 'fresher' ? 0 : formData.professional_profile.years_of_experience
                                }
                            })}
                            className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                        >
                            <option value="student">Student</option>
                            <option value="fresher">Fresher</option>
                            <option value="working_professional">Working Professional</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Years of Experience</label>
                        <input
                            type="number"
                            min="0"
                            max="50"
                            value={formData.professional_profile.years_of_experience}
                            onChange={(e) => setFormData({
                                ...formData,
                                professional_profile: {
                                    ...formData.professional_profile,
                                    years_of_experience: parseInt(e.target.value) || 0
                                }
                            })}
                            disabled={formData.professional_profile.current_status === 'student' || formData.professional_profile.current_status === 'fresher'}
                            className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none disabled:opacity-50"
                        />
                    </div>

                    <div className="md:col-span-2">
                        <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Domain *</label>
                        <select
                            value={formData.professional_profile.preferred_domain}
                            onChange={(e) => setFormData({
                                ...formData,
                                professional_profile: {
                                    ...formData.professional_profile,
                                    preferred_domain: e.target.value
                                }
                            })}
                            className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                        >
                            <option value="">Select a domain</option>
                            <option value="AI/ML">AI/ML</option>
                            <option value="Web Development">Web Development</option>
                            <option value="Mobile Development">Mobile Development</option>
                            <option value="Data Science">Data Science</option>
                            <option value="DevOps">DevOps</option>
                            <option value="Cloud Computing">Cloud Computing</option>
                            <option value="Cybersecurity">Cybersecurity</option>
                            <option value="QA/Testing">QA/Testing</option>
                            <option value="Full Stack Development">Full Stack Development</option>
                            <option value="Backend Development">Backend Development</option>
                            <option value="Frontend Development">Frontend Development</option>
                        </select>
                    </div>

                    <div className="md:col-span-2">
                        <label className="block text-sm font-medium text-gray-700 mb-2">Career Goal * (10-200 characters)</label>
                        <textarea
                            value={formData.professional_profile.career_goal}
                            onChange={(e) => setFormData({
                                ...formData,
                                professional_profile: {
                                    ...formData.professional_profile,
                                    career_goal: e.target.value.slice(0, 200)
                                }
                            })}
                            placeholder="e.g., Seeking a challenging role in AI/ML to leverage my skills in building intelligent systems"
                            className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none resize-none"
                            rows="3"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                            {formData.professional_profile.career_goal.length}/200 characters
                        </p>
                    </div>
                </div>
            </div>

            {/* Personal Information */}
            <div className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Personal Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        type="text"
                        placeholder="Full Name *"
                        value={formData.personal_info.name}
                        onChange={(e) => handlePersonalInfoChange('name', e.target.value)}
                        className="p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <input
                        type="email"
                        placeholder="Email *"
                        value={formData.personal_info.email}
                        onChange={(e) => handlePersonalInfoChange('email', e.target.value)}
                        className="p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <input
                        type="tel"
                        placeholder="Phone *"
                        value={formData.personal_info.phone}
                        onChange={(e) => handlePersonalInfoChange('phone', e.target.value)}
                        className="p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <input
                        type="text"
                        placeholder="LinkedIn URL (optional)"
                        value={formData.personal_info.linkedin}
                        onChange={(e) => handlePersonalInfoChange('linkedin', e.target.value)}
                        className="p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <input
                        type="text"
                        placeholder="GitHub URL (optional)"
                        value={formData.personal_info.github}
                        onChange={(e) => handlePersonalInfoChange('github', e.target.value)}
                        className="p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                </div>
            </div>

            {/* Education */}
            <div className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-bold text-gray-900">Education</h3>
                    <button onClick={addEducation} className="flex items-center text-blue-600 hover:text-blue-700 font-semibold">
                        <Plus className="h-4 w-4 mr-1" /> Add
                    </button>
                </div>
                {formData.education.map((edu, index) => (
                    <div key={index} className="mb-4 p-4 bg-gray-50 rounded-xl relative">
                        {formData.education.length > 1 && (
                            <button onClick={() => removeEducation(index)} className="absolute top-2 right-2 text-red-500 hover:text-red-700">
                                <Trash2 className="h-4 w-4" />
                            </button>
                        )}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <input
                                type="text"
                                placeholder="Degree *"
                                value={edu.degree}
                                onChange={(e) => updateEducation(index, 'degree', e.target.value)}
                                className="p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                            <input
                                type="text"
                                placeholder="Institution *"
                                value={edu.institution}
                                onChange={(e) => updateEducation(index, 'institution', e.target.value)}
                                className="p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                            <input
                                type="text"
                                placeholder="Year *"
                                value={edu.year}
                                onChange={(e) => updateEducation(index, 'year', e.target.value)}
                                className="p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                            <input
                                type="text"
                                placeholder="GPA (optional)"
                                value={edu.gpa}
                                onChange={(e) => updateEducation(index, 'gpa', e.target.value)}
                                className="p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                        </div>
                    </div>
                ))}
            </div>

            {/* Skills */}
            <div className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Skills</h3>
                <div className="flex gap-2 mb-4">
                    <input
                        type="text"
                        placeholder="Add a skill (e.g., Python, React)"
                        value={skillInput}
                        onChange={(e) => setSkillInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && addSkill()}
                        className="flex-1 p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <button onClick={addSkill} className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700">
                        Add
                    </button>
                </div>
                <div className="flex flex-wrap gap-2">
                    {formData.skills.map((skill, index) => (
                        <span key={index} className="inline-flex items-center px-3 py-1 bg-blue-50 text-blue-700 rounded-lg text-sm font-medium">
                            {skill}
                            <button onClick={() => removeSkill(index)} className="ml-2 text-blue-500 hover:text-blue-700">
                                ×
                            </button>
                        </span>
                    ))}
                </div>
            </div>

            {/* Projects */}
            <div className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-bold text-gray-900">Projects</h3>
                    <button onClick={addProject} className="flex items-center text-blue-600 hover:text-blue-700 font-semibold">
                        <Plus className="h-4 w-4 mr-1" /> Add
                    </button>
                </div>
                {formData.projects.map((project, index) => (
                    <div key={index} className="mb-4 p-4 bg-gray-50 rounded-xl relative">
                        {formData.projects.length > 1 && (
                            <button onClick={() => removeProject(index)} className="absolute top-2 right-2 text-red-500 hover:text-red-700">
                                <Trash2 className="h-4 w-4" />
                            </button>
                        )}
                        <div className="space-y-3">
                            <input
                                type="text"
                                placeholder="Project Title *"
                                value={project.title}
                                onChange={(e) => updateProject(index, 'title', e.target.value)}
                                className="w-full p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                            <textarea
                                placeholder="Project Description *"
                                value={project.description}
                                onChange={(e) => updateProject(index, 'description', e.target.value)}
                                rows="3"
                                className="w-full p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                            <input
                                type="text"
                                placeholder="Technologies Used (optional)"
                                value={project.technologies}
                                onChange={(e) => updateProject(index, 'technologies', e.target.value)}
                                className="w-full p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                        </div>
                    </div>
                ))}
            </div>

            {/* Experience (Optional) */}
            <div className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-bold text-gray-900">Experience <span className="text-sm text-gray-500">(Optional)</span></h3>
                    <button onClick={addExperience} className="flex items-center text-blue-600 hover:text-blue-700 font-semibold">
                        <Plus className="h-4 w-4 mr-1" /> Add
                    </button>
                </div>
                {formData.experience.map((exp, index) => (
                    <div key={index} className="mb-4 p-4 bg-gray-50 rounded-xl relative">
                        <button onClick={() => removeExperience(index)} className="absolute top-2 right-2 text-red-500 hover:text-red-700">
                            <Trash2 className="h-4 w-4" />
                        </button>
                        <div className="space-y-3">
                            <input
                                type="text"
                                placeholder="Role"
                                value={exp.role}
                                onChange={(e) => updateExperience(index, 'role', e.target.value)}
                                className="w-full p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                            <input
                                type="text"
                                placeholder="Company"
                                value={exp.company}
                                onChange={(e) => updateExperience(index, 'company', e.target.value)}
                                className="w-full p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                            <input
                                type="text"
                                placeholder="Duration (e.g., Jan 2023 - Present)"
                                value={exp.duration}
                                onChange={(e) => updateExperience(index, 'duration', e.target.value)}
                                className="w-full p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                            <textarea
                                placeholder="Responsibilities"
                                value={exp.responsibilities}
                                onChange={(e) => updateExperience(index, 'responsibilities', e.target.value)}
                                rows="3"
                                className="w-full p-2 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                        </div>
                    </div>
                ))}
            </div>

            {/* Certifications (Optional) */}
            <div className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Certifications <span className="text-sm text-gray-500">(Optional)</span></h3>
                {/* ... existing cert code ... */}
                <div className="flex gap-2 mb-4">
                    <input
                        type="text"
                        placeholder="Add certification"
                        value={certInput}
                        onChange={(e) => setCertInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && addCertification()}
                        className="flex-1 p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <button onClick={addCertification} className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700">
                        Add
                    </button>
                </div>
                <div className="space-y-2">
                    {formData.certifications.map((cert, index) => (
                        <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                            <span className="text-sm">{cert}</span>
                            <button onClick={() => removeCertification(index)} className="text-red-500 hover:text-red-700">
                                <Trash2 className="h-4 w-4" />
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            {/* References (New Section) */}
            <div className="bg-white rounded-[2rem] shadow-xl p-8 border border-gray-100">
                <h3 className="text-xl font-bold text-gray-900 mb-4">References <span className="text-sm text-gray-500">(Optional)</span></h3>
                <p className="text-sm text-gray-600 mb-4">Add specific references or leave empty/add "Available upon request"</p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                    <input
                        type="text"
                        placeholder="Name *"
                        value={refInput.name}
                        onChange={(e) => setRefInput({ ...refInput, name: e.target.value })}
                        className="p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <input
                        type="text"
                        placeholder="Designation"
                        value={refInput.designation}
                        onChange={(e) => setRefInput({ ...refInput, designation: e.target.value })}
                        className="p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <input
                        type="text"
                        placeholder="Organization"
                        value={refInput.organization}
                        onChange={(e) => setRefInput({ ...refInput, organization: e.target.value })}
                        className="p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <input
                        type="text"
                        placeholder="Contact (Email/Phone)"
                        value={refInput.contact}
                        onChange={(e) => setRefInput({ ...refInput, contact: e.target.value })}
                        className="p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                    <div className="md:col-span-2">
                        <button onClick={addReference} className="w-full py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 flex items-center justify-center">
                            <Plus className="h-4 w-4 mr-2" /> Add Reference
                        </button>
                    </div>
                </div>

                <div className="space-y-3">
                    {formData.references.map((ref, index) => (
                        <div key={index} className="p-4 bg-gray-50 rounded-xl relative border border-gray-200">
                            <button onClick={() => removeReference(index)} className="absolute top-4 right-4 text-red-500 hover:text-red-700">
                                <Trash2 className="h-4 w-4" />
                            </button>
                            <h4 className="font-bold text-gray-900">{ref.name}</h4>
                            <div className="text-sm text-gray-600">
                                {ref.designation && <span>{ref.designation}</span>}
                                {ref.organization && <span> at {ref.organization}</span>}
                            </div>
                            {ref.contact && <div className="text-sm text-gray-500 mt-1">{ref.contact}</div>}
                        </div>
                    ))}
                </div>
            </div>

            {/* Error Display */}
            {error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700">
                    {error}
                </div>
            )}

            {/* Helper Note */}
            <div className="bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-100 rounded-xl p-4">
                <div className="flex items-center text-sm text-indigo-800">
                    <Wand2 className="h-4 w-4 mr-2 text-indigo-600" />
                    <span><strong>Next Step:</strong> AI will help structure your content professionally and format it in an ATS-friendly layout.</span>
                </div>
            </div>

            {/* Generate Button */}
            <button
                onClick={handleGenerateContent}
                disabled={isGenerating}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 rounded-xl font-bold hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg transition-all transform hover:-translate-y-1"
            >
                {isGenerating ? (
                    <span className="flex items-center justify-center">
                        <Loader2 className="animate-spin h-5 w-5 mr-2" />
                        Generating Resume...
                    </span>
                ) : (
                    <span className="flex items-center justify-center">
                        <Sparkles className="h-5 w-5 mr-2" />
                        Generate Professional Resume
                        <FileDown className="h-5 w-5 ml-2" />
                    </span>
                )}
            </button>
        </div>
    );
};

export default ResumeCreator;
