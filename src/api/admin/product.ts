import request from '../admin-request'

export function getProductList() { return request.get('/products') }
export function reviewProduct(id: string, data: { action: string; note: string }) { return request.post(`/products/${id}/review`, data) }
export function saveProduct(data: any) { return request.post('/products', data) }
export function updateProduct(id: string, data: any) { return request.put(`/products/${id}`, data) }
export function offlineProduct(id: string) { return request.post(`/products/${id}/offline`) }
