import React from 'react';
import { Bell, Search, User, LogOut } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Header = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    return (
        <header className="h-20 px-8 flex items-center justify-between bg-surface/50 backdrop-blur-xl border-b border-border sticky top-0 z-20">
            <div className="flex items-center gap-4 flex-1">
                <div className="relative w-96 group">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary group-focus-within:text-primary transition-colors" />
                    <input
                        type="text"
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                alert(`Searching for: ${e.target.value}... (Search logic isn't fully connected to backend yet!)`);
                            }
                        }}
                        placeholder="Search projects, analysis, or bugs... (Press Enter)"
                        className="w-full pl-10 pr-4 py-2.5 bg-bg/50 border border-border rounded-xl text-sm text-text focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50 transition-all placeholder:text-text-secondary/50"
                    />
                </div>
            </div>

            <div className="flex items-center gap-6">
                <button className="p-2.5 text-text-secondary hover:text-white hover:bg-white/5 rounded-xl transition-all relative group">
                    <Bell className="w-5 h-5" />
                    <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-red-500 rounded-full animate-pulse shadow-lg shadow-red-500/50"></span>
                </button>

                <div className="h-8 w-px bg-border/50"></div>

                <div 
                    className="flex items-center gap-3 cursor-pointer group hover:bg-white/5 p-2 rounded-xl transition-all"
                    onClick={() => navigate('/profile')}
                >
                    <div className="text-right hidden md:block">
                        <p className="text-sm font-bold text-white group-hover:text-primary transition-colors">{user?.full_name || user?.username || 'Guest User'}</p>
                        <p className="text-xs text-text-secondary font-medium">{user?.is_guest ? 'Guest Access' : 'Pro Member'}</p>
                    </div>
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary via-primary/80 to-indigo-600 flex items-center justify-center shadow-lg shadow-primary/20 border border-white/10 group-hover:scale-105 transition-transform">
                        <span className="text-white font-bold text-lg">
                            {(user?.username?.[0] || 'G').toUpperCase()}
                        </span>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;
