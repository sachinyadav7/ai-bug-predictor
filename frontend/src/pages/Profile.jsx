import React from 'react';
import { User, Mail, Shield, Calendar, Award, Star, Settings, ExternalLink } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';

const Profile = () => {
    const { user } = useAuth();

    const stats = [
        { label: 'Analyses Run', value: '124', icon: Star, color: 'text-primary' },
        { label: 'Issues Found', value: '38', icon: Award, color: 'text-success' },
        { label: 'Security Score', value: '98%', icon: Shield, color: 'text-accent' },
    ];

    return (
        <div className="max-w-6xl mx-auto space-y-8 p-4">
            {/* Header / Banner */}
            <div className="relative h-64 rounded-3xl overflow-hidden bg-surface border border-border group">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-surface to-bg"></div>
                <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10"></div>
                
                <div className="absolute -bottom-12 left-12 flex items-end gap-6 z-10">
                    <div className="w-32 h-32 rounded-3xl bg-gradient-to-br from-primary to-indigo-600 border-4 border-bg flex items-center justify-center shadow-2xl shadow-primary/30">
                        <span className="text-white text-5xl font-bold">
                            {(user?.username?.[0] || 'G').toUpperCase()}
                        </span>
                    </div>
                </div>

                <div className="absolute bottom-6 right-8">
                    <button className="px-6 py-2.5 bg-white/5 backdrop-blur-md border border-white/10 rounded-xl text-white text-sm font-medium hover:bg-white/10 transition-all flex items-center gap-2">
                        <Settings className="w-4 h-4" />
                        Edit Profile
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pt-6">
                {/* Left Column: User Info */}
                <div className="space-y-6">
                    <div className="p-8 rounded-3xl bg-surface/50 border border-border backdrop-blur-xl space-y-6">
                        <div>
                            <h1 className="text-2xl font-bold text-white">{user?.full_name || 'User Name'}</h1>
                            <p className="text-primary font-medium">@{user?.username || 'username'}</p>
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-center gap-3 text-text-secondary group">
                                <div className="p-2 rounded-lg bg-bg border border-border group-hover:border-primary/50 transition-colors">
                                    <Mail className="w-4 h-4" />
                                </div>
                                <span className="text-sm">{user?.email || 'not connected'}</span>
                            </div>
                            <div className="flex items-center gap-3 text-text-secondary group">
                                <div className="p-2 rounded-lg bg-bg border border-border group-hover:border-primary/50 transition-colors">
                                    <Calendar className="w-4 h-4" />
                                </div>
                                <span className="text-sm">Joined March 2024</span>
                            </div>
                            <div className="flex items-center gap-3 text-text-secondary group">
                                <div className="p-2 rounded-lg bg-bg border border-border group-hover:border-primary/50 transition-colors">
                                    <Shield className="w-4 h-4" />
                                </div>
                                <span className="text-sm">{user?.is_admin ? 'Administrator' : 'Standard User'}</span>
                            </div>
                        </div>

                        <div className="pt-4 border-t border-border">
                            <p className="text-xs text-text-secondary leading-relaxed uppercase tracking-widest font-bold mb-4">Bio</p>
                            <p className="text-sm text-text leading-relaxed italic">
                                &quot;Obsessed with clean code and unbreakable security. Using BugPredictor to automate the boring stuff.&quot;
                            </p>
                        </div>
                    </div>

                    <div className="p-8 rounded-3xl bg-gradient-to-br from-primary/10 to-transparent border border-primary/20">
                        <h3 className="text-sm font-bold text-white mb-2">Account Status</h3>
                        <div className="flex items-center justify-between">
                            <span className="text-xs text-text-secondary">Pro Subscription</span>
                            <span className="px-2 py-1 bg-primary/20 text-primary text-[10px] uppercase font-bold rounded">Active</span>
                        </div>
                    </div>
                </div>

                {/* Right Column: Stats & Activity */}
                <div className="lg:col-span-2 space-y-8">
                    {/* Stats Grid */}
                    <div className="grid grid-cols-3 gap-6">
                        {stats.map((stat, i) => (
                            <motion.div
                                key={stat.label}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: i * 0.1 }}
                                className="p-6 rounded-3xl bg-surface/50 border border-border backdrop-blur-md flex flex-col items-center text-center group hover:border-primary/50 transition-all hover:-translate-y-1"
                            >
                                <div className={`p-3 rounded-2xl bg-bg border border-border mb-4 ${stat.color}`}>
                                    <stat.icon className="w-6 h-6" />
                                </div>
                                <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                                <div className="text-xs text-text-secondary font-medium uppercase tracking-wider">{stat.label}</div>
                            </motion.div>
                        ))}
                    </div>

                    {/* Recent Achievements / Badges */}
                    <div className="p-8 rounded-3xl bg-surface/50 border border-border backdrop-blur-xl">
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-lg font-bold text-white">Recent Achievements</h2>
                            <button className="text-xs text-primary font-bold flex items-center gap-1 hover:underline">
                                View All <ExternalLink className="w-3 h-3" />
                            </button>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {[
                                { title: 'Bug Hunter', desc: 'Identified 10 dangerous security flaws', date: '2 days ago' },
                                { title: 'Clean Coder', desc: 'Maintained 95%+ security score for 7 days', date: 'last week' }
                            ].map((achievement) => (
                                <div key={achievement.title} className="p-4 rounded-2xl bg-bg/50 border border-border hover:border-primary/30 transition-colors flex gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                                        <Award className="w-6 h-6 text-primary" />
                                    </div>
                                    <div>
                                        <h4 className="text-sm font-bold text-white">{achievement.title}</h4>
                                        <p className="text-xs text-text-secondary mt-1">{achievement.desc}</p>
                                        <p className="text-[10px] text-primary/50 mt-2 font-mono uppercase">{achievement.date}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Profile;
