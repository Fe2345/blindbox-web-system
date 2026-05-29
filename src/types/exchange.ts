export interface ExchangePost {
  id: string
  userId: string
  username: string
  assetId: string
  assetName: string
  assetImage: string
  assetRarity: 'N' | 'R' | 'SR' | 'SSR'
  assetCategory: string
  expectDescription: string
  remark: string
  status: 'published' | 'locked' | 'completed' | 'cancelled'
  createdAt: string
}

export interface ExchangeApplication {
  id: string
  postId: string
  applicantId: string
  applicantName: string
  applicantAssetId: string
  applicantAssetName: string
  applicantAssetImage: string
  applicantAssetRarity: 'N' | 'R' | 'SR' | 'SSR'
  postAssetId: string
  postAssetName: string
  postAssetImage: string
  postAssetRarity: 'N' | 'R' | 'SR' | 'SSR'
  remark: string
  status: 'pending' | 'accepted' | 'rejected' | 'cancelled'
  createdAt: string
}

export interface AdminExchange {
  id: string
  postId: string
  publisherId: string
  publisherName: string
  publisherAssetName: string
  applicantId: string
  applicantName: string
  applicantAssetName: string
  status: 'pending' | 'accepted' | 'locked' | 'completed' | 'cancelled' | 'exception'
  createdAt: string
}
