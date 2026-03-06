import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

const SettingsLayout = ({ title, description, children }) => {
    const navigate = useNavigate();

    return (
        <div className="container mx-auto px-4 py-8 max-w-4xl">
            <div className="mb-8 flex items-center justify-between">
                <div>
                    <button
                        onClick={() => navigate('/')}
                        className="flex items-center text-slate-500 hover:text-blue-600 transition-colors mb-2 text-sm font-medium"
                    >
                        <ArrowLeft className="w-4 h-4 mr-1" />
                        Back to Dashboard
                    </button>
                    <h1 className="text-3xl font-bold text-slate-900">{title}</h1>
                    {description && <p className="text-slate-500 mt-1">{description}</p>}
                </div>
            </div>

            <div className="bg-white rounded-3xl shadow-xl shadow-blue-900/5 border border-slate-100 overflow-hidden">
                {children}
            </div>
        </div>
    );
};

export default SettingsLayout;
