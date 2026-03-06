import React from 'react';
import SettingsLayout from '../../components/Settings/SettingsLayout';
import { useSettings } from '../../contexts/SettingsContext';
import { Sun, Moon, LayoutGrid, List, BrainCircuit, Code2, Video } from 'lucide-react';

const Preferences = () => {
    const { settings, updateSettings } = useSettings();

    return (
        <SettingsLayout
            title="Preferences"
            description="Customize your learning environment and app layout."
        >
            <div className="p-8 space-y-12">
                {/* Appearance Section */}
                <section className="space-y-6">
                    <div>
                        <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider pl-1">Appearance</h3>
                        <p className="text-xs text-slate-500 pl-1 mt-1">Choose your preferred visual theme.</p>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-center">
                        <button
                            onClick={() => updateSettings('preferences.theme', 'light')}
                            className={`p-6 rounded-3xl border-2 transition-all duration-300 ${settings.preferences.theme === 'light'
                                    ? 'border-blue-600 bg-blue-50/50 shadow-lg'
                                    : 'border-slate-100 bg-white hover:border-slate-200'
                                }`}
                        >
                            <div className={`w-12 h-12 rounded-2xl flex items-center justify-center mx-auto mb-4 ${settings.preferences.theme === 'light' ? 'bg-blue-600 text-white shadow-blue-200 shadow-lg' : 'bg-slate-100 text-slate-500'
                                }`}>
                                <Sun className="w-6 h-6" />
                            </div>
                            <span className={`font-bold text-sm ${settings.preferences.theme === 'light' ? 'text-blue-900' : 'text-slate-600'}`}>Light Mode</span>
                        </button>
                        <button
                            onClick={() => updateSettings('preferences.theme', 'dark')}
                            className={`p-6 rounded-3xl border-2 transition-all duration-300 ${settings.preferences.theme === 'dark'
                                    ? 'border-blue-600 bg-slate-900 shadow-lg'
                                    : 'border-slate-100 bg-white hover:border-slate-200'
                                }`}
                        >
                            <div className={`w-12 h-12 rounded-2xl flex items-center justify-center mx-auto mb-4 ${settings.preferences.theme === 'dark' ? 'bg-blue-600 text-white shadow-blue-900 shadow-lg' : 'bg-slate-100 text-slate-500'
                                }`}>
                                <Moon className="w-6 h-6" />
                            </div>
                            <span className={`font-bold text-sm ${settings.preferences.theme === 'dark' ? 'text-white' : 'text-slate-600'}`}>Dark Mode</span>
                        </button>
                    </div>
                </section>

                {/* Layout Section */}
                <section className="space-y-6 pt-6 border-t border-slate-100">
                    <div>
                        <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider pl-1">Dashboard Layout</h3>
                        <p className="text-xs text-slate-500 pl-1 mt-1">Control how much information is shown on your screen.</p>
                    </div>
                    <div className="flex space-x-4">
                        <button
                            onClick={() => updateSettings('preferences.dashboardLayout', 'normal')}
                            className={`flex-1 flex items-center space-x-3 p-4 rounded-2xl border-2 transition-all ${settings.preferences.dashboardLayout === 'normal'
                                    ? 'border-blue-600 bg-blue-50 overflow-hidden'
                                    : 'border-slate-100 bg-white hover:border-slate-200'
                                }`}
                        >
                            <div className={`p-2 rounded-xl ${settings.preferences.dashboardLayout === 'normal' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-400'}`}>
                                <LayoutGrid className="w-5 h-5" />
                            </div>
                            <div className="text-left">
                                <p className={`font-bold text-sm ${settings.preferences.dashboardLayout === 'normal' ? 'text-blue-900' : 'text-slate-600'}`}>Comfortable</p>
                                <p className="text-[10px] text-slate-400 leading-tight">Spacious views with full details.</p>
                            </div>
                        </button>
                        <button
                            onClick={() => updateSettings('preferences.dashboardLayout', 'compact')}
                            className={`flex-1 flex items-center space-x-3 p-4 rounded-2xl border-2 transition-all ${settings.preferences.dashboardLayout === 'compact'
                                    ? 'border-blue-600 bg-blue-50 overflow-hidden'
                                    : 'border-slate-100 bg-white hover:border-slate-200'
                                }`}
                        >
                            <div className={`p-2 rounded-xl ${settings.preferences.dashboardLayout === 'compact' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-400'}`}>
                                <List className="w-5 h-5" />
                            </div>
                            <div className="text-left">
                                <p className={`font-bold text-sm ${settings.preferences.dashboardLayout === 'compact' ? 'text-blue-900' : 'text-slate-600'}`}>Compact</p>
                                <p className="text-[10px] text-slate-400 leading-tight">Denser information density.</p>
                            </div>
                        </button>
                    </div>
                </section>

                {/* Default Experience Section */}
                <section className="space-y-6 pt-6 border-t border-slate-100">
                    <div>
                        <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider pl-1">Default Landing Module</h3>
                        <p className="text-xs text-slate-500 pl-1 mt-1">Which module would you like to see first when logging in?</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {[
                            { id: 'Dashboard', icon: LayoutGrid, label: 'Standard Dashboard' },
                            { id: 'Aptitude', icon: BrainCircuit, label: 'Aptitude Training' },
                            { id: 'Coding', icon: Code2, label: 'Coding Practice' },
                            { id: 'Interview', icon: Video, label: 'Mock Interview' },
                        ].map((module) => {
                            const Icon = module.icon;
                            const isActive = settings.preferences.defaultModule === module.id;
                            return (
                                <button
                                    key={module.id}
                                    onClick={() => updateSettings('preferences.defaultModule', module.id)}
                                    className={`flex items-center space-x-3 p-4 rounded-2xl border-2 transition-all ${isActive ? 'border-blue-600 bg-blue-50' : 'border-slate-100 bg-white hover:bg-slate-50'
                                        }`}
                                >
                                    <div className={`p-2 rounded-xl flex-shrink-0 ${isActive ? 'bg-blue-600 text-white shadow-md' : 'bg-slate-100 text-slate-400'}`}>
                                        <Icon className="w-5 h-5" />
                                    </div>
                                    <span className={`font-bold text-sm truncate ${isActive ? 'text-blue-900' : 'text-slate-600'}`}>{module.label}</span>
                                    {isActive && <div className="ml-auto w-2 h-2 rounded-full bg-blue-600" />}
                                </button>
                            );
                        })}
                    </div>
                </section>
            </div>
        </SettingsLayout>
    );
};

export default Preferences;
