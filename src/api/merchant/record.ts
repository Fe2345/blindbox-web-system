import request from '../merchant-request'

export function getMerchantRecords(params?: {
  type?: string
  keyword?: string
  startDate?: string
  endDate?: string
}) {
  return request.get('/records', { params })
}
