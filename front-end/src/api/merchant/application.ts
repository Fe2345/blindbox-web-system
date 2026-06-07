import request from '../merchant-request'

/** 查询商家信息 */
export function getMerchantInfo() {
  return request.get('/info')
}

/** 查询入驻申请状态 */
export function getApplicationStatus() {
  return request.get('/application')
}

/** 提交入驻申请 */
export function submitApplication(data: {
  name: string
  contact_name: string
  phone: string
  email?: string
  license?: string
  business_scope?: string
  supply_desc?: string
}) {
  return request.post('/application', data)
}
