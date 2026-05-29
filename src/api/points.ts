import request from './request'

export function getPointsRecords() {
  return request.get('/points/records')
}

export function getPointsBalance() {
  return request.get('/points/balance')
}

export function getTransactions() {
  return request.get('/transactions')
}
