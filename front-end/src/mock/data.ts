import type { BlindBox, AdminBlindBox } from '@/types/blindbox'
import type { Asset } from '@/types/asset'
import type { Order, AdminOrder } from '@/types/order'
import type { ExchangePost, ExchangeApplication, AdminExchange } from '@/types/exchange'
import type { PointsRecord, TransactionRecord } from '@/types/points'
import type { Address, AdminUser } from '@/types/user'
import type { Merchant } from '@/types/merchant'
import type { Product } from '@/types/product'
import type { RuleConfig } from '@/types/rule'
import type { OpLog, ExceptionRecord } from '@/types/log'

export const mockBlindBoxes: BlindBox[] = [
  {
    id: 'bb001',
    name: '原神角色盲盒',
    cover: 'https://picsum.photos/seed/genshin/400/300',
    description: '原神人气角色周边，含限定联名款挂件、立牌、徽章等',
    category: '动漫IP',
    ipName: '原神',
    costPoints: 120,
    status: 'active',
    startTime: '2026-01-01',
    endTime: '2026-12-31',
    maxDrawCount: 10,
    allowSimulation: true,
    sortOrder: 1,
    prizes: [
      { id: 'p001', name: '派蒙亚克力挂件', image: 'https://picsum.photos/seed/paimon/200/200', rarity: 'N', probability: 40, weight: 40, quantity: 100, remainingQuantity: 85, isActive: true, ipNameSnapshot: '原神' },
      { id: 'p002', name: '刻晴金属徽章', image: 'https://picsum.photos/seed/keqing/200/200', rarity: 'R', probability: 30, weight: 30, quantity: 60, remainingQuantity: 48, isActive: true, ipNameSnapshot: '原神' },
      { id: 'p003', name: '雷电将军手办', image: 'https://picsum.photos/seed/raiden/200/200', rarity: 'SR', probability: 20, weight: 20, quantity: 30, remainingQuantity: 22, isActive: true, ipNameSnapshot: '原神' },
      { id: 'p004', name: '钟离限定立牌', image: 'https://picsum.photos/seed/zhongli/200/200', rarity: 'SSR', probability: 10, weight: 10, quantity: 10, remainingQuantity: 5, isActive: true, ipNameSnapshot: '原神' },
    ],
  },
  {
    id: 'bb002',
    name: 'MOLLY城市盲盒',
    cover: 'https://picsum.photos/seed/molly/400/300',
    description: '泡泡玛特MOLLY城市系列，每个城市一个造型，隐藏款概率惊喜',
    category: '潮玩',
    ipName: 'MOLLY',
    costPoints: 100,
    status: 'active',
    startTime: '2026-02-01',
    endTime: '2026-08-31',
    maxDrawCount: 10,
    allowSimulation: true,
    sortOrder: 2,
    prizes: [
      { id: 'p005', name: 'MOLLY-北京造型', image: 'https://picsum.photos/seed/mollybj/200/200', rarity: 'N', probability: 30, weight: 30, quantity: 80, remainingQuantity: 65, isActive: true, ipNameSnapshot: 'MOLLY' },
      { id: 'p006', name: 'MOLLY-上海造型', image: 'https://picsum.photos/seed/mollysh/200/200', rarity: 'R', probability: 28, weight: 28, quantity: 50, remainingQuantity: 38, isActive: true, ipNameSnapshot: 'MOLLY' },
      { id: 'p007', name: 'MOLLY-成都造型', image: 'https://picsum.photos/seed/mollycd/200/200', rarity: 'SR', probability: 25, weight: 25, quantity: 25, remainingQuantity: 15, isActive: true, ipNameSnapshot: 'MOLLY' },
      { id: 'p008', name: 'MOLLY-隐藏款星空', image: 'https://picsum.photos/seed/mollystar/200/200', rarity: 'SSR', probability: 10, weight: 10, quantity: 8, remainingQuantity: 3, isActive: true, ipNameSnapshot: 'MOLLY' },
    ],
  },
  {
    id: 'bb003',
    name: '居家生活盲盒',
    cover: 'https://picsum.photos/seed/daily/400/300',
    description: '精选居家日用好物，保温杯、香薰、收纳盒、小夜灯等实用好物',
    category: '生活',
    ipName: '',
    costPoints: 60,
    status: 'inactive',
    startTime: '2026-03-01',
    endTime: '2026-09-30',
    maxDrawCount: 5,
    allowSimulation: true,
    sortOrder: 3,
    prizes: [
      { id: 'p009', name: '创意马克杯', image: 'https://picsum.photos/seed/mug/200/200', rarity: 'N', probability: 35, weight: 35, quantity: 60, remainingQuantity: 42, isActive: true, ipNameSnapshot: '' },
      { id: 'p010', name: '无火香薰套装', image: 'https://picsum.photos/seed/aroma/200/200', rarity: 'R', probability: 30, weight: 30, quantity: 40, remainingQuantity: 28, isActive: true, ipNameSnapshot: '' },
      { id: 'p011', name: '智能保温杯', image: 'https://picsum.photos/seed/thermos/200/200', rarity: 'SR', probability: 25, weight: 25, quantity: 20, remainingQuantity: 12, isActive: true, ipNameSnapshot: '' },
      { id: 'p012', name: '星空投影灯', image: 'https://picsum.photos/seed/lamp/200/200', rarity: 'SSR', probability: 10, weight: 10, quantity: 5, remainingQuantity: 2, isActive: true, ipNameSnapshot: '' },
    ],
  },
  {
    id: 'bb004',
    name: 'SPY×FAMILY 盲盒',
    cover: 'https://picsum.photos/seed/spyfamily/400/300',
    description: '间谍过家家系列周边，阿尼亚、约尔、黄昏全家福',
    category: '动漫IP',
    ipName: 'SPY×FAMILY',
    costPoints: 90,
    status: 'ended',
    startTime: '2025-10-01',
    endTime: '2026-01-31',
    maxDrawCount: 10,
    allowSimulation: false,
    sortOrder: 4,
    prizes: [
      { id: 'p013', name: '阿尼亚哇酷哇酷挂件', image: 'https://picsum.photos/seed/anya/200/200', rarity: 'N', probability: 40, weight: 40, quantity: 100, remainingQuantity: 0, isActive: false, ipNameSnapshot: 'SPY×FAMILY' },
      { id: 'p014', name: '约尔暗夜公主徽章', image: 'https://picsum.photos/seed/yor/200/200', rarity: 'R', probability: 30, weight: 30, quantity: 60, remainingQuantity: 0, isActive: false, ipNameSnapshot: 'SPY×FAMILY' },
      { id: 'p015', name: '黄昏特工造型手办', image: 'https://picsum.photos/seed/twilight/200/200', rarity: 'SR', probability: 20, weight: 20, quantity: 30, remainingQuantity: 0, isActive: false, ipNameSnapshot: 'SPY×FAMILY' },
      { id: 'p016', name: '福杰一家全家福立牌', image: 'https://picsum.photos/seed/forger/200/200', rarity: 'SSR', probability: 10, weight: 10, quantity: 10, remainingQuantity: 0, isActive: false, ipNameSnapshot: 'SPY×FAMILY' },
    ],
  },
]

export const mockAssets: Asset[] = [
  {
    id: 'a001', productId: 'p002', productName: '刻晴金属徽章', productImage: 'https://picsum.photos/seed/keqing/200/200',
    category: '动漫IP', rarity: 'R', description: '原神刻晴角色限定金属徽章，做工精致',
    sourceType: 'blindbox', sourceName: '原神角色盲盒', obtainedAt: '2026-05-10T10:30:00',
    status: 'available', estimatedPoints: 200, recyclablePoints: 80, canRecycle: true, canShip: true, canExchange: true,
  },
  {
    id: 'a002', productId: 'p001', productName: '派蒙亚克力挂件', productImage: 'https://picsum.photos/seed/paimon/200/200',
    category: '动漫IP', rarity: 'N', description: '原神派蒙造型亚克力挂件',
    sourceType: 'blindbox', sourceName: '原神角色盲盒', obtainedAt: '2026-05-08T14:20:00',
    status: 'available', estimatedPoints: 100, recyclablePoints: 30, canRecycle: true, canShip: true, canExchange: true,
  },
  {
    id: 'a003', productId: 'p007', productName: 'MOLLY-成都造型', productImage: 'https://picsum.photos/seed/mollycd/200/200',
    category: '潮玩', rarity: 'SR', description: '泡泡玛特MOLLY城市系列成都限定',
    sourceType: 'blindbox', sourceName: 'MOLLY城市盲盒', obtainedAt: '2026-05-05T09:15:00',
    status: 'exchange_published', estimatedPoints: 500, recyclablePoints: 200, canRecycle: false, canShip: false, canExchange: false,
  },
  {
    id: 'a004', productId: 'p009', productName: '创意马克杯', productImage: 'https://picsum.photos/seed/mug/200/200',
    category: '生活', rarity: 'N', description: '创意手绘马克杯，400ml容量',
    sourceType: 'blindbox', sourceName: '居家生活盲盒', obtainedAt: '2026-05-01T16:45:00',
    status: 'pending_shipment', estimatedPoints: 80, recyclablePoints: 25, canRecycle: false, canShip: false, canExchange: false,
  },
  {
    id: 'a005', productId: 'p011', productName: '智能保温杯', productImage: 'https://picsum.photos/seed/thermos/200/200',
    category: '生活', rarity: 'SR', description: '智能温度显示保温杯，500ml大容量',
    sourceType: 'blindbox', sourceName: '居家生活盲盒', obtainedAt: '2026-04-28T11:00:00',
    status: 'recycled', estimatedPoints: 450, recyclablePoints: 180, canRecycle: false, canShip: false, canExchange: false,
  },
]

export const mockOrders: Order[] = [
  {
    id: 'o001', orderNo: 'ORD20260501001', type: 'shipment', assetId: 'a004', assetName: '创意马克杯',
    assetImage: 'https://picsum.photos/seed/mug/200/200', status: 'pending',
    address: { name: '张三', phone: '13800138000', fullAddress: '北京市朝阳区某某路123号' },
    logistics: null, createdAt: '2026-05-15T10:00:00', shippedAt: null, completedAt: null,
  },
  {
    id: 'o002', orderNo: 'ORD20260428001', type: 'shipment', assetId: 'a005', assetName: '智能保温杯',
    assetImage: 'https://picsum.photos/seed/thermos/200/200', status: 'shipped',
    address: { name: '张三', phone: '13800138000', fullAddress: '北京市朝阳区某某路123号' },
    logistics: { company: '顺丰速运', trackingNo: 'SF1234567890' },
    createdAt: '2026-04-28T14:00:00', shippedAt: '2026-04-29T09:00:00', completedAt: null,
  },
]

export const mockExchangePosts: ExchangePost[] = [
  {
    id: 'ep001', userId: 'u002', username: '潮玩收藏家', assetId: 'a003', assetName: 'MOLLY-成都造型',
    assetImage: 'https://picsum.photos/seed/mollycd/200/200', assetRarity: 'SR', assetCategory: '潮玩',
    expectDescription: '希望换取MOLLY隐藏款星空或原神SSR周边', remark: '全新未拆，附原盒',
    status: 'published', createdAt: '2026-05-10T08:00:00',
  },
  {
    id: 'ep002', userId: 'u003', username: '原神老玩家', assetId: 'a006', assetName: '钟离限定立牌',
    assetImage: 'https://picsum.photos/seed/zhongli/200/200', assetRarity: 'SSR', assetCategory: '动漫IP',
    expectDescription: '希望换取雷电将军手办或MOLLY隐藏款', remark: '全新未拆',
    status: 'published', createdAt: '2026-05-12T15:30:00',
  },
  {
    id: 'ep003', userId: 'u004', username: '生活好物分享', assetId: 'a007', assetName: '无火香薰套装',
    assetImage: 'https://picsum.photos/seed/aroma/200/200', assetRarity: 'R', assetCategory: '生活',
    expectDescription: '希望换取任意R级动漫或潮玩周边', remark: '',
    status: 'locked', createdAt: '2026-05-08T12:00:00',
  },
]

export const mockExchangeApplications: ExchangeApplication[] = [
  {
    id: 'ea001', postId: 'ep001', applicantId: 'u001', applicantName: '当前用户',
    applicantAssetId: 'a001', applicantAssetName: '刻晴金属徽章',
    applicantAssetImage: 'https://picsum.photos/seed/keqing/200/200', applicantAssetRarity: 'R',
    postAssetId: 'a003', postAssetName: 'MOLLY-成都造型',
    postAssetImage: 'https://picsum.photos/seed/mollycd/200/200', postAssetRarity: 'SR',
    remark: '我的刻晴徽章品相很好，希望可以交换', status: 'pending', createdAt: '2026-05-11T09:00:00',
  },
]

export const mockPointsRecords: PointsRecord[] = [
  { id: 'pr001', type: 'blindbox_consume', amount: -120, balance: 880, description: '抽取原神角色盲盒', relatedId: 'bb001', createdAt: '2026-05-10T10:30:00' },
  { id: 'pr002', type: 'blindbox_consume', amount: -100, balance: 780, description: '抽取MOLLY城市盲盒', relatedId: 'bb002', createdAt: '2026-05-05T09:15:00' },
  { id: 'pr003', type: 'recycle_return', amount: 180, balance: 960, description: '回收智能保温杯', relatedId: 'a005', createdAt: '2026-04-28T11:00:00' },
  { id: 'pr004', type: 'blindbox_consume', amount: -60, balance: 780, description: '抽取居家生活盲盒', relatedId: 'bb003', createdAt: '2026-04-25T16:00:00' },
  { id: 'pr005', type: 'system_adjust', amount: 500, balance: 840, description: '新用户注册赠送积分', relatedId: '', createdAt: '2026-04-20T10:00:00' },
]

export const mockTransactionRecords: TransactionRecord[] = [
  { id: 'tr001', type: 'blindbox_draw', description: '抽取原神角色盲盒', relatedAssetName: '刻晴金属徽章', statusChange: '获得新资产', createdAt: '2026-05-10T10:30:00' },
  { id: 'tr002', type: 'blindbox_draw', description: '抽取MOLLY城市盲盒', relatedAssetName: 'MOLLY-成都造型', statusChange: '获得新资产', createdAt: '2026-05-05T09:15:00' },
  { id: 'tr003', type: 'recycle', description: '回收商品', relatedAssetName: '智能保温杯', statusChange: '可回收 → 已回收', createdAt: '2026-04-28T11:00:00' },
  { id: 'tr004', type: 'shipment', description: '申请发货', relatedAssetName: '创意马克杯', statusChange: '可回收 → 待发货', createdAt: '2026-05-15T10:00:00' },
  { id: 'tr005', type: 'exchange', description: '发布换物', relatedAssetName: 'MOLLY-成都造型', statusChange: '可回收 → 换物发布中', createdAt: '2026-05-10T08:00:00' },
]

export const mockAddresses: Address[] = [
  { id: 'addr001', receiver_name: '张三', receiver_phone: '13800138000', province: { code: '110000', name: '北京市', level: 1 }, city: { code: '110100', name: '北京市', level: 2 }, district: { code: '110105', name: '朝阳区', level: 3 }, street: '', detail: '某某路123号', is_default: true },
  { id: 'addr002', receiver_name: '张三', receiver_phone: '13800138000', province: { code: '310000', name: '上海市', level: 1 }, city: { code: '310100', name: '上海市', level: 2 }, district: { code: '310115', name: '浦东新区', level: 3 }, street: '', detail: '某某大道456号', is_default: false },
]

// ========== Admin Mock Data ==========

export const mockMerchants: Merchant[] = [
  { id: 'm001', name: '潮玩优品', contactName: '李明', phone: '13900001111', email: 'liming@chaowan.com', license: '营业执照编号12345', status: 'approved', creditScore: 95, supplyCount: 12, violationCount: 0, reviewNote: '资质齐全，审核通过', createdAt: '2026-01-15', reviewedAt: '2026-01-16' },
  { id: 'm002', name: '数码好物坊', contactName: '王芳', phone: '13900002222', email: 'wangfang@digital.com', license: '营业执照编号23456', status: 'pending', creditScore: 0, supplyCount: 0, violationCount: 0, reviewNote: '', createdAt: '2026-05-18', reviewedAt: null },
  { id: 'm003', name: '零食汇', contactName: '赵强', phone: '13900003333', email: 'zhaoqiang@snack.com', license: '营业执照编号34567', status: 'approved', creditScore: 88, supplyCount: 8, violationCount: 1, reviewNote: '审核通过，注意食品资质', createdAt: '2025-11-20', reviewedAt: '2025-11-22' },
  { id: 'm004', name: '美妆小铺', contactName: '孙丽', phone: '13900004444', email: 'sunli@beauty.com', license: '营业执照编号45678', status: 'rejected', creditScore: 0, supplyCount: 0, violationCount: 0, reviewNote: '资质材料不全，需补充化妆品经营许可证', createdAt: '2026-05-10', reviewedAt: '2026-05-11' },
]

export const mockAdminUsers: AdminUser[] = [
  { id: 'u001', username: '张三', phone: '13800138000', email: 'zhangsan@test.com', status: 'active', points: 930, assetCount: 5, orderCount: 2, createdAt: '2026-04-20' },
  { id: 'u002', username: '李四', phone: '13800138001', email: 'lisi@test.com', status: 'active', points: 500, assetCount: 3, orderCount: 1, createdAt: '2026-04-22' },
  { id: 'u003', username: '王五', phone: '13800138002', email: 'wangwu@test.com', status: 'frozen', points: 200, assetCount: 1, orderCount: 0, createdAt: '2026-03-10' },
  { id: 'u004', username: '赵六', phone: '13800138003', email: 'zhaoliu@test.com', status: 'active', points: 1200, assetCount: 8, orderCount: 4, createdAt: '2026-02-15' },
]

export const mockProducts: Product[] = [
  { id: 'prod001', name: '派蒙亚克力挂件', image: 'https://picsum.photos/seed/paimon/200/200', category: '动漫IP', rarity: 'N', description: '原神派蒙造型挂件', merchantId: 'm001', merchantName: '潮玩优品', stock: 100, estimatedPoints: 50, status: 'approved', reviewNote: '', createdAt: '2026-03-01' },
  { id: 'prod002', name: '刻晴金属徽章', image: 'https://picsum.photos/seed/keqing/200/200', category: '动漫IP', rarity: 'R', description: '原神刻晴限定徽章', merchantId: 'm001', merchantName: '潮玩优品', stock: 60, estimatedPoints: 120, status: 'approved', reviewNote: '', createdAt: '2026-03-01' },
  { id: 'prod003', name: 'MOLLY-成都造型', image: 'https://picsum.photos/seed/mollycd/200/200', category: '潮玩', rarity: 'SR', description: '泡泡玛特MOLLY城市系列', merchantId: 'm001', merchantName: '潮玩优品', stock: 25, estimatedPoints: 300, status: 'approved', reviewNote: '', createdAt: '2026-02-15' },
  { id: 'prod004', name: '无线蓝牙耳机', image: 'https://picsum.photos/seed/earphone/200/200', category: '数码', rarity: 'N', description: '蓝牙5.3无线耳机', merchantId: 'm002', merchantName: '数码好物坊', stock: 80, estimatedPoints: 60, status: 'pending', reviewNote: '', createdAt: '2026-05-18' },
  { id: 'prod005', name: '智能保温杯', image: 'https://picsum.photos/seed/thermos/200/200', category: '生活', rarity: 'SR', description: '智能温度显示保温杯', merchantId: 'm003', merchantName: '零食汇', stock: 20, estimatedPoints: 280, status: 'approved', reviewNote: '', createdAt: '2026-03-10' },
  { id: 'prod006', name: '大牌香水小样', image: 'https://picsum.photos/seed/perfume/200/200', category: '美妆', rarity: 'SSR', description: '国际大牌香水试用装', merchantId: 'm004', merchantName: '美妆小铺', stock: 10, estimatedPoints: 500, status: 'rejected', reviewNote: '商家资质未通过', createdAt: '2026-05-10' },
]

export const mockAdminBlindBoxes: AdminBlindBox[] = [
  {
    id: 'bb001', name: '原神角色盲盒', cover: 'https://picsum.photos/seed/genshin/400/300',
    description: '原神人气角色周边', category: '动漫IP', ipName: '原神', costPoints: 120, status: 'active',
    startTime: '2026-01-01', endTime: '2026-12-31', maxDrawCount: 10, allowSimulation: true, sortOrder: 1, createdAt: '2025-12-20',
    prizes: [
      { id: 'p001', productId: 'prod001', name: '派蒙亚克力挂件', image: 'https://picsum.photos/seed/paimon/200/200', rarity: 'N', probability: 40, weight: 40, quantity: 100, remainingQuantity: 85, isActive: true, ipNameSnapshot: '原神' },
      { id: 'p002', productId: 'prod002', name: '刻晴金属徽章', image: 'https://picsum.photos/seed/keqing/200/200', rarity: 'R', probability: 30, weight: 30, quantity: 60, remainingQuantity: 48, isActive: true, ipNameSnapshot: '原神' },
      { id: 'p003', productId: 'prod003', name: '雷电将军手办', image: 'https://picsum.photos/seed/raiden/200/200', rarity: 'SR', probability: 20, weight: 20, quantity: 30, remainingQuantity: 22, isActive: true, ipNameSnapshot: '原神' },
      { id: 'p004', productId: 'prod004', name: '钟离限定立牌', image: 'https://picsum.photos/seed/zhongli/200/200', rarity: 'SSR', probability: 10, weight: 10, quantity: 10, remainingQuantity: 5, isActive: true, ipNameSnapshot: '原神' },
    ],
  },
  {
    id: 'bb002', name: 'MOLLY城市盲盒', cover: 'https://picsum.photos/seed/molly/400/300',
    description: '泡泡玛特MOLLY城市系列', category: '潮玩', ipName: 'MOLLY', costPoints: 100, status: 'active',
    startTime: '2026-02-01', endTime: '2026-08-31', maxDrawCount: 10, allowSimulation: true, sortOrder: 2, createdAt: '2026-01-15',
    prizes: [
      { id: 'p005', productId: 'prod005', name: 'MOLLY-北京造型', image: 'https://picsum.photos/seed/mollybj/200/200', rarity: 'N', probability: 30, weight: 30, quantity: 80, remainingQuantity: 65, isActive: true, ipNameSnapshot: 'MOLLY' },
      { id: 'p006', productId: 'prod006', name: 'MOLLY-上海造型', image: 'https://picsum.photos/seed/mollysh/200/200', rarity: 'R', probability: 28, weight: 28, quantity: 50, remainingQuantity: 38, isActive: true, ipNameSnapshot: 'MOLLY' },
      { id: 'p007', productId: 'prod007', name: 'MOLLY-成都造型', image: 'https://picsum.photos/seed/mollycd/200/200', rarity: 'SR', probability: 25, weight: 25, quantity: 25, remainingQuantity: 15, isActive: true, ipNameSnapshot: 'MOLLY' },
      { id: 'p008', productId: 'prod008', name: 'MOLLY-隐藏款星空', image: 'https://picsum.photos/seed/mollystar/200/200', rarity: 'SSR', probability: 17, weight: 17, quantity: 8, remainingQuantity: 3, isActive: true, ipNameSnapshot: 'MOLLY' },
    ],
  },
  {
    id: 'bb003', name: '居家生活盲盒', cover: 'https://picsum.photos/seed/daily/400/300',
    description: '精选居家日用好物', category: '生活', ipName: '', costPoints: 60, status: 'inactive',
    startTime: '2026-03-01', endTime: '2026-09-30', maxDrawCount: 5, allowSimulation: true, sortOrder: 3, createdAt: '2026-02-25',
    prizes: [
      { id: 'p009', productId: 'prod009', name: '创意马克杯', image: 'https://picsum.photos/seed/mug/200/200', rarity: 'N', probability: 35, weight: 35, quantity: 60, remainingQuantity: 42, isActive: true, ipNameSnapshot: '' },
      { id: 'p010', productId: 'prod010', name: '无火香薰套装', image: 'https://picsum.photos/seed/aroma/200/200', rarity: 'R', probability: 30, weight: 30, quantity: 40, remainingQuantity: 28, isActive: true, ipNameSnapshot: '' },
      { id: 'p011', productId: 'prod011', name: '智能保温杯', image: 'https://picsum.photos/seed/thermos/200/200', rarity: 'SR', probability: 25, weight: 25, quantity: 20, remainingQuantity: 12, isActive: true, ipNameSnapshot: '' },
      { id: 'p012', productId: 'prod012', name: '星空投影灯', image: 'https://picsum.photos/seed/lamp/200/200', rarity: 'SSR', probability: 10, weight: 10, quantity: 5, remainingQuantity: 2, isActive: true, ipNameSnapshot: '' },
    ],
  },
]

export const mockAdminOrders: AdminOrder[] = [
  { id: 'o001', orderNo: 'ORD20260515001', type: 'shipment', userId: 'u001', username: '张三', assetName: '创意马克杯', assetImage: 'https://picsum.photos/seed/mug/200/200', status: 'pending', address: { name: '张三', phone: '13800138000', fullAddress: '北京市朝阳区某某路123号' }, logistics: null, createdAt: '2026-05-15T10:00:00', shippedAt: null, completedAt: null },
  { id: 'o002', orderNo: 'ORD20260428001', type: 'shipment', userId: 'u001', username: '张三', assetName: '智能保温杯', assetImage: 'https://picsum.photos/seed/thermos/200/200', status: 'shipped', address: { name: '张三', phone: '13800138000', fullAddress: '北京市朝阳区某某路123号' }, logistics: { company: '顺丰速运', trackingNo: 'SF1234567890' }, createdAt: '2026-04-28T14:00:00', shippedAt: '2026-04-29T09:00:00', completedAt: null },
  { id: 'o003', orderNo: 'ORD20260510001', type: 'exchange', userId: 'u002', username: '李四', assetName: 'MOLLY-成都造型', assetImage: 'https://picsum.photos/seed/mollycd/200/200', status: 'pending', address: { name: '李四', phone: '13800138001', fullAddress: '上海市浦东新区某某大道456号' }, logistics: null, createdAt: '2026-05-10T08:00:00', shippedAt: null, completedAt: null },
]

export const mockAdminExchanges: AdminExchange[] = [
  { id: 'ex001', postId: 'ep001', publisherId: 'u002', publisherName: '潮玩收藏家', publisherAssetName: 'MOLLY-成都造型', applicantId: 'u001', applicantName: '张三', applicantAssetName: '刻晴金属徽章', status: 'locked', createdAt: '2026-05-11T09:00:00' },
  { id: 'ex002', postId: 'ep002', publisherId: 'u003', publisherName: '原神老玩家', publisherAssetName: '钟离限定立牌', applicantId: 'u004', applicantName: '赵六', applicantAssetName: '雷电将军手办', status: 'completed', createdAt: '2026-05-08T12:00:00' },
  { id: 'ex003', postId: 'ep003', publisherId: 'u001', publisherName: '张三', publisherAssetName: '智能保温杯', applicantId: 'u002', applicantName: '李四', applicantAssetName: '迷你充电宝', status: 'exception', createdAt: '2026-05-13T15:00:00' },
]

export const mockRules: RuleConfig = {
  recycleRate: 30,
  newUserPoints: 500,
  maxDrawPerDay: 20,
  minPointsToDraw: 60,
  orderAutoConfirmDays: 7,
  exchangeLockHours: 48,
  updatedAt: '2026-05-01T10:00:00',
  updatedBy: '超级管理员',
}

export const mockOpLogs: OpLog[] = [
  { id: 'log001', operator: '超级管理员', action: '审核商家', target: '潮玩优品', detail: '审核通过', createdAt: '2026-01-16T10:00:00' },
  { id: 'log002', operator: '超级管理员', action: '审核商家', target: '美妆小铺', detail: '驳回，资质不全', createdAt: '2026-05-11T14:00:00' },
  { id: 'log003', operator: '超级管理员', action: '配置盲盒', target: '原神角色盲盒', detail: '修改库存为50', createdAt: '2026-05-01T09:00:00' },
  { id: 'log004', operator: '超级管理员', action: '修改规则', target: '系统规则', detail: '新用户积分调整为500', createdAt: '2026-05-01T10:00:00' },
  { id: 'log005', operator: '超级管理员', action: '禁用用户', target: '王五', detail: '违规操作，冻结账户', createdAt: '2026-04-15T16:00:00' },
  { id: 'log006', operator: '超级管理员', action: '审核商品', target: '大牌香水小样', detail: '驳回，商家资质未通过', createdAt: '2026-05-10T11:00:00' },
]

export const mockExceptions: ExceptionRecord[] = [
  { id: 'exc001', type: 'stock', description: 'MOLLY-隐藏款星空库存与实际不一致', relatedId: 'bb002', status: 'open', result: '', createdAt: '2026-05-18T09:00:00', resolvedAt: null },
  { id: 'exc002', type: 'appeal', description: '用户张三申诉换物被误操作锁定', relatedId: 'ex003', status: 'processing', result: '', createdAt: '2026-05-14T10:00:00', resolvedAt: null },
  { id: 'exc003', type: 'order', description: '订单ORD20260428001物流信息异常', relatedId: 'o002', status: 'resolved', result: '已联系物流公司核实，确认正常', createdAt: '2026-05-02T14:00:00', resolvedAt: '2026-05-03T09:00:00' },
]

export const mockLedger = [
  { id: 'led001', type: 'blindbox_draw', description: '张三抽取原神角色盲盒', amount: -120, createdAt: '2026-05-10T10:30:00' },
  { id: 'led002', type: 'recycle', description: '李四回收智能保温杯', amount: 180, createdAt: '2026-04-28T11:00:00' },
  { id: 'led003', type: 'shipment', description: '张三申请发货创意马克杯', amount: 0, createdAt: '2026-05-15T10:00:00' },
  { id: 'led004', type: 'exchange', description: '换物：刻晴徽章 ↔ MOLLY成都', amount: 0, createdAt: '2026-05-11T09:00:00' },
  { id: 'led005', type: 'system', description: '新用户注册赠送积分', amount: 500, createdAt: '2026-04-20T10:00:00' },
]

// ========== Merchant Self-Service Mock Data ==========

import type { MerchantApplication, MerchantProduct, InventoryItem, InventoryRecord, ShipmentTask, MerchantRecord } from '@/types/merchant-self'

export const mockMerchantApplication: MerchantApplication = {
  id: 'app001',
  merchantName: '潮玩优品',
  contactName: '李明',
  phone: '13900001111',
  businessScope: '动漫周边、潮玩手办、IP联名产品',
  supplyDescription: '专注原神、泡泡玛特等热门IP周边供货，品质优良，价格合理',
  status: 'approved',
  reviewNote: '资质齐全，审核通过',
  createdAt: '2026-01-15',
  reviewedAt: '2026-01-16',
}

export const mockMerchantProducts: MerchantProduct[] = [
  { id: 'prod001', name: '派蒙亚克力挂件', image: 'https://picsum.photos/seed/paimon/200/200', description: '原神派蒙造型亚克力挂件', category: '动漫IP', rarity: 'N', stock: 100, status: 'approved', reviewNote: '', createdAt: '2026-03-01' },
  { id: 'prod002', name: '刻晴金属徽章', image: 'https://picsum.photos/seed/keqing/200/200', description: '原神刻晴限定金属徽章', category: '动漫IP', rarity: 'R', stock: 60, status: 'approved', reviewNote: '', createdAt: '2026-03-01' },
  { id: 'prod003', name: 'MOLLY-成都造型', image: 'https://picsum.photos/seed/mollycd/200/200', description: '泡泡玛特MOLLY城市系列成都限定', category: '潮玩', rarity: 'SR', stock: 25, status: 'approved', reviewNote: '', createdAt: '2026-02-15' },
  { id: 'prod004', name: '雷电将军手办', image: 'https://picsum.photos/seed/raiden/200/200', description: '原神雷电将军精致手办', category: '动漫IP', rarity: 'SR', stock: 15, status: 'pending', reviewNote: '', createdAt: '2026-05-18' },
  { id: 'prod005', name: '钟离限定立牌', image: 'https://picsum.photos/seed/zhongli/200/200', description: '原神钟离限定亚克力立牌', category: '动漫IP', rarity: 'SSR', stock: 5, status: 'rejected', reviewNote: '图片不清晰，请重新上传高清图片', createdAt: '2026-05-10' },
]

export const mockMerchantInventory: InventoryItem[] = [
  { id: 'inv001', productId: 'prod001', productName: '派蒙亚克力挂件', productImage: 'https://picsum.photos/seed/paimon/200/200', currentStock: 100, stockStatus: 'normal' },
  { id: 'inv002', productId: 'prod002', productName: '刻晴金属徽章', productImage: 'https://picsum.photos/seed/keqing/200/200', currentStock: 60, stockStatus: 'normal' },
  { id: 'inv003', productId: 'prod003', productName: 'MOLLY-成都造型', productImage: 'https://picsum.photos/seed/mollycd/200/200', currentStock: 3, stockStatus: 'low' },
  { id: 'inv004', productId: 'prod004', productName: '雷电将军手办', productImage: 'https://picsum.photos/seed/raiden/200/200', currentStock: 0, stockStatus: 'empty' },
]

export const mockInventoryRecords: InventoryRecord[] = [
  { id: 'ir001', productId: 'prod001', productName: '派蒙亚克力挂件', type: 'increase', beforeStock: 80, afterStock: 100, reason: '补货入库', createdAt: '2026-05-15T10:00:00' },
  { id: 'ir002', productId: 'prod002', productName: '刻晴金属徽章', type: 'decrease', beforeStock: 65, afterStock: 60, reason: '发放消耗', createdAt: '2026-05-14T14:30:00' },
  { id: 'ir003', productId: 'prod003', productName: 'MOLLY-成都造型', type: 'decrease', beforeStock: 10, afterStock: 3, reason: '发放消耗', createdAt: '2026-05-12T09:00:00' },
  { id: 'ir004', productId: 'prod004', productName: '雷电将军手办', type: 'modify', beforeStock: 15, afterStock: 0, reason: '盘点调整', createdAt: '2026-05-10T16:00:00' },
]

export const mockShipmentTasks: ShipmentTask[] = [
  {
    id: 'sh001', taskNo: 'SH20260515001', productName: '创意马克杯', productImage: 'https://picsum.photos/seed/mug/200/200',
    orderNo: 'ORD20260515001', receiverName: '张三', receiverPhone: '13800138000',
    receiverAddress: '北京市朝阳区某某路123号', status: 'pending',
    createdAt: '2026-05-15T10:00:00', shippedAt: null, logisticsCompany: null, trackingNo: null,
  },
  {
    id: 'sh002', taskNo: 'SH20260510001', productName: 'MOLLY-成都造型', productImage: 'https://picsum.photos/seed/mollycd/200/200',
    orderNo: 'ORD20260510001', receiverName: '李四', receiverPhone: '13800138001',
    receiverAddress: '上海市浦东新区某某大道456号', status: 'pending',
    createdAt: '2026-05-10T08:00:00', shippedAt: null, logisticsCompany: null, trackingNo: null,
  },
  {
    id: 'sh003', taskNo: 'SH20260428001', productName: '智能保温杯', productImage: 'https://picsum.photos/seed/thermos/200/200',
    orderNo: 'ORD20260428001', receiverName: '张三', receiverPhone: '13800138000',
    receiverAddress: '北京市朝阳区某某路123号', status: 'shipped',
    createdAt: '2026-04-28T14:00:00', shippedAt: '2026-04-29T09:00:00', logisticsCompany: '顺丰速运', trackingNo: 'SF1234567890',
  },
]

export const mockMerchantRecords: MerchantRecord[] = [
  { id: 'mr001', type: 'inventory', productName: '派蒙亚克力挂件', description: '库存增加', detail: '补货入库 80 → 100', createdAt: '2026-05-15T10:00:00' },
  { id: 'mr002', type: 'shipment', productName: '创意马克杯', description: '用户申请发货', detail: '订单 ORD20260515001 待发货', createdAt: '2026-05-15T10:00:00' },
  { id: 'mr003', type: 'inventory', productName: '刻晴金属徽章', description: '库存减少', detail: '发放消耗 65 → 60', createdAt: '2026-05-14T14:30:00' },
  { id: 'mr004', type: 'status_change', productName: '雷电将军手办', description: '商品提交审核', detail: '状态：草稿 → 待审核', createdAt: '2026-05-13T09:00:00' },
  { id: 'mr005', type: 'shipment', productName: '智能保温杯', description: '确认发货', detail: '顺丰速运 SF1234567890', createdAt: '2026-04-29T09:00:00' },
  { id: 'mr006', type: 'status_change', productName: '钟离限定立牌', description: '商品审核驳回', detail: '驳回原因：图片不清晰', createdAt: '2026-05-11T11:00:00' },
]
