import type { Config } from "tailwindcss";

export default {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                // Palette Vert Émeraude / Noir - Éthique & Bien-être RH
                emerald: {
                    DEFAULT: '#009879',
                    light: '#5DE6C1',
                    dark: '#007A61',
                },
                dark: {
                    DEFAULT: '#0C1D24',
                    light: '#1A2F38',
                },
                light: {
                    DEFAULT: '#F4F7F7',
                    gray: '#E8ECEC',
                },
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
} satisfies Config;
