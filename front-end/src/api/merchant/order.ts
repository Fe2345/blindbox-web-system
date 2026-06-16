import request from '../merchant-request'

export function getMerchantOrders(params?: { status?: string }) {
  return request.get('/orders', { params })
}

export function shipOrder(id: number, data: { logisticsCompany: string; trackingNo: string }) {
  return request.post(`/orders/${id}/ship`, data)
}
