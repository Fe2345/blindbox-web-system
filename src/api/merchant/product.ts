import request from '../merchant-request'

export function getMerchantProducts(params?: { status?: string; keyword?: string }) {
  return request.get('/products', { params })
}

export function getMerchantProductDetail(id: string) {
  return request.get(`/products/${id}`)
}

export function submitProduct(data: {
  name: string
  image: string
  description: string
  category: string
  rarity: string
  stock: number
}) {
  return request.post('/products', data)
}

export function updateProduct(id: string, data: {
  name?: string
  image?: string
  description?: string
  stock?: number
}) {
  return request.put(`/products/${id}`, data)
}
