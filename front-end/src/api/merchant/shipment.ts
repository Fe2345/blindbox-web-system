import request from '../merchant-request'

/** 发货列表查询参数 */
export interface ShipmentListParams {
  page?: number
  page_size?: number
  status?: string
  keyword?: string
  order_by?: string
}

/** 发货参数 */
export interface ShipmentShipData {
  logistics_company: string
  tracking_no: string
}

/** 发货任务列表 */
export function getShipmentList(params?: ShipmentListParams) {
  return request.get('/shipments', { params })
}

/** 发货任务详情 */
export function getShipmentDetail(id: number) {
  return request.get(`/shipments/${id}`)
}

/** 执行发货 */
export function confirmShipment(id: number, data: ShipmentShipData) {
  return request.post(`/shipments/${id}/ship`, data)
}
