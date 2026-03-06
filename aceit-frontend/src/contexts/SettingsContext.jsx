import React, { createContext, useState, useContext, useEffect } from 'react';

const SettingsContext = createContext();

export const SettingsProvider = ({ children }) => {
    const [settings, setSettings] = useState(() => {
        const saved = localStorage.getItem('aceit_settings');
        return saved ? JSON.parse(saved) : {
            notifications: {
                practiceReminders: true,
                interviewReminders: true,
                weeklyReports: true,
                systemAnnouncements: true,
                emailNotifications: false,
                reminderTime: '09:00'
            },
            preferences: {
                theme: 'light',
                dashboardLayout: 'normal',
                defaultModule: 'Dashboard'
            }
        };
    });

    useEffect(() => {
        localStorage.setItem('aceit_settings', JSON.stringify(settings));
        // Apply theme to document
        if (settings.preferences.theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [settings]);

    const updateSettings = (key, value) => {
        setSettings(prev => {
            const keys = key.split('.');
            if (keys.length === 2) {
                return {
                    ...prev,
                    [keys[0]]: {
                        ...prev[keys[0]],
                        [keys[1]]: value
                    }
                };
            }
            return { ...prev, [key]: value };
        });
    };

    return (
        <SettingsContext.Provider value={{ settings, updateSettings }}>
            {children}
        </SettingsContext.Provider>
    );
};

export const useSettings = () => useContext(SettingsContext);
