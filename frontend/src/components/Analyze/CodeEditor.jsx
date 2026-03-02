import React, { useState, useRef } from 'react';
import Editor from '@monaco-editor/react';
import { Play, Settings, AlertTriangle, CheckCircle, FileCode, ChevronRight, X } from 'lucide-react';
import RiskMeter from './RiskMeter';
import HighlightOverlay from './HighlightOverlay';

const CodeEditor = ({ initialCode = '', onAnalyze }) => {
    const [code, setCode] = useState(initialCode || '# Paste your python code here\n\ndef sum(a, b):\n    return a + b\n');
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(false);
    const editorRef = useRef(null);
    const monacoRef = useRef(null);
    const [language, setLanguage] = useState('python');

    const handleAnalyze = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/v1/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code,
                    language,
                    include_explanation: true
                })
            });
            const data = await response.json();
            setAnalysis(data);
            highlightBugs(data.results);
        } catch (error) {
            console.error('Analysis failed:', error);
            // Mock error for demo visualization if server fails
            // setAnalysis({ ...mockData });
        }
        setLoading(false);
    };

    const highlightBugs = (results) => {
        if (!editorRef.current || !monacoRef.current) return;

        const editor = editorRef.current;
        const monaco = monacoRef.current;

        const decorations = results
            .filter(r => r.is_buggy)
            .map(r => ({
                range: new monaco.Range(r.line_start, 1, r.line_end, 1),
                options: {
                    isWholeLine: true,
                    className: 'bg-danger/10 border-l-2 border-danger', // Tailwind classes passed as string might work if CSS rules exist, but typically Monaco needs specific class names defined in CSS.
                    glyphMarginClassName: 'bug-glyph', // We might need to keep custom CSS for this or inject styles
                    hoverMessage: { value: `Bug confidence: ${(r.confidence * 100).toFixed(1)}%` }
                }
            }));

        // Note: For Monaco className to work with Tailwind classes, the CSS must be globally available.
        // Since we import index.css, standard utilities work.

        if (window.lastDecorations) {
            window.lastDecorations = editor.deltaDecorations(window.lastDecorations, decorations);
        } else {
            window.lastDecorations = editor.deltaDecorations([], decorations);
        }
    };

    const scrollToLine = (line) => {
        if (editorRef.current) {
            editorRef.current.revealLineInCenter(line);
            editorRef.current.setPosition({ lineNumber: line, column: 1 });
            editorRef.current.focus();
        }
    }

    return (
        <div className="flex h-full w-full">
            {/* Main Editor Area */}
            <div className="flex-1 flex flex-col min-w-0 bg-bg">
                {/* Toolbar */}
                <div className="flex items-center justify-between px-4 py-2 bg-surface/50 border-b border-border">
                    <div className="flex items-center gap-3">
                        <div className="flex items-center gap-2 px-3 py-1.5 bg-surface rounded text-sm text-text-secondary border border-border">
                            <FileCode className="w-4 h-4" />
                            <select
                                value={language}
                                onChange={(e) => setLanguage(e.target.value)}
                                className="bg-transparent border-none outline-none text-text appearance-none cursor-pointer"
                            >
                                <option value="python">main.py</option>
                                <option value="java">Main.java</option>
                                <option value="javascript">app.js</option>
                            </select>
                        </div>
                    </div>
                    <button
                        className={`flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium transition-all ${loading
                                ? 'bg-surface text-text-secondary cursor-not-allowed'
                                : 'bg-primary text-bg hover:bg-primary-hover shadow-lg shadow-primary/20'
                            }`}
                        onClick={handleAnalyze}
                        disabled={loading}
                    >
                        {loading ? 'Analyzing...' : (
                            <>
                                <Play className="w-4 h-4 fill-current" />
                                Analyze Code
                            </>
                        )}
                    </button>
                </div>

                {/* Editor */}
                <div className="flex-1 relative">
                    <Editor
                        height="100%"
                        defaultLanguage="python"
                        language={language}
                        theme="vs-dark"
                        value={code}
                        onChange={setCode}
                        onMount={(editor, monaco) => {
                            editorRef.current = editor;
                            monacoRef.current = monaco;
                            // Update theme background to match
                            monaco.editor.defineTheme('custom-dark', {
                                base: 'vs-dark',
                                inherit: true,
                                rules: [],
                                colors: {
                                    'editor.background': '#1e1e2e',
                                }
                            });
                            monaco.editor.setTheme('custom-dark');
                        }}
                        options={{
                            minimap: { enabled: false },
                            fontSize: 15,
                            fontFamily: 'JetBrains Mono',
                            padding: { top: 20 },
                            glyphMargin: true,
                            folding: true,
                            lineNumbers: 'on',
                            renderWhitespace: 'selection',
                            scrollBeyondLastLine: false,
                            smoothScrolling: true,
                            cursorBlinking: 'smooth',
                            cursorSmoothCaretAnimation: 'on',
                        }}
                    />
                    {analysis && <HighlightOverlay results={analysis.results} />}
                </div>
            </div>

            {/* Analysis Sidebar */}
            {analysis && (
                <div className="w-80 bg-surface border-l border-border flex flex-col animate-in slide-in-from-right duration-300">
                    <div className="p-4 border-b border-border">
                        <h2 className="text-sm font-bold text-text uppercase tracking-wider mb-4">Analysis Results</h2>
                        <RiskMeter
                            score={analysis.file_risk_score}
                            functions={analysis.functions_analyzed}
                            bugs={analysis.buggy_functions_count}
                        />
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        <div className="flex items-center justify-between text-xs text-text-secondary font-medium">
                            <span>FUNCTIONS ({analysis.results.length})</span>
                            <span>RISK</span>
                        </div>

                        <div className="space-y-2">
                            {analysis.results.map((func, idx) => (
                                <div
                                    key={idx}
                                    className={`group p-3 rounded-lg border transition-all cursor-pointer hover:shadow-md ${func.is_buggy
                                            ? 'bg-danger/5 border-danger/20 hover:border-danger/50'
                                            : 'bg-surface-hover/50 border-transparent hover:border-border'
                                        }`}
                                    onClick={() => scrollToLine(func.line_start)}
                                >
                                    <div className="flex items-center justify-between mb-2">
                                        <div className="flex items-center gap-2">
                                            {func.is_buggy ? (
                                                <AlertTriangle className="w-4 h-4 text-danger" />
                                            ) : (
                                                <CheckCircle className="w-4 h-4 text-success" />
                                            )}
                                            <span className="font-mono text-sm text-text font-medium">{func.function_name}</span>
                                        </div>
                                        <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${func.is_buggy
                                                ? 'bg-danger/10 text-danger'
                                                : 'bg-success/10 text-success'
                                            }`}>
                                            {(func.confidence * 100).toFixed(0)}%
                                        </span>
                                    </div>

                                    <div className="text-xs text-text-secondary flex justify-between items-center">
                                        <span>Line {func.line_start}-{func.line_end}</span>
                                        <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                                    </div>

                                    {func.is_buggy && func.highlighted_tokens && (
                                        <div className="mt-2 pt-2 border-t border-danger/10">
                                            <p className="text-[10px] text-danger/80 font-medium mb-1">SUSPICIOUS PATTERNS</p>
                                            <div className="flex flex-wrap gap-1">
                                                {func.highlighted_tokens.slice(0, 3).map((t, i) => (
                                                    <span key={i} className="px-1.5 py-0.5 bg-bg rounded text-[10px] font-mono text-text">
                                                        {t.token}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CodeEditor;
