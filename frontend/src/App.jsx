import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import Analyze from './pages/Analyze';
import History from './pages/History';
import Settings from './pages/Settings';
import Profile from './pages/Profile';
import Login from './pages/Login';

const ProtectedRoute = () => {
    const { user, loading } = useAuth();
    if (loading) return <div className="min-h-screen bg-bg flex items-center justify-center text-primary">Loading...</div>;
    return user ? <Layout><Outlet /></Layout> : <Navigate to="/login" />;
};

function App() {
    return (
        <Router>
            <AuthProvider>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route element={<ProtectedRoute />}>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/analyze" element={<Analyze />} />
                        <Route path="/history" element={<History />} />
                        <Route path="/settings" element={<Settings />} />
                        <Route path="/profile" element={<Profile />} />
                    </Route>
                </Routes>
            </AuthProvider>
        </Router>
    );
}

export default App;
