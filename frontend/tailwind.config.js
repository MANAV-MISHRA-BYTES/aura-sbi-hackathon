/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        sbi: {
          deep:  '#003478',
          sky:   '#0072BC',
          light: '#E8F4FD',
          dark:  '#002456',
        },
      },
    },
  },
  plugins: [],
}
