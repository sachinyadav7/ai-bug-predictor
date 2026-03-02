import { useState, useCallback } from 'react';

const API_BASE_URL = 'http://localhost:8000';

export const useBugPrediction = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [result, setResult] = useState(null);

    const predict = useCallback(async (code, options = {}) => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code,
                    language: options.language || 'python',
                    include_explanation: options.explain || false,
                    filename: options.filename
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Prediction failed');
            }

            const data = await response.json();
            setResult(data);
            return data;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    return { predict, loading, error, result };
};

export const useBatchScan = () => {
    const [progress, setProgress] = useState(0);

    const scanFiles = async (files) => {
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));

        const response = await fetch(`${API_BASE_URL}/api/v1/batch-scan`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('Batch scan failed');
        return response.json();
    };

    return { scanFiles, progress };
};
