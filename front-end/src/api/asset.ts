import request from './request'

export function getAssets() {
  return request.get('/assets')
}

export function getAssetDetail(id: string) {
  return request.get(`/assets/${id}`)
}

export function recycleAsset(id: string) {
  return request.post(`/assets/${id}/recycle`)
}

export function shipAsset(id: string) {
  return request.post(`/assets/${id}/ship`)
}

export function publishExchange(id: string, data: { expectDescription: string; remark: string }) {
  return request.post(`/assets/${id}/publish-exchange`, data)
}
