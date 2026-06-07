/** 商家信息 */
export interface MerchantInfo {
  id: number
  username: string
  name: string
  contact_name: string
  phone: string
  email: string
  license: string
  business_scope: string
  supply_desc: string
  status: 'pending' | 'approved' | 'rejected' | 'frozen'
  status_display: string
  credit_score: number
  review_note: string
  reviewed_at: string | null
  created_at: string
}

/** 商家入驻申请参数 */
export interface MerchantApplicationData {
  name: string
  contact_name: string
  phone: string
  email?: string
  license?: string
  business_scope?: string
  supply_desc?: string
}

/** 商家工作台数据 */
export interface MerchantDashboard {
  totalProducts: number
  pendingProducts: number
  lowStockProducts: number
  pendingShipments: number
  totalStock: number
  todos: MerchantTodo[]
}

/** 待办事项 */
export interface MerchantTodo {
  id: string
  title: string
  link: string
}

/** 商品信息 */
export interface MerchantProduct {
  id: number
  name: string
  image: string
  category: string
  rarity: 'N' | 'R' | 'SR' | 'SSR'
  rarity_display: string
  description?: string
  estimated_points: number
  status: 'pending' | 'approved' | 'rejected' | 'offline'
  status_display: string
  inventory_stock: number
  review_note: string
  created_at: string
  updated_at?: string
}

/** 库存信息 */
export interface InventoryItem {
  id: number
  product: number
  product_name: string
  product_image: string
  product_category: string
  product_rarity: string
  product_status: string
  current_stock: number
  updated_at: string
}

/** 库存变动记录 */
export interface InventoryRecord {
  id: number
  product: number
  product_name: string
  type: 'increase' | 'decrease' | 'modify'
  type_display: string
  before_stock: number
  after_stock: number
  reason: string
  created_at: string
}

/** 发货任务 */
export interface ShipmentTask {
  id: number
  task_no: string
  order_no: string
  product: number
  product_name: string
  product_image: string
  receiver_name: string
  receiver_phone: string
  receiver_address?: string
  status: 'pending' | 'shipped'
  status_display: string
  logistics_company: string
  tracking_no: string
  shipped_at: string | null
  created_at: string
  updated_at?: string
}

/** 操作记录 */
export interface MerchantRecord {
  id: string | number
  type: string
  type_display: string
  description: string
  created_at: string
}

/** 分页响应 */
export interface PaginatedResponse<T> {
  count: number
  page: number
  page_size: number
  results: T[]
}

/** API 响应 */
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}
