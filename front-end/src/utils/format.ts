export function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const h = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${y}-${m}-${day} ${h}:${min}`
}

export function formatPoints(points: number): string {
  return points.toLocaleString()
}

export function formatProbability(probability: number): string {
  return Number(probability).toFixed(2).replace(/\.?0+$/, '')
}

export function rarityLabel(rarity: string): string {
  const map: Record<string, string> = { N: '普通', R: '稀有', SR: '超稀有', SSR: '传说' }
  return map[rarity] || rarity
}

export function rarityColor(rarity: string): string {
  const map: Record<string, string> = { N: '#909399', R: '#409EFF', SR: '#E6A23C', SSR: '#F56C6C' }
  return map[rarity] || '#909399'
}

export function assetStatusLabel(status: string): string {
  const map: Record<string, string> = {
    available: '可操作',
    exchange_published: '换物发布中',
    exchange_locked: '交换锁定中',
    pending_shipment: '待发货',
    shipped: '已发货',
    recycled: '已回收',
    completed: '已完成',
  }
  return map[status] || status
}

export function assetStatusType(status: string): string {
  const map: Record<string, string> = {
    available: 'success',
    exchange_published: 'warning',
    exchange_locked: 'info',
    pending_shipment: 'primary',
    shipped: 'primary',
    recycled: 'info',
    completed: 'info',
  }
  return map[status] || 'info'
}

export function orderStatusLabel(status: string): string {
  const map: Record<string, string> = { pending: '待发货', shipped: '已发货', completed: '已完成' }
  return map[status] || status
}

export function pointsTypeLabel(type: string): string {
  const map: Record<string, string> = {
    blindbox_consume: '盲盒消费',
    recycle_return: '回收返还',
    recharge: '积分充值',
    system_adjust: '系统调整',
  }
  return map[type] || type
}

export function transactionTypeLabel(type: string): string {
  const map: Record<string, string> = {
    blindbox_draw: '盲抽记录',
    recycle: '回收记录',
    shipment: '发货记录',
    exchange: '换物记录',
  }
  return map[type] || type
}

export function merchantStatusLabel(status: string): string {
  const map: Record<string, string> = { pending: '待审核', approved: '已通过', rejected: '已驳回', frozen: '已冻结' }
  return map[status] || status
}

export function merchantStatusType(status: string): string {
  const map: Record<string, string> = { pending: 'warning', approved: 'success', rejected: 'danger', frozen: 'info' }
  return map[status] || 'info'
}

export function exchangeStatusLabel(status: string): string {
  const map: Record<string, string> = {
    pending: '待处理',
    accepted: '已接受',
    rejected: '已拒绝',
    locked: '交换锁定',
    completed: '已完成',
    cancelled: '已取消',
    exception: '异常',
  }
  return map[status] || status
}

export function exceptionTypeLabel(type: string): string {
  const map: Record<string, string> = {
    stock: '库存异常',
    order: '订单异常',
    duplicate: '重复异常',
    appeal: '用户申诉',
    other: '其他',
  }
  return map[type] || type
}

export function productStatusLabel(status: string): string {
  const map: Record<string, string> = { pending: '待审核', approved: '审核通过', rejected: '审核驳回', offline: '已下架' }
  return map[status] || status
}

export function productStatusType(status: string): string {
  const map: Record<string, string> = { pending: 'warning', approved: 'success', rejected: 'danger', offline: 'info' }
  return map[status] || 'info'
}

export function stockStatusLabel(status: string): string {
  const map: Record<string, string> = { normal: '正常', low: '库存不足', empty: '库存为零' }
  return map[status] || status
}

export function stockStatusType(status: string): string {
  const map: Record<string, string> = { normal: 'success', low: 'warning', empty: 'danger' }
  return map[status] || 'info'
}

export function shipmentStatusLabel(status: string): string {
  const map: Record<string, string> = { pending: '待发货', shipped: '已发货' }
  return map[status] || status
}

export function shipmentStatusType(status: string): string {
  const map: Record<string, string> = { pending: 'warning', shipped: 'success' }
  return map[status] || 'info'
}

export function recordTypeLabel(type: string): string {
  const map: Record<string, string> = { inventory: '库存记录', shipment: '发货记录', status_change: '状态变更' }
  return map[type] || type
}

export function recordTypeColor(type: string): string {
  const map: Record<string, string> = { inventory: 'primary', shipment: 'success', status_change: 'warning' }
  return map[type] || 'info'
}
