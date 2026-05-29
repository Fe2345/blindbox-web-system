import request from '../merchant-request'

export function getMerchantDashboard() {
  return request.get('/dashboard')
}
