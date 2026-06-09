export interface BlindBox {
  id: string
  name: string
  cover: string
  description: string
  category: string
  ipName: string
  costPoints: number
  status: 'active' | 'inactive' | 'ended'
  startTime: string
  endTime: string
  maxDrawCount: number
  allowSimulation: boolean
  sortOrder: number
  prizes: BlindBoxPrize[]
}

export interface BlindBoxPrize {
  id: string
  name: string
  image: string
  rarity: 'N' | 'R' | 'SR' | 'SSR'
  probability: number
  weight: number
  quantity: number
  remainingQuantity: number
  isActive: boolean
  ipNameSnapshot: string
  estimatedPoints?: number
  recyclablePoints?: number
}

export interface DrawResult {
  id: string
  assetId: string
  prizeId: string
  prizeName: string
  prizeImage: string
  rarity: 'N' | 'R' | 'SR' | 'SSR'
  blindBoxId: string
  blindBoxName: string
  costPoints: number
  remainingPoints: number
  batchNo: string
  drawType: 'real' | 'simulation'
  drawStatus: 'success' | 'failed'
  drawTime: string
}

export interface DrawBatchResult {
  batchNo: string
  count: number
  totalCostPoints: number
  remainingPoints: number
  blindBoxId: string
  blindBoxName: string
  results: DrawResult[]
}

export interface AdminBlindBox {
  id: string
  name: string
  cover: string
  description: string
  category: string
  ipName: string
  costPoints: number
  status: 'active' | 'inactive' | 'ended'
  startTime: string
  endTime: string
  maxDrawCount: number
  allowSimulation: boolean
  sortOrder: number
  prizes: AdminPrize[]
  createdAt: string
}

export interface AdminPrize {
  id: string
  productId: string
  name: string
  image: string
  rarity: 'N' | 'R' | 'SR' | 'SSR'
  probability: number
  weight: number
  quantity: number
  remainingQuantity: number
  isActive: boolean
  ipNameSnapshot: string
  estimatedPoints?: number
  recyclablePoints?: number
}
