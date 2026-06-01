import request from '../merchant-request'

export function merchantLogin(data: { username: string; password: string }) {
  return request.post('/login', data)
}

export function getMerchantInfo() {
  return request.get('/info')
}
