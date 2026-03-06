import React from 'react';
import SettingsLayout from '../../components/Settings/SettingsLayout';
import { FileText, Bookmark, Info, Scale } from 'lucide-react';

const TermsOfService = () => {
    const sections = [
        {
            title: "1. Usage Rules",
            icon: Bookmark,
            content: "AceIt is an educational platform designed for placement preparation. Any misuse of the platform, including automated scraping, intentional overloading of servers, or distribution of copyrighted material, may lead to account termination."
        },
        {
            title: "2. Student Responsibilities",
            icon: Info,
            content: "Users are responsible for maintaining the confidentiality of their login credentials. All activity under a specific account is the legal responsibility of the registered user."
        },
        {
            title: "3. Data Usage & AI Analysis",
            icon: FileText,
            content: "By using AceIt, you consent to our AI processing of your practice data (including text, audio, and video inputs) for the purpose of providing feedback. We do not use your individual data for training large language models without prior anonymization."
        },
        {
            title: "4. Disclaimer",
            icon: Scale,
            content: "AceIt is a tool intended to assist in preparation. We do not guarantee job placements or final results in external examinations. The scores provided by our AI are analytical estimates of current performance levels."
        }
    ];

    return (
        <SettingsLayout
            title="Terms of Service"
            description="The rules and responsibilities for using the AceIt platform."
        >
            <div className="p-8 pb-16">
                <div className="max-w-3xl mx-auto space-y-12">
                    {/* Main Content */}
                    <section className="prose prose-slate max-w-none">
                        <p className="text-slate-600 leading-relaxed text-lg">
                            Welcome to AceIt. By accessing our platform, you agree to comply with and be bound by the following terms and conditions of use. Please read these terms carefully.
                        </p>
                    </section>

                    <div className="grid gap-10">
                        {sections.map((section, idx) => {
                            const Icon = section.icon;
                            return (
                                <div key={idx} className="flex space-x-6">
                                    <div className="flex-shrink-0">
                                        <div className="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center">
                                            <Icon className="w-7 h-7" />
                                        </div>
                                    </div>
                                    <div className="pt-1">
                                        <h3 className="text-xl font-bold text-slate-900 mb-3">{section.title}</h3>
                                        <p className="text-slate-600 leading-relaxed">
                                            {section.content}
                                        </p>
                                    </div>
                                </div>
                            );
                        })}
                    </div>

                    {/* Acceptable Use Policy Table */}
                    <section className="pt-10 border-t border-slate-100">
                        <h2 className="text-2xl font-bold text-slate-900 mb-6">Acceptable Usage Policy</h2>
                        <div className="overflow-hidden rounded-3xl border border-slate-100 bg-white">
                            <table className="min-w-full divide-y divide-slate-100">
                                <thead className="bg-slate-50">
                                    <tr>
                                        <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Action</th>
                                        <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-slate-100 text-sm">
                                    {[
                                        { action: 'Multiple Account Creation', status: 'Prohibited' },
                                        { action: 'Mock Interview Recording sharing', status: 'Restricted' },
                                        { action: 'Third-party API access', status: 'Strictly Prohibited' },
                                        { action: 'Course Content Distribution', status: 'Prohibited' },
                                    ].map((row, i) => (
                                        <tr key={i}>
                                            <td className="px-6 py-4 whitespace-nowrap text-slate-700 font-medium">{row.action}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-red-600 font-bold">{row.status}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </section>

                    <div className="text-center pt-8 border-t border-slate-100">
                        <p className="text-slate-400 text-xs">Last Updated: March 2026 • AceIt v1.0.0</p>
                    </div>
                </div>
            </div>
        </SettingsLayout>
    );
};

export default TermsOfService;
