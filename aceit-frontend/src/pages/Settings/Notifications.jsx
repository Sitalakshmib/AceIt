import React from 'react';
import SettingsLayout from '../../components/Settings/SettingsLayout';
import { useSettings } from '../../contexts/SettingsContext';
import { Bell, Mail, Clock, ShieldCheck } from 'lucide-react';

const Notifications = () => {
    const { settings, updateSettings } = useSettings();

    const toggleSetting = (id) => {
        updateSettings(`notifications.${id}`, !settings.notifications[id]);
    };

    const notificationSections = [
        {
            title: "Practice Alerts",
            items: [
                { id: 'practiceReminders', label: 'Daily Practice Reminders', desc: 'Get reminded to complete your daily aptitude and coding tasks.', icon: Bell },
                { id: 'interviewReminders', label: 'Interview Reminders', desc: 'Alerts for scheduled mock interview sessions.', icon: Clock },
            ]
        },
        {
            title: "Reports & Updates",
            items: [
                { id: 'weeklyReports', label: 'Weekly Progress Reports', desc: 'Receive a summary of your performance every Monday.', icon: ShieldCheck },
                { id: 'systemAnnouncements', label: 'System Announcements', desc: 'Stay updated with new features and platform improvements.', icon: Bell },
            ]
        },
        {
            title: "Delivery Methods",
            items: [
                { id: 'emailNotifications', label: 'Email Notifications', desc: 'Receive the above alerts via your registered email address.', icon: Mail },
            ]
        }
    ];

    return (
        <SettingsLayout
            title="Notifications"
            description="Manage how and when you receive alerts from AceIt."
        >
            <div className="p-8">
                <div className="space-y-10">
                    {notificationSections.map((section, idx) => (
                        <div key={idx} className="space-y-4">
                            <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider pl-1">
                                {section.title}
                            </h3>
                            <div className="space-y-3">
                                {section.items.map((item) => {
                                    const Icon = item.icon;
                                    const isChecked = settings.notifications[item.id];
                                    return (
                                        <div
                                            key={item.id}
                                            className="flex items-center justify-between p-4 rounded-2xl border border-slate-50 bg-slate-50/50 hover:bg-slate-50 transition-colors"
                                        >
                                            <div className="flex items-start space-x-4">
                                                <div className={`mt-1 p-2 rounded-xl ${isChecked ? 'bg-blue-100 text-blue-600' : 'bg-slate-200 text-slate-500'}`}>
                                                    <Icon className="w-5 h-5" />
                                                </div>
                                                <div>
                                                    <p className="font-semibold text-slate-800">{item.label}</p>
                                                    <p className="text-sm text-slate-500 max-w-md">{item.desc}</p>
                                                </div>
                                            </div>
                                            <button
                                                onClick={() => toggleSetting(item.id)}
                                                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 focus:outline-none ${isChecked ? 'bg-blue-600' : 'bg-slate-300'
                                                    }`}
                                            >
                                                <span
                                                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200 ${isChecked ? 'translate-x-6' : 'translate-x-1'
                                                        }`}
                                                />
                                            </button>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    ))}

                    <div className="pt-6 border-t border-slate-100">
                        <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider pl-1 mb-4">
                            Reminder Schedule
                        </h3>
                        <div className="flex items-center space-x-4 p-4 rounded-2xl bg-blue-50/50 border border-blue-100/50">
                            <div className="p-2 bg-blue-100 text-blue-600 rounded-xl">
                                <Clock className="w-5 h-5" />
                            </div>
                            <div className="flex-1">
                                <p className="font-semibold text-blue-900 text-sm">Preferred Reminder Time</p>
                                <p className="text-xs text-blue-700">Set the daily time for your practice alerts.</p>
                            </div>
                            <input
                                type="time"
                                value={settings.notifications.reminderTime}
                                onChange={(e) => updateSettings('notifications.reminderTime', e.target.value)}
                                className="bg-white border border-blue-200 text-blue-900 text-sm rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </SettingsLayout>
    );
};

export default Notifications;
