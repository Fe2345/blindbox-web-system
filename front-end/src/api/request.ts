import axios from 'axios'
import router from '@/router'

// Preserve the original HTTP adapter before any mock replaces it.
// Uses a global to survive Vite HMR re-execution (which would otherwise
// capture the mock adapter after setupMock() has run).
// The actual capture now happens in main.ts before setupMock().
const _g = window as any
if (!_g.__axiosOriginalAdapter) {
  _g.__axiosOriginalAdapter = axios.defaults.adapter
}

const request = axios.create({
  baseURL: '/user/api',
  timeout: 10000,
  adapter: _g.__axiosOriginalAdapter,
})

request.interceptors.request.use((config) => {
  console.log('[request]', config.method?.toUpperCase(), config.baseURL, '+', config.url)
  return config
})

// --- 401 拦截与 token 自动续期 ---

let isRefreshing = false
let failedQueue: Array<{ resolve: (value: any) => void; reject: (reason?: any) => void }> = []

function processQueue(error: any, token: string | null = null) {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

request.interceptors.response.use(
  (res) => res.data,
  async (err) => {
    const originalRequest = err.config
    const isRefreshRequest = originalRequest.url?.includes('/token/refresh/')

    // 非刷新请求的 401 才尝试续期
    if (err.response?.status === 401 && !originalRequest._retry && !isRefreshRequest) {
      if (isRefreshing) {
        // 如果正在刷新 token，把当前请求加入队列等待
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(() => request(originalRequest))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        // 用原始 axios 调用刷新接口，避免循环
        await axios.post('/user/api/token/refresh/', {})
        processQueue(null)
        return request(originalRequest)
      } catch (refreshErr) {
        processQueue(refreshErr)
        // 刷新失败：清除登录态，跳转登录页
        localStorage.removeItem('isLoggedIn')
        router.push('/login')
        return Promise.reject(refreshErr)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(err)
  },
)

export default request
