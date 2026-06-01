import request from './request'

export function login(data: { username: string; password: string }) {
  return request.post('/login', data)
}

export function register(data: { username: string; phone: string; password: string }) {
  return request.post('/register', data)
}

export function getUserInfo() {
  return request.get('/user/info')
}

export function updateUserInfo(data: { username?: string; phone?: string; avatar?: string }) {
  return request.put('/user/info', data)
}

export function getAddresses() {
  return request.get('/user/addresses')
}

export function addAddress(data: any) {
  return request.post('/user/addresses', data)
}

export function updateAddress(id: string, data: any) {
  return request.put(`/user/addresses/${id}`, data)
}

export function deleteAddress(id: string) {
  return request.delete(`/user/addresses/${id}`)
}
