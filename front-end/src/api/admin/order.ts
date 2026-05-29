import request from '../admin-request'

export function getOrderList() { return request.get('/orders') }
export function shipOrder(id: string, data: { company: string; trackingNo: string }) { return request.post(`/orders/${id}/ship`, data) }
