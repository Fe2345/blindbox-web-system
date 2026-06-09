import request from '../merchant-request'

export function merchantLogin(data: { username: string; password: string }) {
  return request.post('/login', data)
}

export function merchantRegister(data: {
  username: string
  password: string
  phone: string
  merchantName?: string
  contactName?: string
}) {
  return request.post('/register', data)
}

export function merchantLogout() {
  return request.post('/logout')
}

export function getMerchantInfo() {
  return request.get('/info')
}
