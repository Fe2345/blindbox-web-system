import request from '../admin-request'

export function getUserList() { return request.get('/users') }
export function updateUserStatus(id: string, status: string) { return request.put(`/users/${id}/status`, { status }) }
