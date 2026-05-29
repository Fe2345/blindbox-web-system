import request from '../admin-request'

export function getRules() { return request.get('/rules') }
export function saveRules(data: any) { return request.post('/rules', data) }
