import request from '../merchant-request'

export function getInventoryList() {
  return request.get('/inventory')
}

export function updateStock(productId: string, stock: number) {
  return request.put(`/inventory/${productId}`, { stock })
}

export function getInventoryRecords(productId?: string) {
  return request.get('/inventory/records', { params: { productId } })
}
