import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
    { name: 'Mon', bugs: 4, fixed: 2 },
    { name: 'Tue', bugs: 3, fixed: 5 },
    { name: 'Wed', bugs: 7, fixed: 6 },
    { name: 'Thu', bugs: 2, fixed: 4 },
    { name: 'Fri', bugs: 6, fixed: 8 },
    { name: 'Sat', bugs: 1, fixed: 2 },
    { name: 'Sun', bugs: 0, fixed: 1 },
];

const ActivityChart = () => {
    return (
        <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                        <linearGradient id="colorBugs" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorFixed" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                    <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                        itemStyle={{ color: '#e2e8f0' }}
                    />
                    <Area type="monotone" dataKey="bugs" stroke="#ef4444" strokeWidth={3} fillOpacity={1} fill="url(#colorBugs)" />
                    <Area type="monotone" dataKey="fixed" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorFixed)" />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ActivityChart;
