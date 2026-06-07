import request from '../merchant-request'

/** 库存列表查询参数 */
export interface InventoryListParams {
  page?: number
  page_size?: number
  keyword?: string
  stock_status?: string
  order_by?: string
}

/** 库存修改参数 */
export interface InventoryUpdateData {
  change_type: 'increase' | 'decrease' | 'modify'
  quantity: number
  reason?: string
}

/** 库存记录查询参数 */
export interface InventoryRecordParams {
  page?: number
  page_size?: number
  product_id?: number
  type?: string
  start_date?: string
  end_date?: string
}

/** 库存列表 */
export function getInventoryList(params?: InventoryListParams) {
  return request.get('/inventory', { params })
}

/** 修改库存 */
export function updateInventory(id: number, data: InventoryUpdateData) {
  return request.put(`/inventory/${id}`, data)
}

/** 库存变动记录 */
export function getInventoryRecords(params?: InventoryRecordParams) {
  return request.get('/inventory/records', { params })
}
