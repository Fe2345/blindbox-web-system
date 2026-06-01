import request from '../admin-request'

export function getOpLogs() { return request.get('/logs') }
export function getExceptions() { return request.get('/exceptions') }
export function resolveException(id: string, data: { result: string }) { return request.post(`/exceptions/${id}/resolve`, data) }
