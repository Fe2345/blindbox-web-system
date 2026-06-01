import request from '../admin-request'

export function adminLogin(data: { username: string; password: string }) {
  return request.post('/login', data)
}

export function getAdminInfo() {
  return request.get('/info')
}
