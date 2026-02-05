import React from 'react';

/**
 * Circular Progress Indicator for Scores
 */
export const ScoreCircle = ({ score, size = 120, strokeWidth = 8, label = "Score" }) => {
    const radius = (size - strokeWidth) / 2;
    const circumference = radius * 2 * Math.PI;
    const offset = circumference - (score / 100) * circumference;

    // Color based on score
    const getColor = () => {
        if (score >= 80) return '#10b981'; // green
        if (score >= 60) return '#f59e0b'; // yellow
        return '#ef4444'; // red
    };

    return (
        <div className="relative inline-flex items-center justify-center">
            <svg width={size} height={size} className="transform -rotate-90">
                {/* Background circle */}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke="#e5e7eb"
                    strokeWidth={strokeWidth}
                    fill="none"
                />
                {/* Progress circle */}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke={getColor()}
                    strokeWidth={strokeWidth}
                    fill="none"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    strokeLinecap="round"
                    className="transition-all duration-1000 ease-out"
                />
            </svg>
            {/* Score text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-2xl font-bold" style={{ color: getColor() }}>
                    {Math.round(score)}%
                </span>
                <span className="text-xs text-gray-500">{label}</span>
            </div>
        </div>
    );
};

/**
 * Score Badge with Rating
 */
export const ScoreBadge = ({ score }) => {
    const getRating = () => {
        if (score >= 85) return { text: 'Excellent', color: 'bg-green-100 text-green-800 border-green-300' };
        if (score >= 70) return { text: 'Good', color: 'bg-blue-100 text-blue-800 border-blue-300' };
        if (score >= 55) return { text: 'Fair', color: 'bg-yellow-100 text-yellow-800 border-yellow-300' };
        return { text: 'Needs Work', color: 'bg-red-100 text-red-800 border-red-300' };
    };

    const rating = getRating();

    return (
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold border ${rating.color}`}>
            {rating.text}
        </span>
    );
};

/**
 * Section Header with Icon
 */
export const SectionHeader = ({ icon, title, subtitle, children }) => {
    return (
        <div className="flex items-center justify-between mb-4 pb-3 border-b-2 border-gray-200">
            <div className="flex items-center">
                <span className="text-3xl mr-3">{icon}</span>
                <div>
                    <h3 className="text-xl font-bold text-gray-800">{title}</h3>
                    {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
                </div>
            </div>
            {children}
        </div>
    );
};

/**
 * Skill Tag with Color Coding
 */
export const SkillTag = ({ skill, matched = true }) => {
    return (
        <span
            className={`inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-medium ${matched
                ? 'bg-green-100 text-green-800 border border-green-300'
                : 'bg-red-50 text-red-700 border border-red-200'
                }`}
        >
            {matched ? (
                <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                    <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                    />
                </svg>
            ) : (
                <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                    <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                        clipRule="evenodd"
                    />
                </svg>
            )}
            {skill}
        </span>
    );
};

/**
 * Metric Card for displaying key metrics
 */
export const MetricCard = ({ icon, label, value, color = 'blue', subtitle }) => {
    const bgColors = {
        blue: 'bg-blue-50',
        green: 'bg-green-50',
        purple: 'bg-purple-50',
        orange: 'bg-orange-50',
        red: 'bg-red-50',
        yellow: 'bg-yellow-50'
    };

    const textColors = {
        blue: 'text-blue-600',
        green: 'text-green-600',
        purple: 'text-purple-600',
        orange: 'text-orange-600',
        red: 'text-red-600',
        yellow: 'text-yellow-600'
    };

    return (
        <div className={`${bgColors[color]} rounded-lg p-5 border border-${color}-200 hover:shadow-md transition-shadow`}>
            <div className="flex items-center justify-between mb-2">
                <span className="text-2xl">{icon}</span>
                <span className={`text-3xl font-bold ${textColors[color]}`}>{value}</span>
            </div>
            <div className={`font-medium ${textColors[color]}`}>{label}</div>
            {subtitle && <div className="text-xs text-gray-600 mt-1">{subtitle}</div>}
        </div>
    );
};

/**
 * Enhanced Progress Bar with Label
 */
export const ProgressBar = ({ label, current, max = 100, showPercentage = true }) => {
    const percentage = (current / max) * 100;

    const getColor = () => {
        if (percentage >= 80) return 'bg-green-500';
        if (percentage >= 60) return 'bg-yellow-500';
        return 'bg-red-500';
    };

    return (
        <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">{label}</span>
                <span className="text-sm font-semibold text-gray-900">
                    {showPercentage ? `${Math.round(percentage)}%` : `${current}/${max}`}
                </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                    className={`h-3 rounded-full ${getColor()} transition-all duration-700 ease-out`}
                    style={{ width: `${Math.min(100, percentage)}%` }}
                />
            </div>
        </div>
    );
};

/**
 * Insight Card for displaying feedback and suggestions
 */
export const InsightCard = ({ type = 'info', icon, title, children }) => {
    const styles = {
        success: {
            bg: 'bg-green-50',
            border: 'border-green-100',
            title: 'text-green-800',
            icon: ''
        },
        warning: {
            bg: 'bg-orange-50',
            border: 'border-orange-100',
            title: 'text-orange-800',
            icon: ''
        },
        info: {
            bg: 'bg-blue-50',
            border: 'border-blue-100',
            title: 'text-blue-800',
            icon: ''
        },
        error: {
            bg: 'bg-red-50',
            border: 'border-red-100',
            title: 'text-red-800',
            icon: ''
        }
    };

    const style = styles[type];

    return (
        <div className={`${style.bg} border ${style.border} rounded-lg p-4 mb-3`}>
            <div className="flex items-start">
                <span className="text-xl mr-3 flex-shrink-0">{icon || style.icon}</span>
                <div className="flex-1">
                    {title && <h4 className={`font-semibold ${style.title} mb-2`}>{title}</h4>}
                    <div className="text-sm text-gray-700">{children}</div>
                </div>
            </div>
        </div>
    );
};

/**
 * Mini Progress Indicator for sub-scores
 */
export const MiniProgress = ({ label, value, max, color = 'blue' }) => {
    const percentage = (value / max) * 100;

    const colors = {
        blue: { bg: 'bg-blue-500', text: 'text-blue-700' },
        green: { bg: 'bg-green-500', text: 'text-green-700' },
        purple: { bg: 'bg-purple-500', text: 'text-purple-700' },
        orange: { bg: 'bg-orange-500', text: 'text-orange-700' },
        yellow: { bg: 'bg-yellow-500', text: 'text-yellow-700' }
    };

    return (
        <div className="mb-3">
            <div className="flex justify-between items-center mb-1">
                <span className="text-xs font-medium text-gray-600">{label}</span>
                <span className={`text-xs font-bold ${colors[color].text}`}>{value}/{max}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                    className={`h-2 rounded-full ${colors[color].bg} transition-all duration-500`}
                    style={{ width: `${Math.min(100, percentage)}%` }}
                />
            </div>
        </div>
    );
};

/**
 * Empty State Component
 */
export const EmptyState = ({ icon, title, description, features }) => {
    return (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">{icon}</div>
            <h3 className="text-2xl font-bold text-gray-700 mb-3">{title}</h3>
            <p className="text-gray-500 mb-6">{description}</p>
            {features && (
                <div className="grid grid-cols-2 gap-4 mt-8 text-sm text-gray-600">
                    {features.map((feature, index) => (
                        <div key={index} className="flex items-center justify-center">
                            <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path
                                    fillRule="evenodd"
                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                    clipRule="evenodd"
                                />
                            </svg>
                            {feature}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

/**
 * Strength/Weakness Card - Enhanced display for AI analysis
 */
export const StrengthWeaknessCard = ({ type = 'strength', items, title }) => {
    const isStrength = type === 'strength';

    // Helper to render text with markdown bold
    const renderTextWithBold = (text) => {
        if (!text) return null;
        const parts = text.split(/(\*\*.*?\*\*)/g);
        return parts.map((part, index) => {
            if (part.startsWith('**') && part.endsWith('**')) {
                const boldText = part.slice(2, -2);
                return <strong key={index} className="font-bold">{boldText}</strong>;
            }
            return <span key={index}>{part}</span>;
        });
    };

    const config = {
        strength: {
            gradient: 'from-emerald-500 to-green-600',
            bgGradient: 'from-emerald-50 to-green-50',
            border: 'border-emerald-200',
            icon: '',
            iconBg: 'bg-gradient-to-br from-emerald-500 to-green-600',
            textColor: 'text-emerald-900',
            itemBg: 'bg-white',
            itemBorder: 'border-emerald-100',
            bulletColor: 'text-emerald-600'
        },
        weakness: {
            gradient: 'from-amber-500 to-orange-600',
            bgGradient: 'from-amber-50 to-orange-50',
            border: 'border-amber-200',
            icon: '!',
            iconBg: 'bg-gradient-to-br from-amber-500 to-orange-600',
            textColor: 'text-amber-900',
            itemBg: 'bg-white',
            itemBorder: 'border-amber-100',
            bulletColor: 'text-amber-600'
        }
    };

    const style = config[type];

    if (!items || items.length === 0) return null;

    return (
        <div className={`bg-gradient-to-br ${style.bgGradient} rounded-xl shadow-lg border-2 ${style.border} p-6 hover:shadow-xl transition-all duration-300`}>
            {/* Header */}
            <div className="flex items-center mb-5">
                <div className={`w-12 h-12 ${style.iconBg} rounded-full flex items-center justify-center text-white font-bold text-xl shadow-md mr-4`}>
                    {style.icon}
                </div>
                <div>
                    <h4 className={`text-xl font-bold ${style.textColor}`}>
                        {title || (isStrength ? 'Key Strengths' : 'Areas for Improvement')}
                    </h4>
                    <p className="text-sm text-gray-600">{items.length} {isStrength ? 'strengths' : 'areas'} identified</p>
                </div>
            </div>

            {/* Items List */}
            <div className="space-y-3">
                {items.map((item, index) => (
                    <div
                        key={index}
                        className={`${style.itemBg} rounded-lg p-4 border ${style.itemBorder} hover:shadow-md transition-shadow duration-200`}
                    >
                        <div className="flex items-start">
                            <span className={`${style.bulletColor} font-bold mr-3 text-lg flex-shrink-0`}>
                                {index + 1}.
                            </span>
                            <p className="text-gray-700 leading-relaxed flex-1">{renderTextWithBold(item)}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

/**
 * AI Insight Panel - Enhanced container for AI-powered analysis
 */
export const AIInsightPanel = ({ children, title = "AI-Powered Insights" }) => {
    return (
        <div className="relative bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 rounded-2xl shadow-xl border-2 border-purple-200 p-8 overflow-hidden">
            {/* Decorative background pattern */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-purple-200/20 to-blue-200/20 rounded-full blur-3xl -mr-32 -mt-32"></div>
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-blue-200/20 to-indigo-200/20 rounded-full blur-3xl -ml-32 -mb-32"></div>

            {/* Content */}
            <div className="relative z-10">
                {/* Header with AI Badge */}
                <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-purple-200">
                    <div className="flex items-center">
                        <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg mr-4 group-hover:scale-110 transition-transform">
                        </div>
                        <div>
                            <h3 className="text-2xl font-bold text-purple-900">{title}</h3>
                            <p className="text-sm text-purple-600 font-medium">Powered by Gemini AI</p>
                        </div>
                    </div>
                    <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-2 rounded-full text-xs font-bold shadow-md">
                        AI ANALYSIS
                    </div>
                </div>

                {/* Content */}
                <div className="space-y-6">
                    {children}
                </div>
            </div>
        </div>
    );
};

/**
 * AI Section Card - Individual sections within AI panel
 */
export const AISectionCard = ({ icon, title, children, color = 'blue' }) => {
    const colors = {
        blue: 'bg-blue-50 border-blue-200 text-blue-900',
        green: 'bg-green-50 border-green-200 text-green-900',
        purple: 'bg-purple-50 border-purple-200 text-purple-900',
        gray: 'bg-gray-50 border-gray-200 text-gray-900'
    };

    return (
        <div className={`${colors[color]} rounded-xl p-5 border-2 shadow-sm`}>
            <div className="flex items-center mb-3">
                <span className="text-2xl mr-3">{icon}</span>
                <h4 className="font-bold text-lg">{title}</h4>
            </div>
            <div className="text-gray-700 leading-relaxed">
                {children}
            </div>
        </div>
    );
};

