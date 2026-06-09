import request from '../admin-request'

export function getUserList() { return request.get('/users') }
export function updateUserStatus(id: string, isActive: boolean) { return request.put(`/users/${id}/status`, { isActive }) }
