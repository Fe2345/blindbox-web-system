import axios from 'axios'
import { ElMessage } from 'element-plus'

const adminRequest = axios.create({
  baseURL: '/admin/api',
  timeout: 10000,
})

adminRequest.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

adminRequest.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const msg = err.response?.data?.message || err.message || '请求失败'
    ElMessage.error(msg)
    return Promise.reject(err)
  }
)

export default adminRequest
