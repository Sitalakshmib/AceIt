import React, { useState, useEffect } from 'react';
import { AlignLeft, AlignCenter, AlignRight, Download, ChevronLeft } from 'lucide-react';

const ResumePreview = ({
    formData,
    generatedContent,
    templateType = 'general', // fresher, technical, general
    onUpdateContent, // function to update generatedContent
    onUpdateStyle, // function to update style options
    onDownload,
    onBack,
    isSaving,
    styleOptions: propsStyleOptions = {}
}) => {
    // Local state for style options (synced with parent later on download)
    const [styleOptions, setStyleOptions] = useState({
        header_alignment: templateType === 'fresher' ? 'center' : 'left',
        body_alignment: templateType === 'fresher' ? 'center' : 'left',
        font_family: 'Arial',
        font_size: 'medium',
        font_color: '#000000',
        ...propsStyleOptions // Merge passed props
    });

    // Update parent style options when changed
    useEffect(() => {
        onUpdateStyle(styleOptions);
    }, [styleOptions, onUpdateStyle]);

    // Handle text edits
    const handleSummaryEdit = (newText) => {
        onUpdateContent({ ...generatedContent, summary: newText });
    };

    const handleExperienceEdit = (index, bulletIndex, newText) => {
        const newExp = [...generatedContent.experience];
        newExp[index].bullets[bulletIndex] = newText;
        onUpdateContent({ ...generatedContent, experience: newExp });
    };

    const handleProjectEdit = (index, descIndex, newText) => {
        const newProj = [...generatedContent.projects];
        newProj[index].description[descIndex] = newText;
        onUpdateContent({ ...generatedContent, projects: newProj });
    };

    // Color Palette
    const colorPalette = [
        '#000000', // Black
        '#1a1a1a', // Dark Gray
        '#003366', // Dark Blue
        '#002147', // Oxford Blue
        '#2C3E50', // Midnight Blue
        '#1B4F72', // Dark Cerulean
        '#5D6D7E', // Slate Blue
        '#4A235A', // Dark Purple
        '#7B241C', // Dark Red
        '#145A32', // Dark Green
    ];

    // Font Options
    const fontOptions = [
        { label: 'Arial', value: 'Arial' },
        { label: 'Calibri', value: 'Calibri' }, // Maps to sans-serif fallback often
        { label: 'Times New Roman', value: 'Times New Roman' },
        { label: 'Helvetica', value: 'Helvetica' },
        { label: 'Georgia', value: 'Georgia' },
        { label: 'Verdana', value: 'Verdana' },
    ];

    // Toolbar Component
    const Toolbar = () => (
        <div className="fixed bottom-8 left-1/2 transform -translate-x-1/2 bg-white shadow-2xl rounded-2xl px-6 py-3 flex items-center gap-6 border border-gray-200 z-50 flex-wrap justify-center">

            {/* Font Family */}
            <div className="flex flex-col gap-1">
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Font</span>
                <select
                    value={styleOptions.font_family}
                    onChange={(e) => setStyleOptions(prev => ({ ...prev, font_family: e.target.value }))}
                    className="p-1.5 rounded-lg border border-gray-200 text-sm focus:ring-2 focus:ring-blue-500 outline-none bg-gray-50"
                >
                    {fontOptions.map(font => (
                        <option key={font.value} value={font.value}>{font.label}</option>
                    ))}
                </select>
            </div>

            {/* Font Size */}
            <div className="flex flex-col gap-1">
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Size</span>
                <div className="flex bg-gray-100 rounded-lg p-1">
                    <button
                        onClick={() => setStyleOptions(prev => ({ ...prev, font_size: 'small' }))}
                        className={`px-3 py-1 rounded-md text-sm transition-all ${styleOptions.font_size === 'small' ? 'bg-white shadow text-blue-600 font-bold' : 'text-gray-500 hover:text-gray-700'}`}
                    >
                        S
                    </button>
                    <button
                        onClick={() => setStyleOptions(prev => ({ ...prev, font_size: 'medium' }))}
                        className={`px-3 py-1 rounded-md text-sm transition-all ${styleOptions.font_size === 'medium' ? 'bg-white shadow text-blue-600 font-bold' : 'text-gray-500 hover:text-gray-700'}`}
                    >
                        M
                    </button>
                    <button
                        onClick={() => setStyleOptions(prev => ({ ...prev, font_size: 'large' }))}
                        className={`px-3 py-1 rounded-md text-sm transition-all ${styleOptions.font_size === 'large' ? 'bg-white shadow text-blue-600 font-bold' : 'text-gray-500 hover:text-gray-700'}`}
                    >
                        L
                    </button>
                </div>
            </div>

            {/* Font Color */}
            <div className="flex flex-col gap-1">
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Color</span>
                <div className="flex gap-1.5">
                    {colorPalette.slice(0, 5).map(color => (
                        <button
                            key={color}
                            onClick={() => setStyleOptions(prev => ({ ...prev, font_color: color }))}
                            className={`w-6 h-6 rounded-full border border-gray-200 transition-transform hover:scale-110 ${styleOptions.font_color === color ? 'ring-2 ring-offset-2 ring-blue-500 scale-110' : ''}`}
                            style={{ backgroundColor: color }}
                            title={color}
                        />
                    ))}
                    {/* Simple expandable or just showing first 5 for now to keep toolbar clean */}
                </div>
            </div>

            <div className="w-px h-8 bg-gray-200 mx-2"></div>

            {/* Alignment Controls */}
            <div className="flex flex-col gap-1">
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Body Align</span>
                <div className="flex gap-1">
                    <button
                        onClick={() => setStyleOptions(prev => ({ ...prev, body_alignment: 'left' }))}
                        className={`p-1.5 rounded hover:bg-gray-100 ${styleOptions.body_alignment === 'left' ? 'text-blue-600 bg-blue-50' : 'text-gray-600'}`}
                        title="Align Left"
                    >
                        <AlignLeft size={16} />
                    </button>
                    <button
                        onClick={() => setStyleOptions(prev => ({ ...prev, body_alignment: 'center' }))}
                        className={`p-1.5 rounded hover:bg-gray-100 ${styleOptions.body_alignment === 'center' ? 'text-blue-600 bg-blue-50' : 'text-gray-600'}`}
                        title="Align Center"
                    >
                        <AlignCenter size={16} />
                    </button>
                    <button
                        onClick={() => setStyleOptions(prev => ({ ...prev, body_alignment: 'right' }))}
                        className={`p-1.5 rounded hover:bg-gray-100 ${styleOptions.body_alignment === 'right' ? 'text-blue-600 bg-blue-50' : 'text-gray-600'}`}
                        title="Align Right"
                    >
                        <AlignRight size={16} />
                    </button>
                </div>
            </div>
            <div className="flex flex-col gap-1">
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Header Align</span>
                <div className="flex gap-1">
                    <button
                        onClick={() => setStyleOptions(prev => ({ ...prev, header_alignment: 'left' }))}
                        className={`p-1.5 rounded hover:bg-gray-100 ${styleOptions.header_alignment === 'left' ? 'text-blue-600 bg-blue-50' : 'text-gray-600'}`}
                        title="Align Left"
                    >
                        <AlignLeft size={16} />
                    </button>
                    <button
                        onClick={() => setStyleOptions(prev => ({ ...prev, header_alignment: 'center' }))}
                        className={`p-1.5 rounded hover:bg-gray-100 ${styleOptions.header_alignment === 'center' ? 'text-blue-600 bg-blue-50' : 'text-gray-600'}`}
                        title="Align Center"
                    >
                        <AlignCenter size={16} />
                    </button>
                    <button
                        onClick={() => setStyleOptions(prev => ({ ...prev, header_alignment: 'right' }))}
                        className={`p-1.5 rounded hover:bg-gray-100 ${styleOptions.header_alignment === 'right' ? 'text-blue-600 bg-blue-50' : 'text-gray-600'}`}
                        title="Align Right"
                    >
                        <AlignRight size={16} />
                    </button>
                </div>
            </div>
        </div>
    );

    // CSS Classes based on template
    const containerClass = "max-w-[210mm] min-h-[297mm] mx-auto bg-white shadow-2xl p-[20mm] text-gray-900 transition-all duration-300";
    // Construct dynamic styles
    const previewStyles = {
        fontFamily: styleOptions.font_family,
        fontSize: styleOptions.font_size === 'small' ? '0.85rem' : styleOptions.font_size === 'large' ? '1.05rem' : '0.95rem',
        // We do NOT apply color to the whole body, only headers usually.
    };

    // Helper to get header style
    const headerStyle = {
        color: styleOptions.font_color
    };

    // Dynamic text alignment classes
    const bodyAlignClass = styleOptions.body_alignment === 'center' ? 'text-center' : styleOptions.body_alignment === 'right' ? 'text-right' : 'text-left';
    const headerAlignClass = styleOptions.header_alignment === 'center' ? 'text-center' : styleOptions.header_alignment === 'right' ? 'text-right' : 'text-left';
    // For lists in center mode, we remove bullets usually, or keep them with list-inside?
    // list-inside helps with centering.
    const listClass = styleOptions.body_alignment === 'center' ? 'list-none' : 'list-disc ml-4';

    return (
        <div className="bg-gray-100 min-h-screen p-8 relative pb-32">
            <Toolbar />

            {/* Top Navigation */}
            <div className="flex justify-between items-center mb-6 max-w-[210mm] mx-auto">
                <button onClick={onBack} className="flex items-center text-gray-600 hover:text-gray-900">
                    <ChevronLeft size={20} /> Back to Form
                </button>
                <button
                    onClick={onDownload}
                    disabled={isSaving}
                    className="flex items-center bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                    <Download size={18} className="mr-2" />
                    {isSaving ? 'Generating...' : 'Download Resume'}
                </button>
            </div>

            {/* A4 Page View */}
            <div className={`${containerClass}`} style={previewStyles}>

                {/* Header */}
                <div className={`mb-6 ${headerAlignClass} border-b-2 border-gray-800 pb-4`}>
                    <h1 className="text-4xl font-bold uppercase tracking-wider mb-2" style={headerStyle} contentEditable suppressContentEditableWarning>
                        {formData.personal_info.name}
                    </h1>
                    <div className="text-sm text-gray-600 space-x-2">
                        <span>{formData.personal_info.email}</span>
                        <span>|</span>
                        <span>{formData.personal_info.phone}</span>
                        {formData.personal_info.linkedin && (
                            <><span>|</span><span>{formData.personal_info.linkedin}</span></>
                        )}
                    </div>
                </div>

                {/* Summary */}
                <div className={`mb-6 ${bodyAlignClass}`}>
                    <h2 className={`text-lg font-bold uppercase mb-2 ${headerAlignClass}`} style={{ ...headerStyle, color: styleOptions.font_color || '#1e3a8a' }}>Professional Profile</h2>
                    <div
                        className="outline-none focus:bg-blue-50 p-1 rounded"
                        contentEditable
                        suppressContentEditableWarning
                        onBlur={(e) => handleSummaryEdit(e.target.innerText)}
                    >
                        {generatedContent.summary}
                    </div>
                </div>

                {/* Skills */}
                <div className={`mb-6 ${bodyAlignClass}`}>
                    <h2 className={`text-lg font-bold uppercase mb-2 ${headerAlignClass}`} style={{ ...headerStyle, color: styleOptions.font_color || '#1e3a8a' }}>Skills</h2>
                    <p>{formData?.skills?.join(", ") || 'No skills listed'}</p>
                </div>

                {/* Experience */}
                <div className="mb-6">
                    <h2 className={`text-lg font-bold uppercase mb-2 ${headerAlignClass}`} style={{ ...headerStyle, color: styleOptions.font_color || '#1e3a8a' }}>Experience</h2>
                    {(generatedContent?.experience || []).map((exp, i) => (
                        <div key={i} className={`mb-4 ${bodyAlignClass}`}>
                            <div className="font-bold text-gray-800">{exp.role} | {exp.company}</div>
                            <ul className={`${listClass} mt-1 text-gray-700`}>
                                {(exp.bullets || []).map((bullet, j) => (
                                    <li key={j} className="mb-1">
                                        <div
                                            className="outline-none focus:bg-blue-50 p-1 rounded"
                                            contentEditable
                                            suppressContentEditableWarning
                                            onBlur={(e) => handleExperienceEdit(i, j, e.target.innerText)}
                                        >
                                            {bullet}
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>

                {/* Projects */}
                <div className="mb-6">
                    <h2 className={`text-lg font-bold uppercase mb-2 ${headerAlignClass}`} style={{ ...headerStyle, color: styleOptions.font_color || '#1e3a8a' }}>Projects</h2>
                    {(generatedContent?.projects || []).map((proj, i) => (
                        <div key={i} className={`mb-4 ${bodyAlignClass}`}>
                            <div className="font-bold text-gray-800">{proj.title}</div>
                            <ul className={`${listClass} mt-1 text-gray-700`}>
                                {(proj.description || []).map((desc, j) => (
                                    <li key={j} className="mb-1">
                                        <div
                                            className="outline-none focus:bg-blue-50 p-1 rounded"
                                            contentEditable
                                            suppressContentEditableWarning
                                            onBlur={(e) => handleProjectEdit(i, j, e.target.innerText)}
                                        >
                                            {desc}
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>

                {/* Education - Read Only from form for now */}
                <div className={`mb-6 ${bodyAlignClass}`}>
                    <h2 className={`text-lg font-bold uppercase mb-2 ${headerAlignClass}`} style={{ ...headerStyle, color: styleOptions.font_color || '#1e3a8a' }}>Education</h2>
                    {(formData?.education || []).map((edu, i) => (
                        <div key={i} className="mb-2">
                            <div className="font-bold">{edu.institution}</div>
                            <div>{edu.degree} <span className="italic text-gray-500">({edu.year})</span></div>
                        </div>
                    ))}
                </div>

                {/* References */}
                {(formData?.references?.length || 0) > 0 && (
                    <div className={`mb-6 ${bodyAlignClass}`}>
                        <h2 className={`text-lg font-bold uppercase mb-2 ${headerAlignClass}`} style={{ ...headerStyle, color: styleOptions.font_color || '#1e3a8a' }}>References</h2>
                        {formData.references.map((ref, i) => (
                            <div key={i} className="mb-2">
                                <span className="font-bold">{ref.name}</span>
                                {(ref.designation || ref.organization) && (
                                    <span>, {ref.designation} {ref.organization && `at ${ref.organization}`}</span>
                                )}
                                {ref.contact && <div className="text-gray-600 text-sm">{ref.contact}</div>}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div className="text-center mt-8 text-gray-500 pb-20">
                Tip: Click on any text to edit it. Use the toolbar below to change alignment.
            </div>
        </div>
    );
};

export default ResumePreview;
