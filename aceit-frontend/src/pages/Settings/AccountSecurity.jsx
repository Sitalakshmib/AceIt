import React, { useState } from 'react';
import SettingsLayout from '../../components/Settings/SettingsLayout';
import { useAuth } from '../../contexts/AuthContext';
import { Lock, Eye, EyeOff, Monitor, MapPin, Smartphone, ShieldCheck, LogOut } from 'lucide-react';

const AccountSecurity = () => {
    const { user, logout } = useAuth();
    const [showPassword, setShowPassword] = useState({ current: false, new: false, confirm: false });
    const [pwStatus, setPwStatus] = useState(null);

    const handlePasswordChange = (e) => {
        e.preventDefault();
        setPwStatus('updating');
        setTimeout(() => {
            setPwStatus('success');
            setTimeout(() => setPwStatus(null), 3000);
            e.target.reset();
        }, 1500);
    };

    const loginActivity = [
        { device: 'Chromebook / Windows', location: 'Kochi, Kerala, IN', time: 'Currently Active', icon: Monitor, current: true },
        { device: 'iPhone 13 / iOS', location: 'Bangalore, Karnataka, IN', time: '2 days ago', icon: Smartphone, current: false },
        { device: 'MacBook Pro / macOS', location: 'Kochi, Kerala, IN', time: '5 days ago', icon: Monitor, current: false },
    ];

    return (
        <SettingsLayout
            title="Account Security"
            description="Manage your password and protect your AceIt account."
        >
            <div className="p-8 space-y-12">
                {/* Change Password Section */}
                <section>
                    <div className="flex items-center space-x-3 mb-8">
                        <div className="w-10 h-10 bg-amber-100 text-amber-600 rounded-xl flex items-center justify-center">
                            <Lock className="w-5 h-5" />
                        </div>
                        <h2 className="text-xl font-bold text-slate-900">Change Password</h2>
                    </div>

                    <form onSubmit={handlePasswordChange} className="max-w-md space-y-4">
                        {['current', 'new', 'confirm'].map((field) => (
                            <div key={field} className="space-y-1.5 font-medium">
                                <label className="text-xs text-slate-500 uppercase tracking-wider pl-1 font-bold">
                                    {field === 'confirm' ? 'Confirm New Password' : `${field} Password`}
                                </label>
                                <div className="relative">
                                    <input
                                        required
                                        type={showPassword[field] ? 'text' : 'password'}
                                        placeholder={`Enter ${field} password`}
                                        className="w-full pl-4 pr-12 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(prev => ({ ...prev, [field]: !prev[field] }))}
                                        className="absolute right-4 top-3.5 text-slate-400 hover:text-slate-600"
                                    >
                                        {showPassword[field] ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                                    </button>
                                </div>
                            </div>
                        ))}

                        <button
                            type="submit"
                            disabled={pwStatus === 'updating'}
                            className={`w-full py-4 rounded-2xl font-bold transition-all mt-4 ${pwStatus === 'success'
                                ? 'bg-green-100 text-green-700'
                                : 'bg-slate-900 text-white hover:bg-black shadow-lg active:scale-[0.98]'
                                }`}
                        >
                            {pwStatus === 'updating' ? (
                                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mx-auto text-center"></div>
                            ) : pwStatus === 'success' ? (
                                "Password Updated!"
                            ) : (
                                "Update Password"
                            )}
                        </button>
                    </form>
                </section>

                {/* Two-Factor Authentication Placeholder */}
                <section className="pt-10 border-t border-slate-100">
                    <div className="flex items-center justify-between p-6 rounded-[2rem] bg-indigo-50 border border-indigo-100/50 relative overflow-hidden group">
                        <div className="flex items-start space-x-5 relative z-10">
                            <div className="w-12 h-12 bg-indigo-600 text-white rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-200 group-hover:scale-110 transition-transform">
                                <ShieldCheck className="w-6 h-6" />
                            </div>
                            <div className="max-w-md">
                                <div className="flex items-center space-x-2">
                                    <h3 className="font-bold text-indigo-900 text-lg">Two-Factor Authentication (2FA)</h3>
                                    <span className="bg-indigo-200 text-indigo-700 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">Recommended</span>
                                </div>
                                <p className="text-sm text-indigo-700/80 leading-relaxed mt-1">
                                    Add an extra layer of security to your account by requiring a code from your mobile device.
                                </p>
                            </div>
                        </div>
                        <button className="px-6 py-3 bg-white border border-indigo-200 text-indigo-600 font-bold rounded-2xl hover:bg-slate-50 transition-colors shadow-sm relative z-10">
                            Enable 2FA
                        </button>
                    </div>
                </section>
            </div>
        </SettingsLayout>
    );
};

export default AccountSecurity;
