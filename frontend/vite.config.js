import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// BACKEND_URL is set via docker-compose environment for Docker networking.
// Falls back to localhost:5000 for local development without Docker.
const backendTarget = process.env.BACKEND_URL || 'http://localhost:5000'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: backendTarget,
        changeOrigin: true,
      },
    },
  },
})
