import request from '../admin-request'

export function getBlindBoxList() { return request.get('/blindboxes') }
export function saveBlindBox(data: any) { return request.post('/blindboxes', data) }
export function updateBlindBox(id: string, data: any) { return request.put(`/blindboxes/${id}`, data) }
export function updateBlindBoxStatus(id: string, status: string) { return request.put(`/blindboxes/${id}/status`, { status }) }
export function savePrizePool(blindboxId: string, prizes: any[]) { return request.post(`/blindboxes/${blindboxId}/prizes`, { prizes }) }
