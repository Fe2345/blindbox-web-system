export interface Asset {
  id: string
  productId: string
  productName: string
  productImage: string
  category: string
  rarity: 'N' | 'R' | 'SR' | 'SSR'
  description: string
  sourceType: 'blindbox' | 'exchange'
  sourceName: string
  obtainedAt: string
  status: 'available' | 'exchange_published' | 'exchange_locked' | 'pending_shipment' | 'shipped' | 'recycled' | 'completed'
  estimatedPoints: number
  recyclablePoints: number
  canRecycle: boolean
  canShip: boolean
  canExchange: boolean
}
