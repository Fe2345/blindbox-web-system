import request from '../admin-request'

export function getExchangeList() { return request.get('/exchanges') }
export function resolveException(id: string, data: { action: string; note: string }) { return request.post(`/exchanges/${id}/resolve`, data) }
