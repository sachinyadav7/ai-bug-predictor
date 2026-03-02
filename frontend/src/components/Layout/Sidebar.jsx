import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Code, History, Settings, Bug, LogOut } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import clsx from 'clsx';

const Sidebar = () => {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
        { icon: Code, label: 'Analyze', path: '/analyze' },
        { icon: History, label: 'History', path: '/history' },
        { icon: Settings, label: 'Settings', path: '/settings' },
    ];

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <aside className="w-72 h-screen bg-surface/50 backdrop-blur-xl border-r border-border flex flex-col sticky top-0">
            <div className="p-8 flex items-center gap-3">
                <div className="p-2.5 bg-gradient-to-br from-primary to-primary/50 rounded-xl shadow-lg shadow-primary/20">
                    <Bug className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h1 className="text-xl font-bold tracking-tight text-white leading-none">BugPredictor</h1>
                    <p className="text-xs text-primary font-medium mt-1">AI-Powered Security</p>
                </div>
            </div>

            <nav className="flex-1 px-6 space-y-2 mt-4">
                <div className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-4 px-4">Menu</div>
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            clsx(
                                'flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all duration-300 group',
                                isActive
                                    ? 'bg-gradient-to-r from-primary/20 to-primary/5 text-primary font-medium border-l-2 border-primary'
                                    : 'text-text-secondary hover:bg-white/5 hover:text-white hover:translate-x-1'
                            )
                        }
                    >
                        <item.icon className={clsx("w-5 h-5 transition-colors", ({ isActive }) => isActive ? "text-primary" : "text-text-secondary group-hover:text-white")} />
                        <span>{item.label}</span>
                    </NavLink>
                ))}
            </nav>

            <div className="p-6 border-t border-border space-y-4">
                <button
                    onClick={handleLogout}
                    className="flex items-center gap-3 px-4 py-3 w-full rounded-xl text-text-secondary hover:bg-red-500/10 hover:text-red-400 transition-all duration-300 group"
                >
                    <LogOut className="w-5 h-5 group-hover:scale-110 transition-transform" />
                    <span>Sign Out</span>
                </button>

                <div className="p-5 rounded-2xl bg-gradient-to-br from-primary/20 via-primary/10 to-transparent border border-primary/20 relative overflow-hidden group">
                    <div className="absolute inset-0 bg-primary/5 group-hover:bg-primary/10 transition-colors" />
                    <h3 className="text-sm font-bold text-white relative z-10">Pro Plan</h3>
                    <p className="text-xs text-text-secondary mt-1 mb-3 relative z-10">Unlock advanced models & batch processing.</p>
                    <button className="w-full py-2 bg-primary text-bg font-bold rounded-lg text-xs hover:shadow-lg hover:shadow-primary/25 hover:-translate-y-0.5 transition-all relative z-10">
                        Upgrade Now
                    </button>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
