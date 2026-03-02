import React from 'react';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

const StatCard = ({ title, value, trend, trendValue, icon: Icon, color }) => {
    const isUp = trend === 'up';

    return (
        <div className="p-6 rounded-2xl bg-surface border border-border hover:border-primary/50 transition-all duration-300 group shadow-lg shadow-black/20 hover:shadow-primary/5 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity transform group-hover:scale-110 duration-500">
                <Icon className={`w-16 h-16 ${color}`} />
            </div>

            <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                    <div className={`p-3 rounded-xl bg-bg border border-white/5 ${color.replace('text-', 'bg-').replace('500', '500/10')}`}>
                        <Icon className={`w-6 h-6 ${color}`} />
                    </div>
                    {trendValue && (
                        <div className={`flex items-center gap-1 text-xs font-bold px-2.5 py-1 rounded-full ${isUp ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
                            {isUp ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                            {trendValue}
                        </div>
                    )}
                </div>

                <h3 className="text-text-secondary text-sm font-medium mb-1">{title}</h3>
                <p className="text-3xl font-bold text-white tracking-tight">{value}</p>
            </div>
        </div>
    );
};

export default StatCard;
