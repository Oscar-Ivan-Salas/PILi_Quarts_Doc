/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                'brand-red': '#dc2626',
                'brand-yellow': '#fbbf24',
            },
        },
    },
    plugins: [],
    safelist: [
        'magenta:bg-purple-950',
        'magenta:bg-purple-900',
        'magenta:bg-purple-800',
        'magenta:text-purple-100',
        'magenta:text-purple-300',
        'magenta:border-purple-700',
    ],
}
