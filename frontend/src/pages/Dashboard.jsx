import React from 'react';
import { Bug, CheckCircle, Clock, Zap, ArrowRight, Shield, Activity } from 'lucide-react';
import StatCard from '../components/Dashboard/StatCard';
import ActivityChart from '../components/Dashboard/ActivityChart';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
    const { user } = useAuth();
    const [stats, setStats] = React.useState({
        total_bugs_found: 0,
        bugs_fixed: 0,
        avg_fix_time: "--",
        efficiency_score: "--",
        recent_scans: []
    });

    React.useEffect(() => {
        const fetchStats = async () => {
            try {
                // In a real app, use auth token here
                const response = await fetch('http://localhost:8000/api/v1/dashboard/stats');
                if (response.ok) {
                    const data = await response.json();
                    setStats(data);
                }
            } catch (error) {
                console.error("Failed to fetch dashboard stats:", error);
            }
        };

        fetchStats();
        const interval = setInterval(fetchStats, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div>
                <h2 className="text-3xl font-bold text-white tracking-tight">Dashboard</h2>
                <p className="text-text-secondary mt-1">
                    Overview of your code security status and recent activities.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Total Bugs Found"
                    value={stats.total_bugs_found.toLocaleString()}
                    trend="up"
                    trendValue="12%"
                    icon={Bug}
                    color="text-red-500"
                />
                <StatCard
                    title="Bugs Fixed"
                    value={stats.bugs_fixed.toLocaleString()}
                    trend="up"
                    trendValue="8%"
                    icon={CheckCircle}
                    color="text-green-500"
                />
                <StatCard
                    title="Avg. Fix Time"
                    value={stats.avg_fix_time}
                    trend="down"
                    trendValue="5%"
                    icon={Clock}
                    color="text-blue-500"
                />
                <StatCard
                    title="Efficiency Score"
                    value={stats.efficiency_score}
                    trend="up"
                    trendValue="2%"
                    icon={Zap}
                    color="text-yellow-500"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-6">
                    <div className="p-6 bg-surface border border-border rounded-2xl shadow-lg shadow-black/20">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="text-lg font-bold text-white flex items-center gap-2">
                                <Activity className="w-5 h-5 text-primary" />
                                Analysis Activity
                            </h3>
                            <select className="bg-bg border border-border rounded-lg text-xs text-text-secondary px-3 py-1.5 focus:outline-none focus:border-primary">
                                <option>Last 7 Days</option>
                                <option>Last 30 Days</option>
                            </select>
                        </div>
                        <ActivityChart />
                    </div>
                </div>

                <div className="space-y-6">
                    <div className="bg-surface border border-border rounded-2xl p-6 shadow-lg shadow-black/20 h-full flex flex-col">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="text-lg font-bold text-white flex items-center gap-2">
                                <Shield className="w-5 h-5 text-green-500" />
                                Recent Scans
                            </h3>
                            <button className="text-xs text-primary hover:text-white transition-colors font-medium">View All</button>
                        </div>

                        <div className="space-y-4 flex-1 overflow-y-auto pr-2 custom-scrollbar">
                            {stats.recent_scans.length === 0 ? (
                                <div className="flex flex-col items-center justify-center h-40 text-text-secondary border border-dashed border-border rounded-xl bg-bg/50">
                                    <Bug className="w-8 h-8 opacity-20 mb-2" />
                                    <p className="text-sm">No recent scans</p>
                                </div>
                            ) : (
                                stats.recent_scans.map((scan, i) => (
                                    <div key={i} className="flex items-center justify-between p-4 bg-bg rounded-xl border border-transparent hover:border-primary/20 hover:bg-white/5 transition-all cursor-pointer group">
                                        <div className="flex items-center gap-3">
                                            <div className={`p-2 rounded-lg ${scan.issues_count > 0 ? 'bg-red-500/10 text-red-500' : 'bg-green-500/10 text-green-500'}`}>
                                                <Bug className="w-4 h-4" />
                                            </div>
                                            <div>
                                                <p className="text-sm font-semibold text-white group-hover:text-primary transition-colors">{scan.project_name}</p>
                                                <p className="text-xs text-text-secondary">{new Date(scan.timestamp).toLocaleTimeString()}</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-3">
                                            <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${scan.issues_count > 0
                                                    ? 'bg-red-500/10 text-red-400 border border-red-500/20'
                                                    : 'bg-green-500/10 text-green-400 border border-green-500/20'
                                                }`}>
                                                {scan.issues_count} Issues
                                            </span>
                                            <ArrowRight className="w-4 h-4 text-text-secondary group-hover:text-white -translate-x-2 opacity-0 group-hover:translate-x-0 group-hover:opacity-100 transition-all" />
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
