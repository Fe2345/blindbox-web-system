export interface PointsRecord {
  id: string
  type: 'blindbox_consume' | 'recycle_return' | 'system_adjust' | 'recharge'
  amount: number
  balance: number
  description: string
  relatedId: string
  createdAt: string
}

export interface TransactionRecord {
  id: string
  type: 'blindbox_draw' | 'recycle' | 'shipment' | 'exchange'
  description: string
  relatedAssetName: string
  statusChange: string
  createdAt: string
}
