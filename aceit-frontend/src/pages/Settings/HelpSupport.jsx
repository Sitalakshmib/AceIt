import React, { useState } from 'react';
import SettingsLayout from '../../components/Settings/SettingsLayout';
import { HelpCircle, ChevronDown, ChevronUp, Send, User, Mail, MessageSquare } from 'lucide-react';

const HelpSupport = () => {
    const [openFaq, setOpenFaq] = useState(null);
    const [formStatus, setFormStatus] = useState(null);

    const faqs = [
        {
            q: "How does the Mock Interview work?",
            a: "AceIt uses AI to simulate a real interview environment. You can choose between HR and Technical rounds. The system analyzes your responses using voice and video to provide detailed performance feedback."
        },
        {
            q: "Is my personal data safe?",
            a: "Yes. Raw audio and video from your practice sessions are processed for feedback and not permanently stored. We only keep aggregated analytics to show your growth over time."
        },
        {
            q: "Can I use the resume analyzer multiple times?",
            a: "Absolutely! You can upload different versions of your resume or tailor it for specific job roles to see how your score changes."
        },
        {
            q: "How is my aptitude proficiency calculated?",
            a: "We use an adaptive scoring system that considers not just correct answers, but also the difficulty levels of questions and the time you spend on them."
        }
    ];

    const handleSubmit = (e) => {
        e.preventDefault();
        setFormStatus('sending');
        // Simulate API call
        setTimeout(() => {
            setFormStatus('success');
            e.target.reset();
        }, 1500);
    };

    return (
        <SettingsLayout
            title="Help & Support"
            description="Get help with the platform or contact our team."
        >
            <div className="p-8 space-y-12">
                {/* FAQ Section */}
                <section>
                    <div className="flex items-center space-x-3 mb-6 pl-1">
                        <HelpCircle className="w-6 h-6 text-blue-600" />
                        <h2 className="text-xl font-bold text-slate-900">Frequently Asked Questions</h2>
                    </div>
                    <div className="grid gap-4">
                        {faqs.map((faq, idx) => (
                            <div
                                key={idx}
                                className="rounded-2xl border border-slate-100 overflow-hidden bg-white shadow-sm hover:shadow-md transition-shadow"
                            >
                                <button
                                    onClick={() => setOpenFaq(openFaq === idx ? null : idx)}
                                    className="w-full flex items-center justify-between p-5 text-left bg-white hover:bg-slate-50 transition-colors"
                                >
                                    <span className="font-semibold text-slate-800 pr-4">{faq.q}</span>
                                    {openFaq === idx ? <ChevronUp className="w-5 h-5 text-slate-400" /> : <ChevronDown className="w-5 h-5 text-slate-400" />}
                                </button>
                                {openFaq === idx && (
                                    <div className="p-5 pt-0 text-slate-600 text-sm leading-relaxed border-t border-slate-50">
                                        {faq.a}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </section>

                {/* Contact Form Section */}
                <section className="pt-10 border-t border-slate-100">
                    <div className="grid md:grid-cols-2 gap-12">
                        <div>
                            <h2 className="text-xl font-bold text-slate-900 mb-4">Contact Support</h2>
                            <p className="text-slate-500 text-sm leading-relaxed mb-6">
                                Need more help? Send us a message and our support team will get back to you within 24 hours.
                            </p>

                            <div className="space-y-4">
                                <div className="flex items-center space-x-4 p-4 rounded-2xl bg-blue-50/50 border border-blue-100/30">
                                    <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center text-blue-600">
                                        <Mail className="w-5 h-5" />
                                    </div>
                                    <div>
                                        <p className="text-xs text-blue-700 font-medium">Email Support</p>
                                        <p className="text-sm font-semibold text-blue-900">karthikajayachandran12@gmail.com</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="relative">
                                <User className="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
                                <input
                                    required
                                    type="text"
                                    placeholder="Full Name"
                                    className="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all"
                                />
                            </div>
                            <div className="relative">
                                <Mail className="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
                                <input
                                    required
                                    type="email"
                                    placeholder="Email Address"
                                    className="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all"
                                />
                            </div>
                            <div className="relative">
                                <MessageSquare className="absolute left-4 top-4 w-5 h-5 text-slate-400" />
                                <textarea
                                    required
                                    rows="4"
                                    placeholder="Your Message"
                                    className="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm transition-all"
                                ></textarea>
                            </div>

                            <button
                                type="submit"
                                disabled={formStatus === 'sending' || formStatus === 'success'}
                                className={`w-full flex items-center justify-center space-x-2 py-4 rounded-2xl font-bold transition-all ${formStatus === 'success'
                                    ? 'bg-green-100 text-green-700 cursor-default'
                                    : 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-200 active:scale-[0.98]'
                                    }`}
                            >
                                {formStatus === 'sending' ? (
                                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                                ) : formStatus === 'success' ? (
                                    <><span>Message Sent!</span></>
                                ) : (
                                    <>
                                        <Send className="w-5 h-5" />
                                        <span>Send Message</span>
                                    </>
                                )}
                            </button>
                        </form>
                    </div>
                </section>
            </div>
        </SettingsLayout>
    );
};

export default HelpSupport;
