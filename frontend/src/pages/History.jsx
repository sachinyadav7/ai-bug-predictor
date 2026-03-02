import React from 'react';
import { Calendar, Clock, FileCode, CheckCircle, AlertTriangle, XCircle, Search, Filter, Download } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const History = () => {
    const { user } = useAuth();

    // Mock data for history
    const historyData = [
        { id: 1, project: 'E-commerce API', file: 'payment_gateway.py', timestamp: '2024-02-15T10:30:00', issues: 2, status: 'High Risk' },
        { id: 2, project: 'Frontend Dashboard', file: 'AuthContext.jsx', timestamp: '2024-02-14T14:20:00', issues: 0, status: 'Safe' },
        { id: 3, project: 'User Service', file: 'user_model.py', timestamp: '2024-02-13T09:15:00', issues: 5, status: 'Critical' },
        { id: 4, project: 'Data Pipeline', file: 'etl_script.py', timestamp: '2024-02-12T16:45:00', issues: 1, status: 'Medium Risk' },
        { id: 5, project: 'Inventory System', file: 'inventory.java', timestamp: '2024-02-10T11:00:00', issues: 0, status: 'Safe' },
    ];

    const getStatusColor = (status) => {
        switch (status) {
            case 'Safe': return 'bg-green-500/10 text-green-500 border-green-500/20';
            case 'Medium Risk': return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
            case 'High Risk': return 'bg-orange-500/10 text-orange-500 border-orange-500/20';
            case 'Critical': return 'bg-red-500/10 text-red-500 border-red-500/20';
            default: return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold text-white tracking-tight">Scan History</h2>
                    <p className="text-text-secondary mt-1">
                        Review past analyses and track code quality improvements over time.
                    </p>
                </div>
                <div className="flex gap-3">
                    <button className="flex items-center gap-2 px-4 py-2 bg-surface border border-border rounded-lg text-text-secondary hover:text-white hover:bg-white/5 transition-colors">
                        <Download className="w-4 h-4" />
                        Export Report
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 bg-primary text-bg font-bold rounded-lg hover:brightness-110 shadow-lg shadow-primary/25 transition-all">
                        <Filter className="w-4 h-4" />
                        Filter
                    </button>
                </div>
            </div>

            <div className="bg-surface border border-border rounded-2xl overflow-hidden shadow-lg shadow-black/20">
                <div className="p-4 border-b border-border flex items-center gap-4">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary" />
                        <input
                            type="text"
                            placeholder="Search by file or project..."
                            className="w-full pl-10 pr-4 py-2 bg-bg border border-border rounded-lg text-sm text-text focus:outline-none focus:border-primary transition-all"
                        />
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-bg/50 text-text-secondary font-semibold border-b border-border">
                            <tr>
                                <th className="px-6 py-4">Project / File</th>
                                <th className="px-6 py-4">Status</th>
                                <th className="px-6 py-4">Issues Found</th>
                                <th className="px-6 py-4">Date & Time</th>
                                <th className="px-6 py-4 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border">
                            {historyData.map((item) => (
                                <tr key={item.id} className="hover:bg-white/5 transition-colors group">
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-3">
                                            <div className="p-2 rounded-lg bg-bg border border-border group-hover:border-primary/50 transition-colors">
                                                <FileCode className="w-5 h-5 text-primary" />
                                            </div>
                                            <div>
                                                <p className="font-semibold text-white">{item.project}</p>
                                                <p className="text-xs text-text-secondary">{item.file}</p>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getStatusColor(item.status)}`}>
                                            {item.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-1.5 font-medium text-white">
                                            {item.issues > 0 ? (
                                                <AlertTriangle className="w-4 h-4 text-red-500" />
                                            ) : (
                                                <CheckCircle className="w-4 h-4 text-green-500" />
                                            )}
                                            {item.issues} Issues
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-text-secondary">
                                        <div className="flex flex-col">
                                            <span className="flex items-center gap-1.5">
                                                <Calendar className="w-3.5 h-3.5" />
                                                {new Date(item.timestamp).toLocaleDateString()}
                                            </span>
                                            <span className="flex items-center gap-1.5 text-xs text-text-secondary/70 mt-0.5">
                                                <Clock className="w-3.5 h-3.5" />
                                                {new Date(item.timestamp).toLocaleTimeString()}
                                            </span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <button className="text-primary hover:text-white font-medium text-sm hover:underline transition-all">
                                            View Report
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="p-4 border-t border-border bg-bg/50 flex items-center justify-between text-xs text-text-secondary">
                    <span>Showing 5 of 24 results</span>
                    <div className="flex gap-2">
                        <button className="px-3 py-1 bg-surface border border-border rounded hover:bg-white/5 transition-all text-text disabled:opacity-50" disabled>Previous</button>
                        <button className="px-3 py-1 bg-surface border border-border rounded hover:bg-white/5 transition-all text-text">Next</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default History;
