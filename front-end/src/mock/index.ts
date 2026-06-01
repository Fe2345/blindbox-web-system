import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import {
  mockBlindBoxes,
  mockAssets,
  mockOrders,
  mockExchangePosts,
  mockExchangeApplications,
  mockPointsRecords,
  mockTransactionRecords,
  mockMerchants,
  mockAdminUsers,
  mockProducts,
  mockAdminBlindBoxes,
  mockAdminOrders,
  mockAdminExchanges,
  mockRules,
  mockOpLogs,
  mockExceptions,
  mockLedger,
  mockMerchantApplication,
  mockMerchantProducts,
  mockMerchantInventory,
  mockInventoryRecords,
  mockShipmentTasks,
  mockMerchantRecords,
} from './data'

let mock: MockAdapter | null = null

export function setupMock() {
  if (mock) return
  mock = new MockAdapter(axios, { delayResponse: 300, onNoMatch: 'passthrough' })

  // ==================== User API ====================
  // 用户相关接口（login/register/user/addresses）已接入真实后端，不再 mock

  // BlindBox
  mock.onGet('/user/api/blindboxes').reply(() => {
    return [200, { code: 200, data: mockBlindBoxes, message: 'ok' }]
  })

  mock.onGet(/\/user\/api\/blindboxes\/.*/).reply((config) => {
    const id = config.url?.split('/').pop()
    const box = mockBlindBoxes.find((b) => b.id === id)
    if (box) return [200, { code: 200, data: box, message: 'ok' }]
    return [404, { code: -1, data: null, message: '盲盒不存在' }]
  })

  mock.onPost(/\/user\/api\/blindboxes\/.*\/draw/).reply((config) => {
    const id = config.url?.split('/')[3]
    const box = mockBlindBoxes.find((b) => b.id === id)
    if (!box) return [404, { code: -1, data: null, message: '盲盒不存在' }]
    if (box.stock <= 0) return [200, { code: -1, data: null, message: '库存不足' }]
    const rand = Math.random() * 100
    let cum = 0
    let prize = box.prizes[0]
    for (const p of box.prizes) {
      cum += p.probability
      if (rand <= cum) { prize = p; break }
    }
    box.stock--
    return [200, {
      code: 200,
      data: {
        id: 'draw' + Date.now(),
        prizeId: prize.id,
        prizeName: prize.name,
        prizeImage: prize.image,
        rarity: prize.rarity,
        blindBoxId: box.id,
        blindBoxName: box.name,
        costPoints: box.costPoints,
        remainingPoints: 930 - box.costPoints,
        drawTime: new Date().toISOString(),
      },
      message: 'ok',
    }]
  })

  // Assets
  mock.onGet('/user/api/assets').reply(() => {
    return [200, { code: 200, data: mockAssets, message: 'ok' }]
  })

  mock.onGet(/\/user\/api\/assets\/.*/).reply((config) => {
    const id = config.url?.split('/').pop()
    const asset = mockAssets.find((a) => a.id === id)
    if (asset) return [200, { code: 200, data: asset, message: 'ok' }]
    return [404, { code: -1, data: null, message: '资产不存在' }]
  })

  mock.onPost(/\/user\/api\/assets\/.*\/recycle/).reply((config) => {
    const id = config.url?.split('/')[3]
    const asset = mockAssets.find((a) => a.id === id)
    if (!asset) return [404, { code: -1, data: null, message: '资产不存在' }]
    if (asset.status !== 'available') return [200, { code: -1, data: null, message: '当前状态不可回收' }]
    asset.status = 'recycled'
    return [200, { code: 200, data: { recycledPoints: asset.recyclablePoints }, message: '回收成功' }]
  })

  mock.onPost(/\/user\/api\/assets\/.*\/ship/).reply((config) => {
    const id = config.url?.split('/')[3]
    const asset = mockAssets.find((a) => a.id === id)
    if (!asset) return [404, { code: -1, data: null, message: '资产不存在' }]
    if (asset.status !== 'available') return [200, { code: -1, data: null, message: '当前状态不可发货' }]
    asset.status = 'pending_shipment'
    return [200, { code: 200, data: null, message: '发货申请已提交' }]
  })

  mock.onPost(/\/user\/api\/assets\/.*\/publish-exchange/).reply((config) => {
    const id = config.url?.split('/')[3]
    const asset = mockAssets.find((a) => a.id === id)
    if (!asset) return [404, { code: -1, data: null, message: '资产不存在' }]
    if (asset.status !== 'available') return [200, { code: -1, data: null, message: '当前状态不可换物' }]
    asset.status = 'exchange_published'
    return [200, { code: 200, data: null, message: '发布成功' }]
  })

  // Orders
  mock.onGet('/user/api/orders').reply(() => {
    return [200, { code: 200, data: mockOrders, message: 'ok' }]
  })

  mock.onPost(/\/user\/api\/orders\/.*\/confirm/).reply((config) => {
    const id = config.url?.split('/')[3]
    const order = mockOrders.find((o) => o.id === id)
    if (order) {
      order.status = 'completed'
      order.completedAt = new Date().toISOString()
    }
    return [200, { code: 200, data: null, message: '确认收货成功' }]
  })

  // Exchange
  mock.onGet('/user/api/exchange/posts').reply(() => {
    return [200, { code: 200, data: mockExchangePosts, message: 'ok' }]
  })

  mock.onGet('/user/api/exchange/applications').reply(() => {
    return [200, { code: 200, data: mockExchangeApplications, message: 'ok' }]
  })

  mock.onPost(/\/user\/api\/exchange\/posts\/.*\/apply/).reply(() => {
    return [200, { code: 200, data: null, message: '申请已提交' }]
  })

  mock.onPost(/\/user\/api\/exchange\/applications\/.*\/accept/).reply((config) => {
    const id = config.url?.split('/')[3]
    const app = mockExchangeApplications.find((a) => a.id === id)
    if (app) app.status = 'accepted'
    return [200, { code: 200, data: null, message: '已接受' }]
  })

  mock.onPost(/\/user\/api\/exchange\/applications\/.*\/reject/).reply((config) => {
    const id = config.url?.split('/')[3]
    const app = mockExchangeApplications.find((a) => a.id === id)
    if (app) app.status = 'rejected'
    return [200, { code: 200, data: null, message: '已拒绝' }]
  })

  // Points
  mock.onGet('/user/api/points/records').reply(() => {
    return [200, { code: 200, data: mockPointsRecords, message: 'ok' }]
  })

  mock.onGet('/user/api/points/balance').reply(() => {
    return [200, { code: 200, data: { balance: 930 }, message: 'ok' }]
  })

  // Transactions
  mock.onGet('/user/api/transactions').reply(() => {
    return [200, { code: 200, data: mockTransactionRecords, message: 'ok' }]
  })

  // ==================== Admin API ====================

  // Auth
  mock.onPost('/admin/api/login').reply((config) => {
    const { username, password } = JSON.parse(config.data)
    if (username === 'admin' && password === 'admin123') {
      return [200, { code: 200, data: { token: 'admin-mock-token', user: { id: 'a001', username: '超级管理员', role: 'admin' } }, message: 'ok' }]
    }
    return [200, { code: -1, data: null, message: '用户名或密码错误' }]
  })

  mock.onGet('/admin/api/info').reply(() => {
    return [200, { code: 200, data: { id: 'a001', username: '超级管理员', role: 'admin' }, message: 'ok' }]
  })

  // Dashboard
  mock.onGet('/admin/api/dashboard').reply(() => {
    return [200, {
      code: 200,
      data: {
        userCount: 1286,
        pendingMerchants: mockMerchants.filter((m) => m.status === 'pending').length,
        pendingProducts: mockProducts.filter((p) => p.status === 'pending').length,
        pendingOrders: mockAdminOrders.filter((o) => o.status === 'pending').length,
        openExceptions: mockExceptions.filter((e) => e.status !== 'resolved').length,
        totalBlindBoxes: mockAdminBlindBoxes.length,
        activeBlindBoxes: mockAdminBlindBoxes.filter((b) => b.status === 'active').length,
        todos: [
          { id: 1, title: '审核新商家「数码好物坊」', type: 'merchant', link: '/merchant-review' },
          { id: 2, title: '审核商品「无线蓝牙耳机」', type: 'product', link: '/product-review' },
          { id: 3, title: '处理换物异常记录', type: 'exchange', link: '/exchange-manage' },
          { id: 4, title: '库存异常待核查', type: 'exception', link: '/exception' },
        ],
      },
      message: 'ok',
    }]
  })

  // Merchants
  mock.onGet('/admin/api/merchants').reply(() => [200, { code: 200, data: mockMerchants, message: 'ok' }])
  mock.onGet(/\/admin\/api\/merchants\/.*/).reply((config) => {
    const id = config.url?.split('/').pop()
    const m = mockMerchants.find((x) => x.id === id)
    return m ? [200, { code: 200, data: m, message: 'ok' }] : [404, { code: -1, data: null, message: 'not found' }]
  })
  mock.onPost(/\/admin\/api\/merchants\/.*\/review/).reply((config) => {
    const id = config.url?.split('/')[4]
    const { action, note } = JSON.parse(config.data)
    const m = mockMerchants.find((x) => x.id === id)
    if (m) { m.status = action === 'approve' ? 'approved' : 'rejected'; m.reviewNote = note; m.reviewedAt = new Date().toISOString() }
    return [200, { code: 200, data: null, message: '审核完成' }]
  })
  mock.onPut(/\/admin\/api\/merchants\/.*\/status/).reply((config) => {
    const id = config.url?.split('/')[4]
    const { status } = JSON.parse(config.data)
    const m = mockMerchants.find((x) => x.id === id)
    if (m) m.status = status
    return [200, { code: 200, data: null, message: '修改成功' }]
  })

  // Users
  mock.onGet('/admin/api/users').reply(() => [200, { code: 200, data: mockAdminUsers, message: 'ok' }])
  mock.onPut(/\/admin\/api\/users\/.*\/status/).reply((config) => {
    const id = config.url?.split('/')[4]
    const { status } = JSON.parse(config.data)
    const u = mockAdminUsers.find((x) => x.id === id)
    if (u) u.status = status
    return [200, { code: 200, data: null, message: '修改成功' }]
  })

  // Products
  mock.onGet('/admin/api/products').reply(() => [200, { code: 200, data: mockProducts, message: 'ok' }])
  mock.onPost(/\/admin\/api\/products\/.*\/review/).reply((config) => {
    const id = config.url?.split('/')[4]
    const { action, note } = JSON.parse(config.data)
    const p = mockProducts.find((x) => x.id === id)
    if (p) { p.status = action === 'approve' ? 'approved' : 'rejected'; p.reviewNote = note }
    return [200, { code: 200, data: null, message: '审核完成' }]
  })
  mock.onPost('/admin/api/products').reply(() => [200, { code: 200, data: null, message: '添加成功' }])
  mock.onPut(/\/admin\/api\/products\/.*/).reply(() => [200, { code: 200, data: null, message: '修改成功' }])
  mock.onPost(/\/admin\/api\/products\/.*\/offline/).reply((config) => {
    const id = config.url?.split('/')[4]
    const p = mockProducts.find((x) => x.id === id)
    if (p) p.status = 'offline'
    return [200, { code: 200, data: null, message: '已下架' }]
  })

  // BlindBoxes
  mock.onGet('/admin/api/blindboxes').reply(() => [200, { code: 200, data: mockAdminBlindBoxes, message: 'ok' }])
  mock.onPost('/admin/api/blindboxes').reply(() => [200, { code: 200, data: null, message: '添加成功' }])
  mock.onPut(/\/admin\/api\/blindboxes\/.*/).reply(() => [200, { code: 200, data: null, message: '修改成功' }])
  mock.onPut(/\/admin\/api\/blindboxes\/.*\/status/).reply((config) => {
    const id = config.url?.split('/')[4]
    const { status } = JSON.parse(config.data)
    const b = mockAdminBlindBoxes.find((x) => x.id === id)
    if (b) b.status = status
    return [200, { code: 200, data: null, message: '修改成功' }]
  })
  mock.onPost(/\/admin\/api\/blindboxes\/.*\/prizes/).reply(() => [200, { code: 200, data: null, message: '奖池已更新' }])

  // Orders
  mock.onGet('/admin/api/orders').reply(() => [200, { code: 200, data: mockAdminOrders, message: 'ok' }])
  mock.onPost(/\/admin\/api\/orders\/.*\/ship/).reply((config) => {
    const id = config.url?.split('/')[4]
    const { company, trackingNo } = JSON.parse(config.data)
    const o = mockAdminOrders.find((x) => x.id === id)
    if (o) { o.status = 'shipped'; o.logistics = { company, trackingNo }; o.shippedAt = new Date().toISOString() }
    return [200, { code: 200, data: null, message: '发货成功' }]
  })

  // Exchanges
  mock.onGet('/admin/api/exchanges').reply(() => [200, { code: 200, data: mockAdminExchanges, message: 'ok' }])
  mock.onPost(/\/admin\/api\/exchanges\/.*\/resolve/).reply((config) => {
    const id = config.url?.split('/')[4]
    const ex = mockAdminExchanges.find((x) => x.id === id)
    if (ex) ex.status = 'completed'
    return [200, { code: 200, data: null, message: '已处理' }]
  })

  // Rules
  mock.onGet('/admin/api/rules').reply(() => [200, { code: 200, data: mockRules, message: 'ok' }])
  mock.onPost('/admin/api/rules').reply((config) => {
    const data = JSON.parse(config.data)
    Object.assign(mockRules, data, { updatedAt: new Date().toISOString() })
    return [200, { code: 200, data: null, message: '保存成功' }]
  })

  // Ledger
  mock.onGet('/admin/api/ledger').reply(() => [200, { code: 200, data: mockLedger, message: 'ok' }])

  // Logs
  mock.onGet('/admin/api/logs').reply(() => [200, { code: 200, data: mockOpLogs, message: 'ok' }])

  // Exceptions
  mock.onGet('/admin/api/exceptions').reply(() => [200, { code: 200, data: mockExceptions, message: 'ok' }])
  mock.onPost(/\/admin\/api\/exceptions\/.*\/resolve/).reply((config) => {
    const id = config.url?.split('/')[4]
    const { result } = JSON.parse(config.data)
    const exc = mockExceptions.find((x) => x.id === id)
    if (exc) { exc.status = 'resolved'; exc.result = result; exc.resolvedAt = new Date().toISOString() }
    return [200, { code: 200, data: null, message: '已处理' }]
  })

  // ==================== Merchant API ====================

  // Auth
  mock.onPost('/merchant/api/login').reply((config) => {
    const { username, password } = JSON.parse(config.data)
    if (username === 'merchant' && password === 'merchant123') {
      return [200, {
        code: 200,
        data: {
          token: 'merchant-mock-token',
          merchant: {
            id: 'm001',
            name: '潮玩优品',
            contactName: '李明',
            phone: '13900001111',
            status: 'approved',
          },
        },
        message: 'ok',
      }]
    }
    return [200, { code: -1, data: null, message: '用户名或密码错误' }]
  })

  mock.onGet('/merchant/api/info').reply(() => {
    return [200, {
      code: 200,
      data: {
        id: 'm001',
        name: '潮玩优品',
        contactName: '李明',
        phone: '13900001111',
        email: 'liming@chaowan.com',
        businessScope: '动漫周边、潮玩手办、IP联名产品',
        supplyDescription: '专注原神、泡泡玛特等热门IP周边供货',
        status: 'approved',
        creditScore: 95,
        supplyCount: 12,
        violationCount: 0,
        reviewNote: '资质齐全，审核通过',
        createdAt: '2026-01-15',
        reviewedAt: '2026-01-16',
      },
      message: 'ok',
    }]
  })

  // Application
  mock.onGet('/merchant/api/application').reply(() => {
    return [200, { code: 200, data: mockMerchantApplication, message: 'ok' }]
  })

  mock.onPost('/merchant/api/application').reply(() => {
    return [200, { code: 200, data: null, message: '申请已提交' }]
  })

  // Dashboard
  mock.onGet('/merchant/api/dashboard').reply(() => {
    return [200, {
      code: 200,
      data: {
        totalProducts: mockMerchantProducts.length,
        pendingProducts: mockMerchantProducts.filter((p) => p.status === 'pending').length,
        lowStockProducts: mockMerchantInventory.filter((i) => i.stockStatus === 'low' || i.stockStatus === 'empty').length,
        pendingShipments: mockShipmentTasks.filter((s) => s.status === 'pending').length,
        reviewStatus: 'approved',
        todos: [
          { id: 1, title: '审核中的商品「雷电将军手办」', type: 'product', link: '/products' },
          { id: 2, title: '待发货任务 2 个', type: 'shipment', link: '/shipments' },
          { id: 3, title: '库存预警：MOLLY-成都造型库存不足', type: 'stock', link: '/inventory' },
        ],
      },
      message: 'ok',
    }]
  })

  // Products
  mock.onGet('/merchant/api/products').reply(() => {
    return [200, { code: 200, data: mockMerchantProducts, message: 'ok' }]
  })

  mock.onGet(/\/merchant\/api\/products\/[^/]+$/).reply((config) => {
    const id = config.url?.split('/').pop()
    const p = mockMerchantProducts.find((x) => x.id === id)
    return p ? [200, { code: 200, data: p, message: 'ok' }] : [404, { code: -1, data: null, message: '商品不存在' }]
  })

  mock.onPost('/merchant/api/products').reply((config) => {
    const data = JSON.parse(config.data)
    const newProduct = {
      id: 'prod' + Date.now(),
      ...data,
      status: 'pending',
      reviewNote: '',
      createdAt: new Date().toISOString().split('T')[0],
    }
    mockMerchantProducts.push(newProduct)
    return [200, { code: 200, data: newProduct, message: '提交成功，等待审核' }]
  })

  mock.onPut(/\/merchant\/api\/products\/[^/]+$/).reply((config) => {
    const id = config.url?.split('/').pop()
    const data = JSON.parse(config.data)
    const p = mockMerchantProducts.find((x) => x.id === id)
    if (p) Object.assign(p, data)
    return [200, { code: 200, data: null, message: '修改成功' }]
  })

  // Inventory
  mock.onGet('/merchant/api/inventory').reply(() => {
    return [200, { code: 200, data: mockMerchantInventory, message: 'ok' }]
  })

  mock.onPut(/\/merchant\/api\/inventory\/[^/]+$/).reply((config) => {
    const id = config.url?.split('/').pop()
    const { stock } = JSON.parse(config.data)
    const item = mockMerchantInventory.find((x) => x.productId === id)
    if (item) {
      item.currentStock = stock
      item.stockStatus = stock === 0 ? 'empty' : stock <= 5 ? 'low' : 'normal'
    }
    return [200, { code: 200, data: null, message: '库存已更新' }]
  })

  mock.onGet('/merchant/api/inventory/records').reply(() => {
    return [200, { code: 200, data: mockInventoryRecords, message: 'ok' }]
  })

  // Shipments
  mock.onGet('/merchant/api/shipments').reply(() => {
    return [200, { code: 200, data: mockShipmentTasks, message: 'ok' }]
  })

  mock.onGet(/\/merchant\/api\/shipments\/[^/]+$/).reply((config) => {
    const id = config.url?.split('/').pop()
    const s = mockShipmentTasks.find((x) => x.id === id)
    return s ? [200, { code: 200, data: s, message: 'ok' }] : [404, { code: -1, data: null, message: '任务不存在' }]
  })

  mock.onPost(/\/merchant\/api\/shipments\/.*\/ship/).reply((config) => {
    const id = config.url?.split('/')[4]
    const { logisticsCompany, trackingNo } = JSON.parse(config.data)
    const s = mockShipmentTasks.find((x) => x.id === id)
    if (s) {
      s.status = 'shipped'
      s.logisticsCompany = logisticsCompany
      s.trackingNo = trackingNo
      s.shippedAt = new Date().toISOString()
    }
    return [200, { code: 200, data: null, message: '发货成功' }]
  })

  // Records
  mock.onGet('/merchant/api/records').reply(() => {
    return [200, { code: 200, data: mockMerchantRecords, message: 'ok' }]
  })
}
