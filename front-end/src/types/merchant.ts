export interface Merchant {
  id: string
  name: string
  contactName: string
  phone: string
  email: string
  license: string
  businessScope: string
  supplyDescription: string
  status: 'pending' | 'approved' | 'rejected' | 'frozen'
  creditScore: number
  supplyCount: number
  violationCount: number
  reviewNote: string
  createdAt: string
  reviewedAt: string | null
}
