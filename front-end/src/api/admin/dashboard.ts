import request from '../admin-request'

export function getDashboard() { return request.get('/dashboard') }
