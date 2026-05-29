export interface Product {
  id: string
  name: string
  image: string
  category: string
  rarity: 'N' | 'R' | 'SR' | 'SSR'
  description: string
  merchantId: string
  merchantName: string
  stock: number
  estimatedPoints: number
  status: 'pending' | 'approved' | 'rejected' | 'offline'
  reviewNote: string
  createdAt: string
}
