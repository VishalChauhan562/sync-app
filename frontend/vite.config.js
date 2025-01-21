import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, 
    port: 5173,  
    hmr: {
      host: 'sync-app-1.onrender.com',
      clientPort: 5173,
    },
    allowedHosts: ['sync-app-1.onrender.com'],  
  }
})
