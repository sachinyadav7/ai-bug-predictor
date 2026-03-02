/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                bg: 'var(--bg-color)',
                surface: 'var(--surface-color)',
                primary: 'var(--primary-color)',
                secondary: 'var(--secondary-color)',
                text: 'var(--text-color)',
                'text-secondary': 'var(--text-secondary)',
                border: 'var(--border-color)',
                'surface-hover': '#32324a',     // Panel hover
                'text-secondary': '#a6adc8',    // Secondary text
                primary: '#89b4fa',             // Accent/Primary (blue)
                'primary-hover': '#b4befe',
                success: '#a6e3a1',             // Green
                warning: '#f9e2af',             // Yellow
                danger: '#f38ba8',              // Red
                accent: '#cba6f7',              // Purple accent
            }
        },
    },
    plugins: [],
}
