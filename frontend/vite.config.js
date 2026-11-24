import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// En desarrollo, todo lo que empiece con /api se reenvía al backend (FastAPI),
// así el navegador habla con un solo origen y no hay problemas de CORS.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
