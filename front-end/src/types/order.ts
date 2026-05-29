export interface Order {
  id: string
  orderNo: string
  type: 'shipment' | 'exchange'
  assetId: string
  assetName: string
  assetImage: string
  status: 'pending' | 'shipped' | 'completed'
  address: {
    name: string
    phone: string
    fullAddress: string
  }
  logistics: {
    company: string
    trackingNo: string
  } | null
  createdAt: string
  shippedAt: string | null
  completedAt: string | null
}

export interface AdminOrder {
  id: string
  orderNo: string
  type: 'shipment' | 'exchange'
  userId: string
  username: string
  assetName: string
  assetImage: string
  status: 'pending' | 'shipped' | 'completed'
  address: { name: string; phone: string; fullAddress: string }
  logistics: { company: string; trackingNo: string } | null
  createdAt: string
  shippedAt: string | null
  completedAt: string | null
}
