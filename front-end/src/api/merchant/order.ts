import request from '../merchant-request'

export function getMerchantOrders(params?: { status?: string }) {
  return request.get('/orders', { params })
}
