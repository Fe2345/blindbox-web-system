export interface MerchantApplication {
  id: string
  merchantName: string
  contactName: string
  phone: string
  businessScope: string
  supplyDescription: string
  status: 'pending' | 'approved' | 'rejected'
  reviewNote: string
  createdAt: string
  reviewedAt: string | null
}

export interface MerchantProduct {
  id: string
  name: string
  image: string
  description: string
  category: string
  rarity: 'N' | 'R' | 'SR' | 'SSR'
  stock: number
  status: 'pending' | 'approved' | 'rejected' | 'offline'
  reviewNote: string
  createdAt: string
}

export interface MerchantDashboard {
  totalProducts: number
  pendingProducts: number
  lowStockProducts: number
  pendingShipments: number
  reviewStatus: string
  todos: MerchantTodo[]
}

export interface MerchantTodo {
  id: number
  title: string
  type: 'product' | 'shipment' | 'stock'
  link: string
}

export interface InventoryItem {
  id: string
  productId: string
  productName: string
  productImage: string
  currentStock: number
  stockStatus: 'normal' | 'low' | 'empty'
}

export interface InventoryRecord {
  id: string
  productId: string
  productName: string
  type: 'increase' | 'decrease' | 'modify'
  beforeStock: number
  afterStock: number
  reason: string
  createdAt: string
}

export interface ShipmentTask {
  id: string
  taskNo: string
  productName: string
  productImage: string
  orderNo: string
  receiverName: string
  receiverPhone: string
  receiverAddress: string
  status: 'pending' | 'shipped'
  createdAt: string
  shippedAt: string | null
  logisticsCompany: string | null
  trackingNo: string | null
}

export interface MerchantRecord {
  id: string
  type: 'inventory' | 'shipment' | 'status_change'
  productName: string
  description: string
  detail: string
  createdAt: string
}
