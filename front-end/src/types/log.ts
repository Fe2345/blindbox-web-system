export interface OpLog {
  id: string
  operator: string
  action: string
  target: string
  detail: string
  createdAt: string
}

export interface ExceptionRecord {
  id: string
  type: 'stock' | 'order' | 'duplicate' | 'appeal' | 'other'
  description: string
  relatedId: string
  status: 'open' | 'processing' | 'resolved'
  result: string
  createdAt: string
  resolvedAt: string | null
}
