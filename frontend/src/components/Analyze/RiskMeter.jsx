import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const RiskMeter = ({ score, functions, bugs }) => {
    // Colors from Tailwind config
    const getColor = (score) => {
        if (score < 0.3) return '#a6e3a1'; // success
        if (score < 0.7) return '#f9e2af'; // warning
        return '#f38ba8'; // danger
    };

    const getLabel = (score) => {
        if (score < 0.3) return 'Low Risk';
        if (score < 0.7) return 'Medium Risk';
        return 'High Risk';
    };

    const color = getColor(score);

    return (
        <div className="flex flex-col items-center">
            <div className="w-32 h-32 mb-4">
                <CircularProgressbar
                    value={score * 100}
                    text={`${(score * 100).toFixed(0)}%`}
                    styles={buildStyles({
                        textSize: '24px',
                        pathColor: color,
                        textColor: color,
                        trailColor: '#45475a', // border color
                        backgroundColor: '#2a2a40', // surface
                    })}
                />
            </div>

            <div
                className="text-lg font-bold mb-6"
                style={{ color }}
            >
                {getLabel(score)}
            </div>

            <div className="grid grid-cols-3 gap-2 w-full">
                <div className="flex flex-col items-center p-2 bg-bg/50 rounded-lg">
                    <span className="text-xl font-bold text-text">{functions}</span>
                    <span className="text-xs text-text-secondary uppercase tracking-wider">Funcs</span>
                </div>
                <div className="flex flex-col items-center p-2 bg-danger/10 rounded-lg border border-danger/20">
                    <span className="text-xl font-bold text-danger">{bugs}</span>
                    <span className="text-xs text-danger/70 uppercase tracking-wider">Bugs</span>
                </div>
                <div className="flex flex-col items-center p-2 bg-bg/50 rounded-lg">
                    <span className="text-xl font-bold text-text">
                        {functions > 0 ? ((bugs / functions) * 100).toFixed(0) : 0}%
                    </span>
                    <span className="text-xs text-text-secondary uppercase tracking-wider">Rate</span>
                </div>
            </div>
        </div>
    );
};

export default RiskMeter;
