import request from './request'

export function getExchangePosts() {
  return request.get('/exchange/posts')
}

export function applyExchange(postId: string, data: { assetId: string; remark: string }) {
  return request.post(`/exchange/posts/${postId}/apply`, data)
}

export function getExchangeApplications() {
  return request.get('/exchange/applications')
}

export function acceptApplication(id: string) {
  return request.post(`/exchange/applications/${id}/accept`)
}

export function rejectApplication(id: string) {
  return request.post(`/exchange/applications/${id}/reject`)
}
