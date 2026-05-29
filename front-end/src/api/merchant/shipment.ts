import request from '../merchant-request'

export function getShipmentTasks(params?: { status?: string }) {
  return request.get('/shipments', { params })
}

export function getShipmentDetail(id: string) {
  return request.get(`/shipments/${id}`)
}

export function confirmShipment(id: string, data: {
  logisticsCompany: string
  trackingNo: string
}) {
  return request.post(`/shipments/${id}/ship`, data)
}
