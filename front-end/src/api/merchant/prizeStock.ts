import request from '../merchant-request'

// 获取商家关联商品的奖池库存
export function getPrizeStockList() {
  return request.get('/prize-stock')
}

// 补充奖池库存
export function replenishPrizeStock(prizeId: string, quantity: number) {
  return request.post(`/prize-stock/${prizeId}/replenish`, { quantity })
}

// 获取待发货订单列表
export function getShipmentOrders() {
  return request.get('/shipment-orders')
}

// 确认发货
export function confirmShip(recordId: string) {
  return request.post(`/shipment-orders/${recordId}/ship`)
}
