import { createRouter, createWebHistory } from 'vue-router'

const routes = [
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
      { path: 'records', name: 'MerchantRecords', component: () => import('@/views/merchant/RecordQuery.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('merchant_token')
  if (!to.meta.noAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
