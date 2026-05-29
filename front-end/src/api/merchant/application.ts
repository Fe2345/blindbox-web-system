import request from '../merchant-request'

export function submitApplication(data: {
  merchantName: string
  contactName: string
  phone: string
  businessScope: string
  supplyDescription: string
}) {
  return request.post('/application', data)
}

export function getApplicationStatus() {
  return request.get('/application')
}
