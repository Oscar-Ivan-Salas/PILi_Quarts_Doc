import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'
import fs from 'fs'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    {
      name: 'monaco-editor-loader',
      configResolved(config) {
        this.config = config
      },
      resolveId(id) {
        if (id.includes('monaco-editor')) {
          return null // Dejar que Vite lo resuelva normalmente
        }
      },
      async transform(code, id) {
        // No hace falta transformación especial
        return null
      }
    }
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    host: 'localhost',
    middlewareMode: false,
    // Proxy: redirige llamadas /api/* al backend N04 en 8005
    proxy: {
      '/api': {
        target: 'http://localhost:8005',
        changeOrigin: true,
        rewrite: (path) => path
      }
    },
    // Servir node_modules/monaco-editor como recurso estático
    fs: {
      allow: [
        '.',
        'node_modules/monaco-editor'
      ]
    }
  },
  // Optimizar para que Monaco se incluya en los chunks
  optimizeDeps: {
    include: ['@monaco-editor/react'],
    exclude: ['monaco-editor']
  }
})

