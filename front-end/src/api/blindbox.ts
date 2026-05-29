import request from './request'

export function getBlindBoxes() {
  return request.get('/blindboxes')
}

export function getBlindBoxDetail(id: string) {
  return request.get(`/blindboxes/${id}`)
}

export function drawBlindBox(id: string) {
  return request.post(`/blindboxes/${id}/draw`)
}
