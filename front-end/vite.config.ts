import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
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
    port: 5173,
    // 添加 SPA fallback 配置
    middlewareMode: false,
    proxy: {
      '/merchant/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/user/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/admin/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
