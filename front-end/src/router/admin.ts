import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'AdminLogin',
    component: () => import('@/views/admin/Login.vue'),
    meta: { noAuth: true },
  },
  {
    path: '/',
    component: () => import('@/layouts/AdminLayout.vue'),
    children: [
      { path: '', name: 'Dashboard', component: () => import('@/views/admin/Dashboard.vue') },
      { path: 'merchant-review', name: 'MerchantReview', component: () => import('@/views/admin/MerchantReview.vue') },
      { path: 'merchant-manage', name: 'MerchantManage', component: () => import('@/views/admin/MerchantManage.vue') },
      { path: 'user-manage', name: 'UserManage', component: () => import('@/views/admin/UserManage.vue') },
      { path: 'product-review', name: 'ProductReview', component: () => import('@/views/admin/ProductReview.vue') },
      { path: 'product-template', name: 'ProductTemplate', component: () => import('@/views/admin/ProductTemplate.vue') },
      { path: 'blindbox-config', name: 'BlindBoxConfig', component: () => import('@/views/admin/BlindBoxConfig.vue') },
      { path: 'prize-pool', name: 'PrizePool', component: () => import('@/views/admin/PrizePool.vue') },
      { path: 'order-manage', name: 'OrderManage', component: () => import('@/views/admin/OrderManage.vue') },
      { path: 'exchange-manage', name: 'ExchangeManage', component: () => import('@/views/admin/ExchangeManage.vue') },
      { path: 'rule-config', name: 'RuleConfig', component: () => import('@/views/admin/RuleConfig.vue') },
      { path: 'ledger', name: 'Ledger', component: () => import('@/views/admin/Ledger.vue') },
      { path: 'op-log', name: 'OpLog', component: () => import('@/views/admin/OpLog.vue') },
      { path: 'exception', name: 'Exception', component: () => import('@/views/admin/Exception.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  if (to.meta.noAuth) {
    next()
    return
  }
  if (localStorage.getItem('admin_logged_in') !== 'true') {
    next('/login')
    return
  }
  next()
})

export default router
