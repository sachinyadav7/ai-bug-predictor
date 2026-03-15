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
                primary: '#89b4fa',
                secondary: 'var(--secondary-color)',
                text: 'var(--text-color)',
                'text-secondary': '#a6adc8',
                border: 'var(--border-color)',
                'surface-hover': '#32324a',
                'primary-hover': '#b4befe',
                success: '#a6e3a1',
                warning: '#f9e2af',
                danger: '#f38ba8',
                accent: '#cba6f7',
            }
        },
    },
    plugins: [],
}
