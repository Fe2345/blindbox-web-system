import request from '../admin-request'

export function getMerchantList() { return request.get('/merchants') }
export function getMerchantDetail(id: string) { return request.get(`/merchants/${id}`) }
export function reviewMerchant(id: string, data: { action: string; note: string }) { return request.post(`/merchants/${id}/review`, data) }
export function updateMerchantStatus(id: string, status: string) { return request.put(`/merchants/${id}/status`, { status }) }
