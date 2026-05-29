import request from '../admin-request'

export function getLedger(params?: { type?: string; startDate?: string; endDate?: string }) { return request.get('/ledger', { params }) }
