import axios from 'axios'
import { ElMessage } from 'element-plus'

const merchantRequest = axios.create({
  baseURL: '/merchant/api',
  timeout: 10000,
})

merchantRequest.interceptors.request.use((config) => {
  const token = localStorage.getItem('merchant_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

merchantRequest.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const msg = err.response?.data?.message || err.message || '请求失败'
    ElMessage.error(msg)
    return Promise.reject(err)
  }
)

export default merchantRequest
