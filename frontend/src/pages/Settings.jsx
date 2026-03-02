import React, { useState } from 'react';
import { User, Bell, Moon, Sun, Shield, Key, Mail, Smartphone, Save } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Settings = () => {
    const { user } = useAuth();
    const [activeTab, setActiveTab] = useState('account');

    const tabs = [
        { id: 'account', label: 'Account', icon: User },
        { id: 'appearance', label: 'Appearance', icon: Moon },
        { id: 'notifications', label: 'Notifications', icon: Bell },
        { id: 'security', label: 'Security', icon: Shield },
    ];

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div>
                <h2 className="text-3xl font-bold text-white tracking-tight">Settings</h2>
                <p className="text-text-secondary mt-1">
                    Manage your account preferences and application settings.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                {/* Sidebar Navigation */}
                <div className="lg:col-span-1 space-y-2">
                    {tabs.map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium text-sm ${activeTab === tab.id
                                    ? 'bg-primary/10 text-primary ring-1 ring-primary/50'
                                    : 'text-text-secondary hover:bg-surface hover:text-white'
                                }`}
                        >
                            <tab.icon className="w-5 h-5" />
                            {tab.label}
                        </button>
                    ))}
                </div>

                {/* Content Area */}
                <div className="lg:col-span-3">
                    <div className="bg-surface border border-border rounded-2xl p-8 shadow-lg shadow-black/20">
                        {activeTab === 'account' && (
                            <div className="space-y-8">
                                <div className="flex items-center gap-6 pb-8 border-b border-border">
                                    <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-primary via-primary/80 to-indigo-600 flex items-center justify-center shadow-xl">
                                        <span className="text-4xl font-bold text-white">
                                            {(user?.username?.[0] || 'G').toUpperCase()}
                                        </span>
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-bold text-white">{user?.full_name || 'Guest User'}</h3>
                                        <p className="text-text-secondary">{user?.email || 'guest@example.com'}</p>
                                        <button className="mt-3 px-4 py-2 bg-bg border border-border rounded-lg text-xs font-semibold text-text hover:text-white hover:border-primary/50 transition-all">
                                            Change Avatar
                                        </button>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium text-text-secondary">Full Name</label>
                                        <div className="relative">
                                            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary" />
                                            <input
                                                type="text"
                                                defaultValue={user?.full_name}
                                                className="w-full pl-10 pr-4 py-2.5 bg-bg border border-border rounded-xl text-text focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50"
                                            />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium text-text-secondary">Email Address</label>
                                        <div className="relative">
                                            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary" />
                                            <input
                                                type="email"
                                                defaultValue={user?.email}
                                                className="w-full pl-10 pr-4 py-2.5 bg-bg border border-border rounded-xl text-text focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50"
                                            />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium text-text-secondary">Username</label>
                                        <input
                                            type="text"
                                            defaultValue={user?.username}
                                            disabled
                                            className="w-full px-4 py-2.5 bg-bg/50 border border-border/50 rounded-xl text-text-secondary cursor-not-allowed"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium text-text-secondary">Phone Number</label>
                                        <div className="relative">
                                            <Smartphone className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary" />
                                            <input
                                                type="tel"
                                                placeholder="+1 (555) 000-0000"
                                                className="w-full pl-10 pr-4 py-2.5 bg-bg border border-border rounded-xl text-text focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50"
                                            />
                                        </div>
                                    </div>
                                </div>

                                <div className="flex justify-end pt-4">
                                    <button className="flex items-center gap-2 px-6 py-2.5 bg-primary text-bg font-bold rounded-xl hover:brightness-110 shadow-lg shadow-primary/25 transition-all">
                                        <Save className="w-4 h-4" />
                                        Save Changes
                                    </button>
                                </div>
                            </div>
                        )}

                        {activeTab === 'appearance' && (
                            <div className="space-y-8">
                                <div>
                                    <h3 className="text-lg font-bold text-white mb-4">Theme Preferences</h3>
                                    <div className="grid grid-cols-3 gap-4">
                                        {[
                                            { name: 'Light', icon: Sun },
                                            { name: 'Dark', icon: Moon },
                                            { name: 'System', icon: Smartphone }
                                        ].map((theme) => (
                                            <button key={theme.name} className={`p-4 rounded-xl border flex flex-col items-center gap-3 transition-all ${theme.name === 'Dark'
                                                    ? 'bg-primary/10 border-primary text-primary'
                                                    : 'bg-bg border-border text-text-secondary hover:border-text-secondary'
                                                }`}>
                                                <theme.icon className="w-6 h-6" />
                                                <span className="font-medium">{theme.name}</span>
                                            </button>
                                        ))}
                                    </div>
                                </div>
                                <div className="border-t border-border pt-6">
                                    <h3 className="text-lg font-bold text-white mb-4">Interface Density</h3>
                                    <p className="text-text-secondary text-sm">Adjust the spacing of the application interface.</p>
                                </div>
                            </div>
                        )}

                        {/* Other tabs placeholders */}
                        {(activeTab === 'notifications' || activeTab === 'security') && (
                            <div className="flex flex-col items-center justify-center py-12 text-center">
                                <div className="p-4 bg-surface border border-border rounded-full mb-4">
                                    <Shield className="w-8 h-8 text-primary" />
                                </div>
                                <h3 className="text-lg font-bold text-white">Coming Soon</h3>
                                <p className="text-text-secondary max-w-sm mt-2">
                                    This section is currently under development. Check back later for updates.
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;
