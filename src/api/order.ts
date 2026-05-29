import request from './request'

export function getOrders() {
  return request.get('/orders')
}

export function confirmReceive(id: string) {
  return request.post(`/orders/${id}/confirm`)
}
