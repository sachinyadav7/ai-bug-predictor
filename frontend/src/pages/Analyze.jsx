import React from 'react';
import CodeEditor from '../components/Analyze/CodeEditor';

const Analyze = () => {
    return (
        <div className="h-[calc(100vh-8rem)] flex flex-col">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-white">Code Analysis</h2>
                <div className="flex gap-3">
                    <button className="px-4 py-2 bg-surface border border-border text-text hover:text-white rounded-lg text-sm font-medium transition-colors">
                        Clear Editor
                    </button>
                    <button className="px-4 py-2 bg-primary text-bg hover:brightness-110 rounded-lg text-sm font-bold shadow-lg shadow-primary/25 transition-all">
                        Run Analysis
                    </button>
                </div>
            </div>
            <div className="flex-1 bg-surface border border-border rounded-2xl overflow-hidden shadow-2xl">
                <CodeEditor />
            </div>
        </div>
    );
};

export default Analyze;
