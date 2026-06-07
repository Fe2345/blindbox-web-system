import request from '../merchant-request'

/** 商品列表查询参数 */
export interface ProductListParams {
  page?: number
  page_size?: number
  status?: string
  category?: string
  rarity?: string
  keyword?: string
  order_by?: string
}

/** 商品提交参数 */
export interface ProductSubmitData {
  name: string
  image: string
  category: string
  rarity: string
  description?: string
  estimated_points?: number
}

/** 商品列表 */
export function getProductList(params?: ProductListParams) {
  return request.get('/products', { params })
}

/** 商品详情 */
export function getProductDetail(id: number) {
  return request.get(`/products/${id}`)
}

/** 新增商品 */
export function submitProduct(data: ProductSubmitData) {
  return request.post('/products/submit', data)
}

/** 修改商品 */
export function updateProduct(id: number, data: ProductSubmitData) {
  return request.put(`/products/${id}/edit`, data)
}
