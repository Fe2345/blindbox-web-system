import axios from 'axios'

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
    return Promise.reject(err)
  }
)

export default adminRequest
