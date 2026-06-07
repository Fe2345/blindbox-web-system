import request from '../merchant-request'

/** 记录查询参数 */
export interface RecordListParams {
  page?: number
  page_size?: number
  type?: string
}

/** 操作记录列表 */
export function getMerchantRecords(params?: RecordListParams) {
  return request.get('/records', { params })
}
