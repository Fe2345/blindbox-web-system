import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/register',
    name: 'MerchantRegister',
    component: () => import('@/views/merchant/Register.vue'),
    meta: { noAuth: true },
  },
  {
    path: '/login',
    name: 'MerchantLogin',
    component: () => import('@/views/merchant/Login.vue'),
    meta: { noAuth: true },
  },
  {
    path: '/',
    component: () => import('@/layouts/MerchantLayout.vue'),
    children: [
      { path: '', name: 'MerchantDashboard', component: () => import('@/views/merchant/Dashboard.vue') },
      { path: 'application', name: 'MerchantApplication', component: () => import('@/views/merchant/Application.vue') },
      { path: 'profile', name: 'MerchantProfile', component: () => import('@/views/merchant/Profile.vue') },
      { path: 'products', name: 'MerchantProducts', component: () => import('@/views/merchant/ProductManage.vue') },
      { path: 'products/submit', name: 'ProductSubmit', component: () => import('@/views/merchant/ProductSubmit.vue') },
      { path: 'products/edit/:id', name: 'ProductEdit', component: () => import('@/views/merchant/ProductEdit.vue') },
      { path: 'inventory', name: 'MerchantInventory', component: () => import('@/views/merchant/InventoryManage.vue') },
      { path: 'shipments', name: 'MerchantShipments', component: () => import('@/views/merchant/ShipmentTasks.vue') },
      { path: 'orders', name: 'MerchantOrders', component: () => import('@/views/merchant/OrderManage.vue') },
      { path: 'records', name: 'MerchantRecords', component: () => import('@/views/merchant/RecordQuery.vue') },
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
  if (localStorage.getItem('merchant_logged_in') !== 'true') {
    if (localStorage.getItem('admin_logged_in') === 'true') {
      next({ path: '/login', query: { msg: 'admin' } })
    } else if (localStorage.getItem('isLoggedIn') === 'true') {
      next({ path: '/login', query: { msg: 'user' } })
    } else {
      next('/login')
    }
    return
  }
  next()
})

export default router
