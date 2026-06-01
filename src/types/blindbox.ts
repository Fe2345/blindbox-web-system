export interface BlindBox {
  id: string
  name: string
  cover: string
  description: string
  costPoints: number
  stock: number
  status: 'active' | 'low_stock' | 'ended'
  category: string
  startTime: string
  endTime: string
  prizes: BlindBoxPrize[]
}

export interface BlindBoxPrize {
  id: string
  name: string
  image: string
  rarity: 'N' | 'R' | 'SR' | 'SSR'
  probability: number
  stock: number
}

export interface DrawResult {
  id: string
  prizeId: string
  prizeName: string
  prizeImage: string
  rarity: 'N' | 'R' | 'SR' | 'SSR'
  blindBoxId: string
  blindBoxName: string
  costPoints: number
  remainingPoints: number
  drawTime: string
}

export interface AdminBlindBox {
  id: string
  name: string
  cover: string
  description: string
  category: string
  costPoints: number
  stock: number
  status: 'active' | 'inactive' | 'ended'
  startTime: string
  endTime: string
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
  stock: number
}
