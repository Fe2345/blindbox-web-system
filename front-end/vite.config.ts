import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ mode }) => {
  const envDir = resolve(__dirname, '..')
  const env = loadEnv(mode, envDir)

  const backendUrl = env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'
  const frontendPort = Number(env.VITE_PORT) || 3000

  console.log('[vite] envDir:', envDir)
  console.log('[vite] VITE_PORT:', env.VITE_PORT, '→ port:', frontendPort)
  console.log('[vite] VITE_BACKEND_URL:', env.VITE_BACKEND_URL, '→ proxy target:', backendUrl)

  return {
    envDir,
    plugins: [vue()],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      },
    },
    build: {
      rollupOptions: {
        input: {
          main: resolve(__dirname, 'index.html'),
          admin: resolve(__dirname, 'admin.html'),
          merchant: resolve(__dirname, 'merchant.html'),
        },
      },
    },
    server: {
      port: frontendPort,
      proxy: {
        '/user/api': {
          target: backendUrl,
          changeOrigin: true,
        },
        '/merchant/api': {
          target: backendUrl,
          changeOrigin: true,
        },
        '/admin/api': {
          target: backendUrl,
          changeOrigin: true,
        },
      },
    },
  }
})
