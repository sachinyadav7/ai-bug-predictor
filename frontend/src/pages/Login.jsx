import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Bug, Github, Chrome, ArrowRight, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

const Login = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState(''); // Added for registration
    const [fullName, setFullName] = useState(''); // Added for registration
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login, register, guestLogin } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            if (isLogin) {
                await login(username, password); // Changed email to username for now based on backend
            } else {
                await register(username, email, password, fullName);
            }
            navigate('/');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleGuestLogin = () => {
        guestLogin();
        navigate('/');
    };

    return (
        <div className="min-h-screen flex bg-bg text-text font-sans">
            {/* Left Side - Hero/Branding */}
            <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-surface">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-surface to-bg pointer-events-none" />
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=2070&auto=format&fit=crop')] bg-cover bg-center opacity-10 mix-blend-overlay" />

                <div className="relative z-10 w-full h-full flex flex-col justify-between p-12">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-primary/20 rounded-xl backdrop-blur-md border border-primary/20">
                            <Bug className="w-8 h-8 text-primary" />
                        </div>
                        <h1 className="text-2xl font-bold tracking-tight text-white">BugPredictor</h1>
                    </div>

                    <div className="space-y-6 max-w-lg">
                        <motion.h2
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                            className="text-5xl font-bold text-white leading-tight"
                        >
                            Catch bugs before they reach production.
                        </motion.h2>
                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.4 }}
                            className="text-lg text-text-secondary"
                        >
                            AI-powered code analysis that integrates seamlessly into your workflow.
                            Stop guessing, start fixing.
                        </motion.p>
                    </div>

                    <div className="flex gap-4 text-sm text-text-secondary">
                        <span>© 2024 BugPredictor AI</span>
                        <span>Privacy Policy</span>
                        <span>Terms of Service</span>
                    </div>
                </div>
            </div>

            {/* Right Side - Auth Form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
                <div className="w-full max-w-md space-y-8">
                    <div className="text-center lg:text-left">
                        <h2 className="text-3xl font-bold text-white">
                            {isLogin ? 'Welcome back' : 'Create an account'}
                        </h2>
                        <p className="mt-2 text-text-secondary">
                            {isLogin ? 'Enter your details to access your dashboard.' : 'Start your journey with us today.'}
                        </p>
                    </div>

                    <div className="flex gap-4">
                        <button className="flex-1 py-2.5 flex items-center justify-center gap-2 bg-white text-bg font-semibold rounded-lg hover:bg-gray-100 transition-colors">
                            <img src="https://www.svgrepo.com/show/475656/google-color.svg" className="w-5 h-5" alt="Google" />
                            Google
                        </button>
                        <button className="flex-1 py-2.5 flex items-center justify-center gap-2 bg-surface border border-border text-white font-semibold rounded-lg hover:bg-white/5 transition-colors">
                            <Github className="w-5 h-5" />
                            GitHub
                        </button>
                    </div>

                    <div className="relative">
                        <div className="absolute inset-0 flex items-center">
                            <div className="w-full border-t border-border"></div>
                        </div>
                        <div className="relative flex justify-center text-sm">
                            <span className="px-2 bg-bg text-text-secondary">Or continue with</span>
                        </div>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-5">
                        {/* Username field for both Login and Register */}
                        <div>
                            <label className="block text-sm font-medium text-text-secondary mb-1">Username</label>
                            <input
                                type="text"
                                required
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="w-full px-4 py-2.5 bg-surface border border-border rounded-lg text-white focus:ring-2 focus:ring-primary focus:border-transparent transition-all outline-none"
                                placeholder="johndoe"
                            />
                        </div>

                        {!isLogin && (
                            <>
                                <div>
                                    <label className="block text-sm font-medium text-text-secondary mb-1">Full Name</label>
                                    <input
                                        type="text"
                                        value={fullName}
                                        onChange={(e) => setFullName(e.target.value)}
                                        className="w-full px-4 py-2.5 bg-surface border border-border rounded-lg text-white focus:ring-2 focus:ring-primary focus:border-transparent transition-all outline-none"
                                        placeholder="John Doe"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-text-secondary mb-1">Email</label>
                                    <input
                                        type="email"
                                        required
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="w-full px-4 py-2.5 bg-surface border border-border rounded-lg text-white focus:ring-2 focus:ring-primary focus:border-transparent transition-all outline-none"
                                        placeholder="name@company.com"
                                    />
                                </div>
                            </>
                        )}

                        <div>
                            <label className="block text-sm font-medium text-text-secondary mb-1">Password</label>
                            <input
                                type="password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-4 py-2.5 bg-surface border border-border rounded-lg text-white focus:ring-2 focus:ring-primary focus:border-transparent transition-all outline-none"
                                placeholder="••••••••"
                            />
                        </div>

                        {error && (
                            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-2.5 flex items-center justify-center gap-2 bg-primary text-bg font-bold rounded-lg hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : (isLogin ? 'Sign In' : 'Create Account')}
                            {!loading && <ArrowRight className="w-4 h-4" />}
                        </button>
                    </form>

                    <div className="text-center space-y-4">
                        <button
                            type="button"
                            onClick={handleGuestLogin}
                            className="text-sm text-text-secondary hover:text-white transition-colors underline decoration-dotted"
                        >
                            Continue as Guest
                        </button>

                        <p className="text-sm text-text-secondary">
                            {isLogin ? "Don't have an account?" : "Already have an account?"}
                            <button
                                onClick={() => setIsLogin(!isLogin)}
                                className="ml-1 text-primary hover:text-white transition-colors font-medium"
                            >
                                {isLogin ? 'Sign up' : 'Sign in'}
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
