import React from 'react';
import SettingsLayout from '../../components/Settings/SettingsLayout';
import { Shield, Eye, Lock, FileCheck, Trash2, Video } from 'lucide-react';

const DataPrivacy = () => {
    const sections = [
        {
            title: "Data Collection",
            icon: Eye,
            color: "blue",
            content: "We collect minimal data required to provide our services. This includes your email, username, and practice performance metrics. We also store the results of your aptitude tests and coding submissions to provide analytics."
        },
        {
            title: "Interview Audio & Video",
            icon: Video,
            color: "indigo",
            content: "During mock interviews, we process your audio and video streams to analyze speech patterns and body language. IMPORTANT: These recordings are processed in real-time and are NOT permanently stored on our servers. Only the resulting feedback scores and tips are saved."
        },
        {
            title: "Privacy Controls",
            icon: Lock,
            color: "purple",
            content: "You have full control over your data. We do not share your individual performance reports with third parties unless explicitly authorized (e.g., for specific placement programs)."
        },
        {
            title: "Security Measures",
            icon: Shield,
            color: "green",
            content: "We use industry-standard encryption for data in transit and at rest. Your account and practice history are protected using secure hashing algorithms."
        }
    ];

    return (
        <SettingsLayout
            title="Data Privacy"
            description="Understanding how your data is used and protected on the AceIt platform."
        >
            <div className="p-8 space-y-12">
                <div className="grid md:grid-cols-2 gap-6">
                    {sections.map((section, idx) => {
                        const Icon = section.icon;
                        return (
                            <div key={idx} className="p-6 rounded-3xl border border-slate-100 bg-white shadow-sm flex flex-col items-start">
                                <div className={`p-3 rounded-2xl bg-${section.color}-50 text-${section.color}-600 mb-5`}>
                                    <Icon className="w-6 h-6" />
                                </div>
                                <h3 className="text-lg font-bold text-slate-900 mb-3">{section.title}</h3>
                                <p className="text-slate-600 text-sm leading-relaxed">
                                    {section.content}
                                </p>
                            </div>
                        );
                    })}
                </div>

                <div className="bg-slate-900 rounded-[2.5rem] p-10 relative overflow-hidden">
                    {/* Decorative backdrop */}
                    <div className="absolute top-0 right-0 w-64 h-64 bg-blue-600/10 blur-[100px] -mr-32 -mt-32"></div>

                    <div className="relative z-10 flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-8">
                        <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center text-white flex-shrink-0 shadow-xl shadow-blue-500/20">
                            <FileCheck className="w-8 h-8" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-white mb-2">Detailed Data Usage</h2>
                            <p className="text-slate-400 text-base leading-relaxed">
                                We believe in complete transparency. Our platform uses your practice data solely to provide you with insights into your placement readiness. We do not sell your data to advertisers.
                            </p>
                        </div>
                    </div>
                </div>

                <section className="pt-8 border-t border-slate-100">
                    <div className="flex items-center justify-between p-6 rounded-3xl bg-red-50 border border-red-100">
                        <div className="flex items-start space-x-4">
                            <div className="p-3 bg-red-100 text-red-600 rounded-2xl">
                                <Trash2 className="w-6 h-6" />
                            </div>
                            <div>
                                <h3 className="font-bold text-red-900">Danger Zone</h3>
                                <p className="text-sm text-red-700/80 max-w-md">
                                    Once you delete your account, your practice history, performance analytics, and resume score will be permanently erased. This action cannot be undone.
                                </p>
                            </div>
                        </div>
                        <button className="px-6 py-3 bg-white border border-red-200 text-red-600 font-bold rounded-2xl hover:bg-red-50 transition-colors shadow-sm">
                            Delete Account
                        </button>
                    </div>
                </section>
            </div>
        </SettingsLayout>
    );
};

export default DataPrivacy;
