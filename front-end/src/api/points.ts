import request from './request'

export function getPointsRecords() {
  return request.get('/points/records')
}

export function getPointsBalance() {
  return request.get('/points/balance')
}

export function rechargePoints(amountYuan: number) {
  return request.post('/points/recharge', { amountYuan })
}

export function getTransactions() {
  return request.get('/transactions')
}
