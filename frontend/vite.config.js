import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  // ────────────────────────────────────────────────
  // MOST IMPORTANT FOR DJANGO + WHITENOISE
  // ────────────────────────────────────────────────
  base: '/static/',     // ← change to this (matches STATIC_URL = '/static/')

  server: {
    port: 5173,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/admin': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },

  build: {
    outDir: 'dist',
    assetsDir: 'assets',          // keeps assets in dist/assets/
    sourcemap: false,             // disable in production (smaller files)
    minify: 'esbuild',
    emptyOutDir: true,
    // Optional: chunk large vendor libs
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        }
      }
    }
  }
})