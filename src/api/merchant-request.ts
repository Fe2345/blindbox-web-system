import axios from 'axios'

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
    return Promise.reject(err)
  }
)

export default merchantRequest
