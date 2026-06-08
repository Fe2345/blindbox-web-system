import axios from 'axios'
import router from '@/router/merchant'
import { ElMessage } from 'element-plus'

const merchantRequest = axios.create({
  baseURL: '/merchant/api',
  timeout: 10000,
})

// --- 401 拦截与 token 自动续期 ---

let isRefreshing = false
let failedQueue: Array<{ resolve: (value: any) => void; reject: (reason?: any) => void }> = []

function processQueue(error: any) {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(null)
    }
  })
  failedQueue = []
}

merchantRequest.interceptors.response.use(
  (res) => res.data,
  async (err) => {
    const originalRequest = err.config
    const isRefreshRequest = originalRequest.url?.includes('/token/refresh')

    if (err.response?.status === 401 && !originalRequest._retry && !isRefreshRequest) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(() => merchantRequest(originalRequest))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        await axios.post('/merchant/api/token/refresh', {})
        processQueue(null)
        return merchantRequest(originalRequest)
      } catch (refreshErr) {
        processQueue(refreshErr)
        localStorage.removeItem('merchant_logged_in')
        router.push('/login')
        return Promise.reject(refreshErr)
      } finally {
        isRefreshing = false
      }
    }

    // 403 表示角色不匹配，清除登录态跳转登录页
    if (err.response?.status === 403) {
      localStorage.removeItem('merchant_logged_in')
      router.push('/login')
    }

    const msg = err.response?.data?.message || err.message || '请求失败'
    ElMessage.error(msg)
    return Promise.reject(err)
  },
)

export default merchantRequest
